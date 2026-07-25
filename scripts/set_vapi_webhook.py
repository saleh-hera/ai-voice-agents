#!/usr/bin/env python3
"""
set_vapi_webhook.py
--------------------
Points a Vapi assistant's server webhook at the deployed dealer-engine
backend, so call events (missed calls, bookings) flow into it.

Usage:
    python set_vapi_webhook.py <assistant_id> <backend_url> [webhook_secret]

Example:
    python set_vapi_webhook.py 7b73d28b-695e-4942-a6ee-53cca48408d3 \
        https://your-backend.up.railway.app supersecret123

Reuses scripts/.env (same VAPI_API_KEY as sync_to_vapi.py).
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE = "https://api.vapi.ai"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    assistant_id = sys.argv[1]
    backend_url = sys.argv[2].rstrip("/")
    webhook_secret = sys.argv[3] if len(sys.argv) > 3 else None

    if not VAPI_API_KEY:
        print("Missing VAPI_API_KEY in scripts/.env")
        sys.exit(1)

    payload = {
        "server": {
            "url": f"{backend_url}/webhook/vapi",
        }
    }
    if webhook_secret:
        payload["server"]["secret"] = webhook_secret

    resp = requests.patch(
        f"{VAPI_BASE}/assistant/{assistant_id}",
        headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
        json=payload,
        timeout=30,
    )

    if resp.status_code >= 300:
        print(f"FAILED ({resp.status_code}): {resp.text}")
        print("If this complains about an unknown 'server' field, Vapi's assistant "
              "schema may have changed — check the current PATCH /assistant/:id body "
              "shape in the Vapi dashboard's API reference before retrying.")
        sys.exit(1)

    print(f"OK — assistant {assistant_id} server URL set to {backend_url}/webhook/vapi")


if __name__ == "__main__":
    main()
