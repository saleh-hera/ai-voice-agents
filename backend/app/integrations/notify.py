"""Replaces the n8n "ping me on Slack when something needs attention" step
with a plain email. One function, no workflow tool, no extra service."""

import os
import smtplib
from email.mime.text import MIMEText

_SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
_SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
_SMTP_USER = os.getenv("SMTP_USER")
_SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
_FROM_EMAIL = os.getenv("NOTIFY_FROM_EMAIL")
_TO_EMAIL = os.getenv("NOTIFY_TO_EMAIL")


def notify_owner(subject: str, body: str) -> None:
    if not (_SMTP_USER and _SMTP_PASSWORD and _FROM_EMAIL and _TO_EMAIL):
        print(f"[notify disabled — no SMTP credentials] {subject}: {body}")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = _FROM_EMAIL
    msg["To"] = _TO_EMAIL

    with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT) as server:
        server.starttls()
        server.login(_SMTP_USER, _SMTP_PASSWORD)
        server.sendmail(_FROM_EMAIL, [_TO_EMAIL], msg.as_string())
