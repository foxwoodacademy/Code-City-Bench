import os
import sys
import csv
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

import domain_bridge
import event_envelope
import event_registry
import field_bridge
import field_server
from adapters import csv_ingest


class TempDbTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.old_db_path = field_bridge.DB_PATH
        field_bridge.DB_PATH = self.tmp.name

    def tearDown(self):
        field_bridge.DB_PATH = self.old_db_path
        try:
            os.unlink(self.tmp.name)
        except FileNotFoundError:
            pass


class EventEnvelopeTests(TempDbTestCase):
    def test_emit_adds_standard_envelope(self):
        field_bridge.emit(
            event_type="markets.trend.signal",
            location="test",
            source="unit_test",
            payload={"symbol": "EXAMPLE"},
            confidence=0.8,
            provenance={"source": "fixture"},
        )

        event = field_bridge.poll(limit=1)[0]
        envelope = event["payload"]["_lough"]
        self.assertEqual(envelope["schema_version"], 1)
        self.assertEqual(envelope["created_by"], "unit_test")
        self.assertEqual(envelope["confidence"], 0.8)
        self.assertEqual(envelope["provenance"]["source"], "fixture")
        self.assertEqual(envelope["review_status"], "unreviewed")

    def test_high_risk_prefix_defaults_to_review_required(self):
        payload = event_envelope.normalize_payload(
            event_type="safety_governance.misuse.risk",
            payload={"risk": "boundary"},
            source="unit_test",
        )

        self.assertEqual(payload["_lough"]["review_status"], "review_required")


class RegistryAndDomainBridgeTests(TempDbTestCase):
    def test_registry_loads_plugin_domain(self):
        self.assertIn("safety_governance", event_registry.all_namespaces())
        self.assertIn(
            "safety_governance.simulation.boundary",
            event_registry.all_event_types(),
        )

    def test_domain_bridge_emits_by_key(self):
        domain_bridge.emit_domain_event(
            domain="markets",
            event_key="trend_signal",
            location="test",
            source="unit_test",
            payload={"direction": "up"},
        )

        event = field_bridge.poll(limit=1)[0]
        self.assertEqual(event["event_type"], "markets.trend.signal")
        self.assertEqual(event["payload"]["direction"], "up")


