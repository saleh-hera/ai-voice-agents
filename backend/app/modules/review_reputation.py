from app.config_loader import module_setting
from app.integrations.twilio_client import send_sms
from app.models import Client, Lead


def run(client: Client, lead: Lead) -> None:
    """Called by the scheduler a few hours after a booked appointment's time
    has passed — see app/scheduler.py."""
    if not lead.caller_phone:
        return

    review_link = client.integrations.get("reviewPlatform", {}).get("reviewLink", "")
    body = f"Thanks for visiting {client.name}! Mind leaving us a quick review?"
    if review_link:
        body += f" {review_link}"

    send_sms(to=lead.caller_phone, body=body)
