#!/usr/bin/env python3
"""
set_all_vapi_webhooks.py
--------------------------
Points EVERY agent's Vapi server webhook at the deployed dealer-engine
backend, reading each assistantId straight from agents/<name>/config.json.

Usage:
    python set_all_vapi_webhooks.py <backend_url> [webhook_secret]

Example:
    python set_all_vapi_webhooks.py https://dealer-engine-production.up.railway.app supersecret123

⚠️ This changes the server URL on every LIVE agent, including ones with real
   paying subscribers (Bella, Nova Sales, Nova Support). Confirm the backend
   is actually deployed and its /health endpoint responds before running this
   against production traffic.

Reuses scripts/.env (same VAPI_API_KEY as sync_to_vapi.py).
"""

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE = "https://api.vapi.ai"
AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    if not VAPI_API_KEY:
        print("Missing VAPI_API_KEY in scripts/.env")
        sys.exit(1)

    backend_url = sys.argv[1].rstrip("/")
    webhook_secret = sys.argv[2] if len(sys.argv) > 2 else None

    payload = {"server": {"url": f"{backend_url}/webhook/vapi"}}
    if webhook_secret:
        payload["server"]["secret"] = webhook_secret

    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        config_path = agent_dir / "config.json"
        if not config_path.exists():
            continue

        config = json.loads(config_path.read_text(encoding="utf-8"))
        assistant_id = config.get("assistantId")
        if not assistant_id:
            print(f"SKIP    {agent_dir.name}: no assistantId in config.json")
            continue

        resp = requests.patch(
            f"{VAPI_BASE}/assistant/{assistant_id}",
            headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
            json=payload,
            timeout=30,
        )

        if resp.status_code >= 300:
            print(f"FAILED  {agent_dir.name} ({assistant_id}): {resp.status_code} {resp.text}")
        else:
            print(f"OK      {agent_dir.name} ({assistant_id})")


if __name__ == "__main__":
    main()
