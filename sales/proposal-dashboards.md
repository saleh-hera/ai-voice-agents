# Proposal Dashboards ("Proposal Desk")

Self-serve client proposal tools, live on the website (deployed 2026-07-22,
website repo commit 9561f98, static files in `public/proposals/`).

## Live URLs

| Industry | Agent | URL |
|---|---|---|
| Restaurant | Bella | https://aiagentsvault.tech/proposals/restaurant.html |
| Law firm | LexAssist | https://aiagentsvault.tech/proposals/law.html |
| Dental | DentaDesk | https://aiagentsvault.tech/proposals/dental.html |
| Real estate | HomeConnect | https://aiagentsvault.tech/proposals/realestate.html |

Private claude.ai artifact copies (originals):
- General/restaurant: https://claude.ai/code/artifact/42bf9a1f-c848-489e-b9ef-29ba0b70f7d6
- Law: https://claude.ai/code/artifact/e143e261-4e59-49bb-9b5b-14d6b418cde5
- Dental: https://claude.ai/code/artifact/6bd32412-ef3d-4d0c-b597-284678251d08
- Real estate: https://claude.ai/code/artifact/f68ed055-efd7-4b9e-8f5b-3c936cbf00f5

## How it works

**Admin side (Saleh):**
1. Open the industry page → Admin tab
2. Set "Replies go to" email once (left panel)
3. Add the client, add service line items (name, price/mo, description, projected return/mo)
4. Totals panel shows monthly fee, projected return, net gain, ROI multiple
5. "Copy client link" → sends the whole proposal encoded in the URL hash
6. "Export all data (JSON)" for backup (data lives in the browser's localStorage, per page)

**Client side (the customer):**
- Opens the link → sees only a clean proposal document with their name
- Every service starts ON; toggling one OFF shows in red exactly what they
  give up ("Cutting this gives up $X/mo in projected returns — to save $Y/mo")
- Live totals: monthly fee, projected return kept, ROI multiple, return given up
- Submit → opens a prefilled email back to the reply address with their KEEP/CUT list

## Usage rules (agreed 2026-07-22)

- **Do NOT put these links in cold Apollo sequences** — wrong funnel stage,
  and an unexpected tool link hurts trust/deliverability. Cold emails keep
  one CTA: the demo page.
- Use at **reply stage** (prospect answered and asked about pricing),
  **trial stage** (day ~5: "here's your plan, toggle and send back"), and
  **renewal/downgrade conversations** with live clients.
- Keep projected-return numbers defensible (aligned with the site's ROI
  calculator math). They are labeled "projected" — never present as guarantees.
- Pages are `noindex` and unlinked from site navigation on purpose.

## Possible next step (not built)

"Build your plan" public configurator embedded on each agent marketplace page
(a1/a9/a10/a11): pre-filled services, same toggle-and-see-loss mechanic, CTA =
start trial / request callback with the chosen plan attached. Decided 2026-07-22
that the two-sided admin tool itself does NOT belong on public agent pages.
