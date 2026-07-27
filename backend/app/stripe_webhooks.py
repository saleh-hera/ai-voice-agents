"""Auto-bills each client's one-time setup fee when their trial converts.

Why this exists: Stripe won't let a one-time price share a subscription
Checkout Session's trial (it gets charged immediately at checkout instead of
after the trial), so scripts/create_client_checkout.py deliberately leaves
the setup fee out of the initial checkout and stores it as metadata on the
subscription instead (tier, setup_fee_due_usd, setup_fee_invoiced).

This listens for `customer.subscription.trial_will_end` — Stripe fires it
~3 days before a trial ends — and creates a standalone InvoiceItem for the
customer at that point. Stripe automatically folds any pending InvoiceItems
into the customer's next invoice (the first real charge after the trial),
so no extra scheduling logic is needed here.
"""

import os

import stripe
from fastapi import APIRouter, Header, HTTPException, Request

from app.integrations.notify import notify_owner

router = APIRouter()

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, stripe_signature: str | None = Header(default=None)):
    payload = await request.body()

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET not configured")

    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="invalid Stripe webhook signature")

    if event["type"] == "customer.subscription.trial_will_end":
        _handle_trial_will_end(event["data"]["object"])

    return {"status": "ok"}


def _handle_trial_will_end(subscription: dict) -> None:
    metadata = subscription.get("metadata", {})

    if metadata.get("setup_fee_invoiced") == "true":
        return  # already billed — trial_will_end can fire more than once

    setup_fee_due = metadata.get("setup_fee_due_usd")
    if not setup_fee_due:
        return  # not one of our tiered subscriptions (or missing metadata)

    customer_id = subscription["customer"]
    tier = metadata.get("tier", "Unknown tier")
    business_name = metadata.get("business_name", "Unknown business")
    amount_cents = int(float(setup_fee_due) * 100)

    stripe.InvoiceItem.create(
        customer=customer_id,
        amount=amount_cents,
        currency="usd",
        description=f"{tier} — One-Time Setup Fee",
    )

    stripe.Subscription.modify(
        subscription["id"],
        metadata={**metadata, "setup_fee_invoiced": "true"},
    )

    notify_owner(
        subject=f"Setup fee invoiced — {business_name}",
        body=(
            f"${setup_fee_due} {tier} setup fee added as a pending invoice item for "
            f"{business_name} (customer {customer_id}). It'll be included on their "
            f"next invoice when the trial converts."
        ),
    )
