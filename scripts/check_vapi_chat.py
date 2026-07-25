#!/usr/bin/env python3
"""
check_vapi_chat.py
------------------
One-shot health check for the Vapi Chat API (AI Agents Vault Assistant).
Used by the scheduled "Vapi chat 402 watcher" to detect when chat starts working.

Prints one of:
  CHAT_WORKING   — chat responded successfully (the 402 is resolved!)
  STILL_402      — still blocked on the payment-method 402
  OTHER:<code>   — some other status (worth a look)

Reads VAPI_API_KEY from scripts/.env (never printed).
"""
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_ID = "7b73d28b-695e-4942-a6ee-53cca48408d3"
key = os.getenv("VAPI_API_KEY")

if not key:
    print("OTHER:no-key")
    sys.exit(0)

try:
    r = requests.post(
        "https://api.vapi.ai/chat",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"assistantId": ASSISTANT_ID, "input": "healthcheck: are you there?"},
        timeout=60,
    )
except Exception as e:
    print(f"OTHER:exception-{type(e).__name__}")
    sys.exit(0)

if r.status_code == 402:
    print("STILL_402")
elif r.ok:
    print("CHAT_WORKING")
else:
    print(f"OTHER:{r.status_code}")
