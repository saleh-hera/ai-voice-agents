# AI Digital Dealer — Engine

The n8n-free backend for the modular funnel: one FastAPI app, one database,
plain Python functions per module. See `clients/schemas/customer-config.schema.json`
in the repo root for the config shape this mirrors.

## Run it locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # then fill in Twilio/SMTP creds (optional for local testing)
uvicorn app.main:app --reload
```

Server starts at `http://127.0.0.1:8000`. SQLite file `dealer_engine.db` is
created automatically on first run — nothing else to set up.

Without Twilio/SMTP credentials filled in, `send_sms` and `notify_owner` just
print to the console instead of failing — safe to run and test locally with
zero external accounts.

## Create a test client

```bash
curl -X POST http://127.0.0.1:8000/client -H "Content-Type: application/json" -d "{
  \"id\": \"bright-smile-dental\",
  \"name\": \"Bright Smile Dental\",
  \"industry\": \"dental\",
  \"phone\": \"+15551234567\",
  \"modules\": {
    \"voiceAgent\": {\"enabled\": true},
    \"missedCallRecovery\": {\"enabled\": true},
    \"reminderNoShow\": {\"enabled\": true},
    \"reviewReputation\": {\"enabled\": true}
  },
  \"tier\": \"growth\",
  \"monthly_price_usd\": 699
}"
```

## Simulate a missed call from Vapi

```bash
curl -X POST http://127.0.0.1:8000/webhook/vapi -H "Content-Type: application/json" -d "{
  \"client_id\": \"bright-smile-dental\",
  \"event_type\": \"call.missed\",
  \"caller_name\": \"Jane Doe\",
  \"caller_phone\": \"+15559876543\"
}"
```

You should see a `[twilio disabled — no credentials] would send to +15559876543: ...`
line in the server console — that's `missedCallRecovery` firing correctly.

## Wire it to a real Vapi assistant

In the Vapi dashboard, set the assistant's Server URL to your deployed
backend's `/webhook/vapi` endpoint (and set `VAPI_WEBHOOK_SECRET` in both
Vapi and your `.env` so the endpoint can verify requests). Vapi's actual
payload shape is richer than `VapiWebhookPayload` in `app/schemas.py` —
extend that schema once you're looking at a real webhook payload from your
existing agents.

## Run the scheduler manually

```bash
python -m app.scheduler
```

This is what `.github/workflows/dealer-engine-scheduler.yml` runs hourly once
deployed — it checks for due reminders and post-visit review requests and
fires the matching module. No n8n anywhere in this path.

## Adding a new module

1. Write a function in `app/modules/your_module.py` with signature
   `run(client: Client, lead: Lead) -> None`.
2. Add one line to `app/modules/registry.py` — either `LIVE_EVENT_MODULES`
   (fires off a webhook event) or `SCHEDULED_MODULES` (fires off the cron).
3. Add the module's id to a client's `modules` dict with `enabled: true`.

No new service, no visual workflow — just a function and a dict entry.

## Deploying

Any small always-on host works (Railway, Render, a cheap VPS). Point
`DATABASE_URL` at a real Postgres instance once you're past a couple of
pilot clients — SQLAlchemy means no code changes, just an env var.
