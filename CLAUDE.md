# CLAUDE.md

## What this project is

A portfolio of live AI voice agents built on [Vapi](https://vapi.ai) and deployed for real clients. Each agent has a versioned system prompt and config file; running `scripts/sync_to_vapi.py` pushes changes directly to the live Vapi assistant — no dashboard clicking required.

## Tech stack

| Layer | Tool |
|---|---|
| Voice AI platform | Vapi |
| LLM | OpenAI GPT-4o (per agent) |
| Sync script | Python 3 + `requests` + `python-dotenv` |
| Payments | Stripe (checkout links in each `config.json`) |
| Version control | Git / GitHub |

## Key files

```
agents/<name>/system-prompt.md   — the agent's full behavior instructions
agents/<name>/config.json        — assistantId, voice, pricing, Stripe link
scripts/sync_to_vapi.py          — pushes agents to Vapi via PATCH /assistant/:id
scripts/.env.example             — template for VAPI_API_KEY (never commit .env)
clients/tonys-pizza/             — first real client deployment (copy of Bella)
```

## The three agents

### Bella — Restaurant AI Receptionist
- **Folder:** `agents/bella-restaurant/`
- **Vapi assistant ID:** `24804ad8-2f6d-4b73-a5df-f76d37fe8dd0`
- **Voice:** warm female host
- **Price:** $199/month, 7-day free trial
- **Stripe checkout:** `https://buy.stripe.com/dRmcMYg8KcC2ch37Rabsc00`
- **Use case:** Takes reservations, handles menu questions, manages incoming restaurant calls

### Nova Sales — E-Commerce AI Assistant
- **Folder:** `agents/nova-sales/`
- **Vapi assistant ID:** `cc8183ab-1e8f-4a81-afbf-40e7f7a31212`
- **Voice:** upbeat female shopping assistant
- **Price:** $179/month, 7-day free trial
- **Stripe checkout:** `https://buy.stripe.com/eVqfZa9KmgSi0yl2wQbsc01`
- **Use case:** Helps place orders, track shipments, and find products for e-commerce stores

### Nova Support — 24/7 Customer Service Agent
- **Folder:** `agents/nova-support/`
- **Vapi assistant ID:** `0969aa62-f3b8-4406-b700-67ea3f87014e`
- **Voice:** calm, empathetic female
- **Price:** $199/month, 7-day free trial
- **Stripe checkout:** `https://buy.stripe.com/4gM00ccWy9pQ4OBdbubsc02`
- **Use case:** General-purpose support agent for any business, handles complaints and FAQs

## Rules

1. **Always show what changed before pushing.** Run `git diff` and share a summary of changes before any `git push`. No silent pushes.

2. **Never expose or commit secret keys.** `VAPI_API_KEY` and any other credentials live only in `.env` (which is gitignored). Never hardcode keys in any file, never stage `.env`, and never log keys to the console.

3. **Do not change Stripe payment links unless explicitly asked.** The `checkoutUrl` fields in each `config.json` are live payment links tied to real subscriptions. Leave them exactly as-is unless the user specifically requests a change.