class FieldServerTests(TempDbTestCase):
    def setUp(self):
        super().setUp()
        self.old_token = field_server.API_TOKEN
        self.old_allow_remote = field_server.ALLOW_REMOTE
        field_server.API_TOKEN = None
        field_server.ALLOW_REMOTE = False
        self.client = field_server.app.test_client()

    def tearDown(self):
        field_server.API_TOKEN = self.old_token
        field_server.ALLOW_REMOTE = self.old_allow_remote
        super().tearDown()

    def test_local_registry_request_allowed_without_token(self):
        response = self.client.get("/registry")
        self.assertEqual(response.status_code, 200)
        self.assertIn("markets", response.get_json())

    def test_remote_request_rejected_without_token(self):
        response = self.client.get(
            "/registry",
            environ_overrides={"REMOTE_ADDR": "203.0.113.10"},
        )
        self.assertEqual(response.status_code, 401)

    def test_token_allows_remote_request(self):
        field_server.API_TOKEN = "secret"
        response = self.client.get(
            "/registry",
            headers={"X-Lough-Token": "secret"},
            environ_overrides={"REMOTE_ADDR": "203.0.113.10"},
        )
        self.assertEqual(response.status_code, 200)

    def test_emit_accepts_envelope_fields(self):
        field_server.API_TOKEN = "secret"
        response = self.client.post(
            "/emit",
            json={
                "event_type": "markets.risk.alert",
                "location": "test",
                "source": "unit_test",
                "payload": {"risk": "fixture"},
                "confidence": 0.4,
                "provenance": {"source": "unit"},
                "review_status": "needs_context",
            },
            headers={"X-Lough-Token": "secret"},
            environ_overrides={"REMOTE_ADDR": "203.0.113.10"},
        )
        self.assertEqual(response.status_code, 200)

        event = field_bridge.poll(event_type="markets.risk.alert", limit=1)[0]
        self.assertEqual(event["payload"]["_lough"]["confidence"], 0.4)
        self.assertEqual(event["payload"]["_lough"]["review_status"], "needs_context")

    def test_create_client_and_emit_client_domain_event(self):
        response = self.client.post(
            "/clients",
            json={
                "name": "Example Client",
                "metadata": {"tier": "pilot"},
                "created_by": "unit_test",
            },
        )
        self.assertEqual(response.status_code, 201)
        client_id = response.get_json()["client"]["id"]

        emit_response = self.client.post(
            f"/clients/{client_id}/emit",
            json={
                "domain": "markets",
                "event_key": "trend_signal",
                "payload": {"symbol": "EXAMPLE"},
                "source": "unit_test",
            },
        )
        self.assertEqual(emit_response.status_code, 200)

        event = field_bridge.poll(event_type="markets.trend.signal", relation_id=client_id, limit=1)[0]
        self.assertEqual(event["relation_id"], client_id)
        self.assertEqual(event["payload"]["symbol"], "EXAMPLE")

    def test_review_queue_and_update_endpoint(self):
        field_bridge.emit(
            event_type="safety_governance.policy.review",
            location="test",
            source="unit_test",
            payload={"policy": "fixture"},
        )
        event = field_bridge.poll(event_type="safety_governance.policy.review", limit=1)[0]

        queue_response = self.client.get("/review")
        self.assertEqual(queue_response.status_code, 200)
        self.assertEqual(queue_response.get_json()[0]["id"], event["id"])

        update_response = self.client.post(
            f"/review/{event['id']}",
            json={
                "review_status": "approved_for_analysis",
                "reviewed_by": "unit_reviewer",
                "review_note": "fixture approved",
            },
        )
        self.assertEqual(update_response.status_code, 200)
        updated = update_response.get_json()["event"]
        envelope = updated["payload"]["_lough"]
        self.assertEqual(envelope["review_status"], "approved_for_analysis")
        self.assertEqual(envelope["reviewed_by"], "unit_reviewer")

        audit = field_bridge.poll(event_type="system.review.updated", limit=1)[0]
        self.assertEqual(audit["payload"]["event_id"], event["id"])


class CsvIngestTests(TempDbTestCase):
    def test_csv_ingest_dry_run(self):
        path = self._write_csv()
        result = csv_ingest.ingest_csv(
            path=path,
            domain="markets",
            event_key="price_tick",
            dry_run=True,
        )

        self.assertTrue(result["dry_run"])
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["preview"][0]["payload"]["price"], 12.5)

    def test_csv_ingest_emits_rows_and_completion_event(self):
        client_id = field_bridge.create_entity("client", "CSV Client", {})
        path = self._write_csv()
        result = csv_ingest.ingest_csv(
            path=path,
            domain="markets",
            event_key="price_tick",
            relation_id=client_id,
            source="unit_csv",
            created_by="unit_test",
        )

        self.assertEqual(result["rows"], 2)
        events = field_bridge.poll(event_type="markets.price.tick", relation_id=client_id, limit=5)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["payload"]["_lough"]["provenance"]["adapter"], "csv_ingest")

        completion = field_bridge.poll(event_type="system.ingest.completed", relation_id=client_id, limit=1)[0]
        self.assertEqual(completion["payload"]["rows_emitted"], 2)

    def _write_csv(self):
        tmp = tempfile.NamedTemporaryFile("w", newline="", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=["symbol", "price"])
            writer.writeheader()
            writer.writerow({"symbol": "AAA", "price": "12.5"})
            writer.writerow({"symbol": "BBB", "price": "13.75"})
        self.addCleanup(lambda: os.path.exists(tmp.name) and os.unlink(tmp.name))
        return tmp.name


if __name__ == "__main__":
    unittest.main()
