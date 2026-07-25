import datetime
import os

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config_loader import is_enabled
from app.database import get_db
from app.integrations.notify import notify_owner
from app.models import Client, Lead
from app.modules.registry import LIVE_EVENT_MODULES
from app.schemas import VapiWebhookPayload

router = APIRouter()

_WEBHOOK_SECRET = os.getenv("VAPI_WEBHOOK_SECRET")


def _parse_appointment_time(value: str | None) -> datetime.datetime | None:
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return None


@router.post("/webhook/vapi")
def vapi_webhook(
    payload: VapiWebhookPayload,
    db: Session = Depends(get_db),
    x_webhook_secret: str | None = Header(default=None),
):
    if _WEBHOOK_SECRET and x_webhook_secret != _WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="bad webhook secret")

    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail=f"unknown client_id: {payload.client_id}")

    lead = Lead(
        client_id=client.id,
        caller_name=payload.caller_name,
        caller_phone=payload.caller_phone,
        call_status=payload.call_status or "completed",
        status="booked" if payload.appointment_booked else "new",
        appointment_time=_parse_appointment_time(payload.appointment_time),
        notes=payload.transcript_summary,
    )
    db.add(lead)
    db.flush()  # gets lead.id without committing yet

    if payload.event_type == "call.missed" and is_enabled(client, "missedCallRecovery"):
        LIVE_EVENT_MODULES["missedCallRecovery"](client, lead)

    if payload.appointment_booked:
        notify_owner(
            subject=f"New booking — {client.name}",
            body=f"{lead.caller_name or 'A caller'} ({lead.caller_phone}) just booked via the AI agent.",
        )

    db.commit()
    return {"status": "ok", "lead_id": lead.id}
