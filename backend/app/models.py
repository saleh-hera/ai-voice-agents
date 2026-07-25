import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Client(Base):
    """One row per business — mirrors clients/schemas/customer-config.schema.json"""

    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g. "abc-dental-2026"
    name: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    timezone: Mapped[str] = mapped_column(String, default="America/Los_Angeles")

    # Free-form business data (services, faq, hours) — matches schema's "business" object
    business_data: Mapped[dict] = mapped_column(JSON, default=dict)

    # Module on/off + settings — matches schema's "modules" object, e.g.
    # {"voiceAgent": {"enabled": true, "assistantId": "..."}, "missedCallRecovery": {"enabled": true, ...}}
    modules: Mapped[dict] = mapped_column(JSON, default=dict)

    # Integration settings (twilio numbers, calendar ids, etc.)
    integrations: Mapped[dict] = mapped_column(JSON, default=dict)

    tier: Mapped[str] = mapped_column(String, default="starter")
    monthly_price_usd: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String, default="trial")  # trial | active | paused | cancelled

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    leads: Mapped[list["Lead"]] = relationship(back_populates="client")


class Lead(Base):
    """One row per call/chat/lead event — what modules read/act on."""

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"))

    caller_name: Mapped[str | None] = mapped_column(String, nullable=True)
    caller_phone: Mapped[str | None] = mapped_column(String, nullable=True)

    source: Mapped[str] = mapped_column(String, default="voice_call")  # voice_call | web_chat | ad_form
    call_status: Mapped[str] = mapped_column(String, default="completed")  # completed | missed | voicemail

    status: Mapped[str] = mapped_column(
        String, default="new"
    )  # new | qualified | booked | no_show | follow_up_required | cold

    appointment_time: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    reminder_sent: Mapped[bool] = mapped_column(default=False)

    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    client: Mapped["Client"] = relationship(back_populates="leads")
