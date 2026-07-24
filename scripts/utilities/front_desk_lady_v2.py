from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

VOLTAGE_URL = "https://payments.voltage.cloud"
DEFAULT_PACKAGES_DIR = Path("./saas_packages")
DEFAULT_LOG_PATH = Path("front_desk_routing_log.json")

class FrontDeskLady:
    def __init__(self, lightning_account_id=None, voltage_api_key=None, dry_run=False):
        self.lightning_account_id = lightning_account_id
        self.voltage_api_key = voltage_api_key
        self.dry_run = dry_run
        self.packages = []
        self.routing_log = []

    def load_packages(self, directory):
        path = Path(directory)
        if not path.exists():
            print(f"[ERROR] Directory {path} does not exist.")
            return
        for file_path in sorted(path.glob("*.json")):
            try:
                with file_path.open("r", encoding="utf-8") as fh:
                    self.packages.append(json.load(fh))
                print(f"[LOADED] {file_path.name}")
            except Exception as exc:
                print(f"[SKIP] {file_path.name}: {exc}")

    def create_voltage_invoice(self, package):
        if not self.voltage_api_key:
            return None, None

        amount_sats = int(package.get("price_sats", 1000))
        memo = f"Vertical AI: {package.get('name', 'SaaS Package')}"

        payload = json.dumps({
            "amount": amount_sats,
            "description": memo,
            "currency": "BTC",
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{VOLTAGE_URL}/api/v1/invoices",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.voltage_api_key}",
                "Content-Type": "application/json",
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return data.get("payment_request"), data.get("id")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode()
            print(f"  [Voltage] HTTP {exc.code}: {body[:120]}")
            return None, None
        except Exception as exc:
            print(f"  [Voltage] Error: {exc}")
            return None, None

    def route_package(self, package, platform_filter=None):
        name = package.get("name", "Unnamed")
        print(f"\n[ROUTING] {name}")
        platforms = package.get("target_platforms", ["Fiverr", "Upwork"])
        if platform_filter:
            platforms = [p for p in platforms if p.lower() == platform_filter.lower()]
            if not platforms:
                print(f"  [SKIP] No match for platform filter '{platform_filter}'")
                return

        invoice_bolt11, payment_id = None, None
        if not self.dry_run:
            invoice_bolt11, payment_id = self.create_voltage_invoice(package)
            if invoice_bolt11:
                print(f"  [Voltage] Invoice created (id: {str(payment_id)[:12]}...)")
            else:
                print(f"  [Voltage] No invoice — check API key or connectivity")

        for platform in platforms:
            summary = self.generate_markdown_summary(package, platform, invoice_bolt11)
            self.routing_log.append(
                {
                    "package_name": name,
                    "platform": platform,
                    "status": "DRY_RUN" if self.dry_run else "Routed",
                    "payment_id": payment_id,
                    "invoice_bolt11": invoice_bolt11,
                    "summary": summary,
                }
            )
            tag = "[DRY]" if self.dry_run else "[OK]"
            print(f"  {tag} → {platform}")

    def generate_markdown_summary(self, package, platform, invoice_bolt11=None):
        lines = [
            f"### [New SaaS Offering] {package['name']} on {platform}",
            "",
            f"**Tagline:** {package.get('tagline', '')}",
            "",
            f"**Description:** {package.get('description', '')}",
            "",
            "**Key Features:**",
        ]
        for feature in package.get("features", []):
            lines.append(f"- {feature}")
        lines += [
            "",
            f"**Pricing:** {package.get('pricing_model', '')}",
            f"**Estimated ROI:** {package.get('estimated_roi_per_business', '')}",
            "",
            "**Payment Method:** Lightning Network (BTC)",
            f"**Lightning Address:** {self.lightning_account_id or 'NOT CONFIGURED'}",
        ]
        if invoice_bolt11:
            lines.append(f"**BOLT11 Invoice:** `{invoice_bolt11}`")
        return "\n".join(lines)

    def run(self, platform_filter=None):
        if not self.packages:
            print("[ABORT] No packages loaded.")
            return
        mode = "DRY RUN" if self.dry_run else "LIVE"
        print(f"\n=== Mrs. Higgins ON DUTY [{mode}] — {len(self.packages)} package(s) ===")
        for package in self.packages:
            self.route_package(package, platform_filter=platform_filter)
        self.save_routing_log()

    def save_routing_log(self):
        DEFAULT_LOG_PATH.write_text(json.dumps(self.routing_log, indent=2), encoding="utf-8")
        print(f"\n[DONE] {len(self.routing_log)} route(s) logged → {DEFAULT_LOG_PATH}")


def main():
    parser = argparse.ArgumentParser(description="Front Desk Lady — SaaS package router")
    parser.add_argument("--packages-dir", default=str(DEFAULT_PACKAGES_DIR))
    parser.add_argument("--platform", default=None, help="Fiverr | Upwork | Nostr")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = {}
    config_path = Path("front_desk_config.json")
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))

    lightning_id = os.getenv("LIGHTNING_ACCOUNT_ID", config.get("lightning_account_id"))
    voltage_api_key = os.getenv("VOLTAGE_API_KEY", config.get("voltage_api_key"))

    if not voltage_api_key:
        print("[WARN] No Voltage API key. Invoices will be skipped.")
        print("       Set voltage_api_key in front_desk_config.json or VOLTAGE_API_KEY env var.")

    fdl = FrontDeskLady(lightning_id, voltage_api_key, dry_run=args.dry_run)
    fdl.load_packages(args.packages_dir)
    fdl.run(platform_filter=args.platform)


if __name__ == "__main__":
    main()
