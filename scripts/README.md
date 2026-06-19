# 🔄 Automation — Sync agents to Vapi

This folder holds the automation that keeps the live agents in sync with the
files in this repo.

## What it does
`sync_to_vapi.py` reads each agent's `config.json` + `system-prompt.md` and
pushes them straight to the Vapi API. Edit a prompt, run the script, the live
agent updates — no dashboard clicking, fully version-controlled.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env        # then paste your VAPI_API_KEY into .env
```

## Run
```bash
python sync_to_vapi.py                  # sync all agents
python sync_to_vapi.py bella-restaurant # sync just one
```

> 🔐 Your API key lives only in `.env`, which is git-ignored and never committed.
