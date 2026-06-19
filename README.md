<div align="center">

# 🎙️ AI Voice Agents

### Production AI voice agents that answer business calls 24/7 — taking reservations, orders, and customer questions without ever putting anyone on hold.

Built and deployed by **[Sk Abu Sheleh Hera (Saleh)](https://www.linkedin.com/in/sk-abu-sheleh-hera/)** · Founder of [AI Agents Vault](https://www.aiagentsvault.tech)

[![Live Site](https://img.shields.io/badge/Live-aiagentsvault.tech-7c3aed?style=for-the-badge)](https://www.aiagentsvault.tech)
[![Voice AI](https://img.shields.io/badge/Voice%20AI-Vapi-6366f1?style=for-the-badge)](https://vapi.ai)
[![Status](https://img.shields.io/badge/Status-Live%20in%20Production-22c55e?style=for-the-badge)](https://www.aiagentsvault.tech)

</div>

---

## 👋 What this is

This repository is the **source of truth** for three live AI voice agents I designed, prompt-engineered, voiced, and shipped to production. Each one is a real, callable agent — you can talk to them right now using the demo links below.

Every agent in this repo includes:
- 🧠 Its full **system prompt** (the behavior engine)
- ⚙️ A **config file** (voice, model, and connection settings)
- 📄 A **README** explaining what it does and how it works
- 🎧 A **live demo link** so anyone can hear it in action

---

## 🤖 The Agents

| Agent | Role | Industry | Live Demo |
|-------|------|----------|-----------|
| **[Bella](agents/bella-restaurant)** | Restaurant Receptionist | Hospitality | [🎧 Talk to Bella](https://vapi.ai/?demo=true&shareKey=6b3a74e2-b47c-4c0f-93d4-a3d4b8e5d674&assistantId=24804ad8-2f6d-4b73-a5df-f76d37fe8dd0) |
| **[Nova Sales](agents/nova-sales)** | E-Commerce Shopping Assistant | Retail / E-Commerce | [🎧 Talk to Nova Sales](https://vapi.ai/?demo=true&shareKey=6b3a74e2-b47c-4c0f-93d4-a3d4b8e5d674&assistantId=cc8183ab-1e8f-4a81-afbf-40e7f7a31212) |
| **[Nova Support](agents/nova-support)** | 24/7 Customer Service Agent | Any Business | [🎧 Talk to Nova Support](https://vapi.ai/?demo=true&shareKey=6b3a74e2-b47c-4c0f-93d4-a3d4b8e5d674&assistantId=0969aa62-f3b8-4406-b700-67ea3f87014e) |

> 💡 Each agent is also available as a deployable product on the marketplace: **[aiagentsvault.tech](https://www.aiagentsvault.tech)**

---

## 🛠️ Tech Stack

- **Voice AI Platform:** [Vapi](https://vapi.ai) — real-time voice infrastructure
- **Prompt Engineering:** Custom multi-section system prompts (persona, guardrails, conversation flows, escalation logic)
- **Payments / Subscriptions:** Stripe (recurring billing with free trials)
- **Marketplace Front-End:** Next.js 14 + TypeScript + Tailwind ([website repo](https://github.com/saleh-hera/aiagentsvaultwebsite))
- **Automation:** Python sync script that pushes prompt + config changes straight to Vapi (see [`/scripts`](scripts))

---

## ⚙️ How it works

```
   system-prompt.md  +  config.json
            │
            ▼
   scripts/sync_to_vapi.py   ──►   Vapi API   ──►   Live callable agent
            │
            ▼
   Edit a file, run one command, the agent updates.
```

Instead of clicking through a dashboard, each agent's behavior lives in version-controlled files. Change the prompt, run the sync script, and the live agent updates — fully reproducible and trackable in Git.

---

## 📂 Repo Structure

```
ai-voice-agents/
├── agents/
│   ├── bella-restaurant/    → Restaurant receptionist
│   ├── nova-sales/          → E-commerce shopping assistant
│   └── nova-support/        → Customer service agent
├── scripts/
│   └── sync_to_vapi.py      → Push prompt + config to Vapi
└── README.md
```

---

## 📬 About the Builder

I'm **Saleh** — a data & analytics professional turned AI builder. I design and ship conversational AI agents that solve real business problems (missed calls, slow support, lost orders).

- 🌐 **Marketplace:** [aiagentsvault.tech](https://www.aiagentsvault.tech)
- 💼 **LinkedIn:** [Sk Abu Sheleh Hera](https://www.linkedin.com/in/sk-abu-sheleh-hera/)
- 🧠 **What I build:** Voice agents, customer-service automation, and the platforms around them

---

<div align="center">

*Built with care. Talk to the agents — they're real.* 🎙️

</div>
