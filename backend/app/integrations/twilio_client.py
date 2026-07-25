"""Transactional SMS only — missed-call recovery, reminders, review requests
sent to someone who already called/booked. This is a different consent
category than the parked cold-SMS-to-scraped-leads project (that one hit
TCPA/10DLC opt-in rejection); do not repurpose this client for cold outreach.
"""

import os

from twilio.rest import Client as TwilioRestClient

_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

_client: TwilioRestClient | None = None
if _ACCOUNT_SID and _AUTH_TOKEN:
    _client = TwilioRestClient(_ACCOUNT_SID, _AUTH_TOKEN)


def send_sms(to: str, body: str) -> str | None:
    """Sends an SMS and returns the Twilio message SID, or None if Twilio
    isn't configured yet (so local dev doesn't crash without credentials)."""
    if not _client or not _FROM_NUMBER:
        print(f"[twilio disabled — no credentials] would send to {to}: {body}")
        return None

    message = _client.messages.create(to=to, from_=_FROM_NUMBER, body=body)
    return message.sid
