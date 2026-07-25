"""Run periodically by a GitHub Actions cron job (same pattern as
daily-apollo-lead-loader.yml) — replaces n8n's time-based triggers.

    python -m app.scheduler

Checks every client's due reminders and post-visit review requests, and
fires the matching module. Safe to run hourly; each lead only gets a
reminder/review message once (tracked via lead.reminder_sent / status).
"""

import datetime

from app.config_loader import is_enabled
from app.database import SessionLocal
from app.models import Client, Lead
from app.modules.registry import SCHEDULED_MODULES


def run_due_reminders(db) -> int:
    now = datetime.datetime.now(datetime.UTC)
    window_end = now + datetime.timedelta(hours=24)

    due = (
        db.query(Lead)
        .filter(
            Lead.status == "booked",
            Lead.reminder_sent.is_(False),
            Lead.appointment_time.isnot(None),
            Lead.appointment_time <= window_end,
            Lead.appointment_time >= now,
        )
        .all()
    )

    sent = 0
    for lead in due:
        client = db.get(Client, lead.client_id)
        if client and is_enabled(client, "reminderNoShow"):
            SCHEDULED_MODULES["reminderNoShow"](client, lead)
            sent += 1
    return sent


def run_review_requests(db) -> int:
    now = datetime.datetime.now(datetime.UTC)
    cutoff = now - datetime.timedelta(hours=4)

    completed = (
        db.query(Lead)
        .filter(
            Lead.status == "booked",
            Lead.appointment_time.isnot(None),
            Lead.appointment_time <= cutoff,
        )
        .all()
    )

    sent = 0
    for lead in completed:
        client = db.get(Client, lead.client_id)
        if client and is_enabled(client, "reviewReputation"):
            SCHEDULED_MODULES["reviewReputation"](client, lead)
            lead.status = "completed_reviewed"
            sent += 1
    return sent


def main():
    db = SessionLocal()
    try:
        reminders_sent = run_due_reminders(db)
        reviews_sent = run_review_requests(db)
        db.commit()
        print(f"scheduler run complete: {reminders_sent} reminders, {reviews_sent} review requests")
    finally:
        db.close()


if __name__ == "__main__":
    main()
