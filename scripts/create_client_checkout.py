#!/usr/bin/env python3
"""
create_client_checkout.py
--------------------------
Generate a Stripe Checkout link for a client, built from the base Sales
Agent plus whichever add-on modules they picked (Starter = base only,
Growth = 2-4 modules, Total Solution = 5+), matching the tier logic in the
pricing artifact and clients/schemas/customer-config.schema.json.

Important Stripe limitation this script works around:
    A subscription-mode Checkout Session can only put a free trial on the
    RECURRING line items. A one-time price (the tier's setup fee) included
    in the same session gets charged immediately at checkout — not after
    the trial — which would contradict "setup fee billed after your trial
    converts" on the website/terms page. So this script:
      1. Creates the Checkout Session with ONLY the recurring prices
         (base agent + selected modules), with a 7-day trial.
      2. Does NOT charge the setup fee at checkout.
      3. Prints the setup fee amount + a reminder to invoice it separately
         once the trial converts (Stripe Dashboard: Customer -> Add invoice
         item, or a follow-up webhook-driven script if this becomes
         frequent enough to automate).

Usage:
    python create_client_checkout.py --modules missedCallRecovery,reminderNoShow --customer-email someone@business.com
    python create_client_checkout.py --modules "" --customer-email someone@business.com   # Starter, base only

Requires STRIPE_SECRET_KEY in .env (same as sync_to_stripe.py).
"""

import os
import sys
import json
import argparse
from pathlib import Path

import stripe
from dotenv import load_dotenv

load_dotenv()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
SCRIPT_DIR = Path(__file__).resolve().parent
PRICE_IDS_FILE = SCRIPT_DIR / "stripe_price_ids.json"
PRICING_DATA_FILE = SCRIPT_DIR / "modules_pricing.json"
BASE_MODULE_ID = "voiceAgent"
TRIAL_DAYS = 7


def load_json(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"❌ Missing {path.name} — run sync_to_stripe.py --apply first.")
    return json.loads(path.read_text(encoding="utf-8"))


def tier_for_count(non_required_count: int) -> str:
    """Same thresholds as the pricing artifact's tierForCount()."""
    if non_required_count == 0:
        return "Starter"
    if non_required_count <= 4:
        return "Growth"
    return "Total Solution"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--modules", default="", help="Comma-separated add-on module IDs (base agent is always included). Empty = Starter tier.")
    parser.add_argument("--customer-email", required=True, help="Prefills the client's email at checkout")
    parser.add_argument("--business-name", default="", help="Optional label stored in Checkout Session metadata")
    args = parser.parse_args()

    if not STRIPE_SECRET_KEY:
        sys.exit("❌ Missing STRIPE_SECRET_KEY. Copy .env.example to .env and add your key.")
    stripe.api_key = STRIPE_SECRET_KEY

    price_ids = load_json(PRICE_IDS_FILE)
    pricing_data = load_json(PRICING_DATA_FILE)

    module_ids = [m.strip() for m in args.modules.split(",") if m.strip()]
    unknown = [m for m in module_ids if m not in price_ids["modules"]]
    if unknown:
        sys.exit(f"❌ Unknown module id(s): {', '.join(unknown)} — check modules_pricing.json for valid ids.")

    tier_name = tier_for_count(len(module_ids))
    tier_info = next(t for t in pricing_data["tiers"] if t["name"] == tier_name)
    setup_fee = tier_info["setupFee"]

    # Base agent + every selected module, one line item each, qty 1.
    line_items = [{"price": price_ids["modules"][BASE_MODULE_ID], "quantity": 1}]
    for mod_id in module_ids:
        line_items.append({"price": price_ids["modules"][mod_id], "quantity": 1})

    mode = "LIVE" if STRIPE_SECRET_KEY.startswith("sk_live_") else "TEST"
    print(f"=== Creating Checkout Session in {mode} mode ===")
    print(f"Tier: {tier_name}  ({len(module_ids)} add-on module(s))")
    print(f"Recurring total: base $399/mo + {len(module_ids)} module(s)\n")

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=line_items,
        customer_email=args.customer_email,
        subscription_data={
            "trial_period_days": TRIAL_DAYS,
            "metadata": {
                "tier": tier_name,
                "business_name": args.business_name,
                "setup_fee_due_usd": str(setup_fee),
                "setup_fee_invoiced": "false",
            },
        },
        success_url="https://aiagentsvault.tech/talk-to-sales?checkout=success",
        cancel_url="https://aiagentsvault.tech/talk-to-sales?checkout=cancelled",
    )

    print(f"✅ Checkout link ({tier_name}):\n{session.url}\n")
    print(f"⚠️  Setup fee NOT included in this link — bill ${setup_fee} separately")
    print(f"   once the trial converts (Stripe Dashboard -> Customer -> Add invoice item,")
    print(f"   or track subscription_data.metadata.setup_fee_due_usd via webhook).")


if __name__ == "__main__":
    main()
