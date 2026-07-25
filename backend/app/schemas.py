from pydantic import BaseModel


class ModuleSetting(BaseModel):
    enabled: bool = False


class ClientCreate(BaseModel):
    id: str
    name: str
    industry: str
    phone: str
    email: str | None = None
    timezone: str = "America/Los_Angeles"
    business_data: dict = {}
    modules: dict[str, ModuleSetting] = {}
    integrations: dict = {}
    tier: str = "starter"
    monthly_price_usd: int = 0


class ClientOut(ClientCreate):
    status: str

    class Config:
        from_attributes = True


class VapiWebhookPayload(BaseModel):
    """Minimal shape we actually read from Vapi's call-event webhook.
    Extend as needed once wired to a real Vapi assistant — see Vapi's
    server-webhook docs for the full event schema.
    """

    client_id: str
    event_type: str  # e.g. "call.ended", "call.missed"
    call_status: str | None = None
    caller_name: str | None = None
    caller_phone: str | None = None
    appointment_booked: bool = False
    appointment_time: str | None = None
    transcript_summary: str | None = None
