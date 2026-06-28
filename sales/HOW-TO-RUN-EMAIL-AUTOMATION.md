# How to Run the Email Automation

## Step 1 — Get Your Leads (30 min today)

### Apollo.io (free, 50 leads/month)
1. Go to apollo.io → Sign up free
2. Click "Search" → People
3. Filter:
   - Title: "Owner" OR "Practice Manager" OR "Office Manager" OR "Dentist" OR "Attorney" OR "Broker" OR "Realtor"
   - Industry: Health Care (for dental), Legal Services, Real Estate, Restaurants
   - Location: California
   - Employee count: 1–20
4. Export 50 contacts → download CSV
5. Open the CSV, copy name/business/email/city into `leads-template.csv`

### Google Maps (free, unlimited)
Search these and collect business name + phone (look up email on their website):
- "dental office Los Angeles"
- "law firm San Diego"
- "real estate agency San Francisco"
- "restaurant Santa Monica"

### LinkedIn (free)
- Search for owners (see linkedin-templates.md for search terms)
- Find their email via LinkedIn or guess: firstname@businessname.com

---

## Step 2 — Fill In The Lead Spreadsheet

Open `leads-template.csv` and fill in at least 50 leads:
- Name (first name for email personalization)
- Business (for subject line personalization)
- Type: DentaDesk / HomeConnect / LexAssist / Bella
- City
- Email

---

## Step 3 — Run Email Automation with Claude

Once your lead list is ready, paste it into Claude (this chat) and say:

**"Send the Day 1 email to all leads in my list using the email templates"**

Claude will:
1. Read each lead from the list
2. Pick the right email template (DentaDesk/HomeConnect/LexAssist/Bella)
3. Personalize with their name + business name + city
4. Send via Gmail MCP from saleh.hira@gmail.com
5. Space sends 8 minutes apart (so Gmail doesn't flag as spam)

---

## Step 4 — Follow-Ups (Day 3 and Day 6)

Come back to Claude on Day 3 and say:
**"Check my lead list and send follow-up email 2 to anyone who hasn't replied yet"**

Claude reads the list, skips anyone who replied, and sends the Day 3 follow-up.

Same on Day 6: **"Send the final follow-up to non-replies"**

---

## Step 5 — Handle Replies

When someone replies interested, paste their email into Claude and say:
**"Someone replied to my DentaDesk email. Help me respond and send them the trial link."**

Claude drafts the reply and can send it via Gmail MCP.

---

## Daily Routine (20 min/day total)

| Time | Task | Time |
|---|---|---|
| 8:30am | Tell Claude to send today's 40 emails | 5 min |
| 12:00pm | LinkedIn — 15 DMs (use linkedin-templates.md) | 15 min |
| 12:15pm | Post in 2 Facebook groups (use facebook-reddit-templates.md) | 5 min |
| Evening | Reply to any responses Claude flagged | 10 min |

---

## Gmail Sending Limits (to avoid spam)
- Max 40 emails/day from personal Gmail (free)
- Space at least 8 minutes between each send
- Use your real name in the From field (already set as Saleh Hira)
- If you want to send more: get Google Workspace ($6/mo) — allows 500/day
