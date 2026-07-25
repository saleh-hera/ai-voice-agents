from app.config_loader import module_setting
from app.integrations.twilio_client import send_sms
from app.models import Client, Lead


def run(client: Client, lead: Lead) -> None:
    if not lead.caller_phone:
        return

    template = module_setting(
        client,
        "missedCallRecovery",
        "template",
        default=f"Sorry we missed your call! This is {client.name} — reply here and we'll help right away.",
    )
    send_sms(to=lead.caller_phone, body=template)
    lead.status = "follow_up_required"
