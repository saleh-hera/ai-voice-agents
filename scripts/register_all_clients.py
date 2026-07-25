#!/usr/bin/env python3
"""
register_all_clients.py
------------------------
Reads every agent's agents/<name>/config.json and registers it as a client
in the dealer-engine backend, so each live agent has a config record the
engine can read (missed-call recovery, reminders, review requests).

Usage:
    python register_all_clients.py <backend_url>

Example:
    python register_all_clients.py https://dealer-engine-production.up.railway.app

Safe to re-run: existing clients are updated (PUT), not duplicated.
"""

import json
import sys
from pathlib import Path

import requests

AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"

# Maps each agent folder to the industry enum in clients/schemas/customer-config.schema.json
INDUSTRY_MAP = {
    "auto-dealership": "auto_dealership",
    "bella-restaurant": "restaurant",
    "dental-receptionist": "dental",
    "homeservices-dispatcher": "home_services",
    "lawfirm-intake": "law_firm",
    "mediassist-healthcare": "healthcare",
    "nova-sales": "retail",
    "nova-support": "other",
    "realestate-agent": "real_estate",
    "vault-assistant": "other",
}

# Default modules turned on for every agent — all three are implemented and
# tested in app/modules/. Enable/disable per-client later via PUT /client/{id}.
DEFAULT_MODULES = {
    "voiceAgent": {"enabled": True},
    "missedCallRecovery": {"enabled": True},
    "reminderNoShow": {"enabled": True},
    "reviewReputation": {"enabled": True},
}


def tier_for_price(amount_usd: int) -> str:
    if amount_usd == 0:
        return "starter"
    if amount_usd < 300:
        return "starter"
    if amount_usd < 400:
        return "growth"
    return "total_solution"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    backend_url = sys.argv[1].rstrip("/")

    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        config_path = agent_dir / "config.json"
        if not config_path.exists():
            continue

        config = json.loads(config_path.read_text(encoding="utf-8"))
        client_id = agent_dir.name
        industry = INDUSTRY_MAP.get(client_id, "other")
        pricing = config.get("pricing", {})
        amount = pricing.get("amountUsd", 0) or 0

        body = {
            "id": client_id,
            "name": config.get("name", client_id),
            "industry": industry,
            "phone": "",  # Vapi phone numbers aren't stored in config.json — fill in via PUT once known
            "modules": {**DEFAULT_MODULES},
            "tier": tier_for_price(amount),
            "monthly_price_usd": amount,
        }

        # Try create first; fall back to update if it already exists.
        resp = requests.post(f"{backend_url}/client", json=body, timeout=30)
        if resp.status_code == 409:
            resp = requests.put(f"{backend_url}/client/{client_id}", json=body, timeout=30)

        if resp.status_code >= 300:
            print(f"FAILED  {client_id}: {resp.status_code} {resp.text}")
        else:
            print(f"OK      {client_id} ({industry}, {config.get('assistantId')}) -> tier={body['tier']}")


if __name__ == "__main__":
    main()
