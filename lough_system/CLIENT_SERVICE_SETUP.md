# Client Service Setup

This is the low-cost path for using Lough with clientele while keeping the system auditable and controlled.

## Minimum Viable Service

Run the service locally first:

```bash
export LOUGH_API_TOKEN="replace-with-a-long-random-token"
python ~/lough_system/field_server.py
```

Create one client entity per client:

```bash
curl -X POST http://127.0.0.1:7070/clients \
  -H "Content-Type: application/json" \
  -H "X-Lough-Token: $LOUGH_API_TOKEN" \
  -d '{"name":"Pilot Client","metadata":{"tier":"pilot","contact":"manual"}}'
```

Emit client-linked events:

```bash
curl -X POST http://127.0.0.1:7070/clients/1/emit \
  -H "Content-Type: application/json" \
  -H "X-Lough-Token: $LOUGH_API_TOKEN" \
  -d '{"domain":"markets","event_key":"trend_signal","payload":{"symbol":"EXAMPLE","direction":"up"}}'
```

Export a client review bundle:

```bash
python ~/lough_system/export_events.py --relation-id 1 --limit 500 > client_1_events.jsonl
```

Review client events before delivery:

```bash
curl "http://127.0.0.1:7070/review?relation_id=1" \
  -H "X-Lough-Token: $LOUGH_API_TOKEN"
```

Mark a reviewed event:

```bash
curl -X POST http://127.0.0.1:7070/review/123 \
  -H "Content-Type: application/json" \
  -H "X-Lough-Token: $LOUGH_API_TOKEN" \
  -d '{"review_status":"approved_for_analysis","reviewed_by":"your_name","review_note":"scope and provenance checked"}'
```

## Low-Cost Operating Model

Start with manual or batch workflows:
- Create client entities through `/clients`.
- Import client data through CSV files.
- Export JSONL review bundles.
- Send reports manually after review.

Avoid public exposure until these are true:
- `LOUGH_API_TOKEN` is set.
- You know who is allowed to call the endpoint.
- You have a backup/export habit.
- You have reviewed the data source authorization.
- You have a way to revoke access.

## Client Boundary

Every client should have:
- One `client` entity.
- A short metadata record with scope, contact method, and authorization basis.
- Events linked through `relation_id`.
- Review-required events checked by a human before being used in a consequential report.

Do not mix multiple clients under the same relation ID.

## Phase 2 CSV Workflow

Dry run first:

```bash
python ~/lough_system/adapters/csv_ingest.py ./client_data.csv \
  --domain markets \
  --event-key price_tick \
  --relation-id 1 \
  --dry-run
```

Import after review:

```bash
python ~/lough_system/adapters/csv_ingest.py ./client_data.csv \
  --domain markets \
  --event-key price_tick \
  --relation-id 1
```

## Human Checklist Before Onboarding a Client

- Confirm the client understands this is decision support, not a guarantee.
- Confirm the data source is authorized.
- Confirm whether personal data is present.
- Confirm which domain and event types will be used.
- Confirm whether outputs require review before delivery.
- Confirm export/backup handling.
