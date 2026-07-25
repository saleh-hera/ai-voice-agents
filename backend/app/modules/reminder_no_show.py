from app.config_loader import module_setting
from app.integrations.twilio_client import send_sms
from app.models import Client, Lead


def run(client: Client, lead: Lead) -> None:
    """Called by the scheduler (app/scheduler.py), not by the live webhook —
    reminders fire on a time offset before the appointment, not on a call event."""
    if not lead.caller_phone or not lead.appointment_time or lead.reminder_sent:
        return

    reschedule_link = module_setting(client, "reminderNoShow", "rescheduleLink", default="")
    when = lead.appointment_time.strftime("%A at %-I:%M%p")
    body = f"Reminder: your appointment at {client.name} is {when}."
    if reschedule_link:
        body += f" Reply R to reschedule: {reschedule_link}"

    send_sms(to=lead.caller_phone, body=body)
    lead.reminder_sent = True
