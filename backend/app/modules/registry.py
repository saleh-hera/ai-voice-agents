"""Single source of truth for 'module id -> the function that runs it'.
Adding a new module later means: write the function, add one line here.
No workflow tool, no visual wiring — just a dict."""

from app.modules import missed_call_recovery, reminder_no_show, review_reputation

# Modules triggered live, off a Vapi webhook event
LIVE_EVENT_MODULES = {
    "missedCallRecovery": missed_call_recovery.run,
}

# Modules triggered on a schedule (see app/scheduler.py)
SCHEDULED_MODULES = {
    "reminderNoShow": reminder_no_show.run,
    "reviewReputation": review_reputation.run,
}
