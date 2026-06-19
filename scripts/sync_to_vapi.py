#!/usr/bin/env python3
"""
sync_to_vapi.py
---------------
Push each agent's system prompt + config straight to Vapi.

This is the "automation" layer: instead of editing agents by clicking through
the Vapi dashboard, each agent's behavior lives in version-controlled files
(system-prompt.md + config.json). Run this script and the live agent updates.

Usage:
    1. pip install -r requirements.txt
    2. Copy .env.example to .env and add your VAPI_API_KEY
    3. python sync_to_vapi.py            # sync all agents
       python sync_to_vapi.py bella-restaurant   # sync one agent

Get your Vapi API key from: https://dashboard.vapi.ai  (Settings -> API Keys)
"""

import os
import sys
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE = "https://api.vapi.ai"
AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"


def load_agent(agent_dir: Path) -> dict:
    """Read an agent's config.json and its referenced system prompt."""
    config = json.loads((agent_dir / "config.json").read_text(encoding="utf-8"))
    prompt_file = agent_dir / config["model"]["systemPromptFile"]
    config["_system_prompt"] = prompt_file.read_text(encoding="utf-8")
    return config


def build_payload(config: dict) -> dict:
    """Shape the config into the body Vapi expects for an assistant update."""
    return {
        "firstMessage": config.get("firstMessage", ""),
        "model": {
            "provider": config["model"]["provider"],
            "model": config["model"]["model"],
            "messages": [
                {"role": "system", "content": config["_system_prompt"]}
            ],
        },
    }


def sync_agent(agent_dir: Path) -> None:
    if not VAPI_API_KEY:
        sys.exit("❌ Missing VAPI_API_KEY. Copy .env.example to .env and add your key.")

    config = load_agent(agent_dir)
    assistant_id = config["assistantId"]
    payload = build_payload(config)

    print(f"→ Syncing '{config['name']}'  ({agent_dir.name})")
    resp = requests.patch(
        f"{VAPI_BASE}/assistant/{assistant_id}",
        headers={
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    if resp.status_code in (200, 201):
        print(f"  ✅ Updated successfully.\n")
    else:
        print(f"  ❌ Failed ({resp.status_code}): {resp.text}\n")


def main() -> None:
    targets = sys.argv[1:]
    agent_dirs = sorted(p for p in AGENTS_DIR.iterdir() if (p / "config.json").exists())

    if targets:
        agent_dirs = [d for d in agent_dirs if d.name in targets]
        if not agent_dirs:
            sys.exit(f"No matching agents for: {', '.join(targets)}")

    print(f"\nSyncing {len(agent_dirs)} agent(s) to Vapi...\n")
    for d in agent_dirs:
        sync_agent(d)
    print("Done. 🎙️")


if __name__ == "__main__":
    main()
