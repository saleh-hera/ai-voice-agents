#!/usr/bin/env python3
"""
sync_to_stripe.py
------------------
Create the AI Digital Dealer module + tier Stripe Products/Prices from
scripts/modules_pricing.json, instead of clicking through the Stripe
Dashboard 50+ times by hand.

Mirrors the sync_to_vapi.py pattern: config lives in a version-controlled
file, this script pushes it to the live platform.

Safety:
    - Runs as a DRY RUN by default. Nothing is created until you pass --apply.
    - Idempotent: every Product/Price this script creates is tagged with
      metadata {"source": "ai-digital-dealer-sync"}. Re-running with --apply
      skips anything already created (matched by metadata.module_id or
      metadata.tier_setup_fee) instead of making duplicates.
    - Only ever CREATES. Never archives, deletes, or modifies your existing
      products (e.g. the old per-agent Bella/Nova Sales/Nova Support prices,
      or the unrelated JobAgent products) — do that yourself in the
      Dashboard first, as you already have.

Usage:
    1. pip install -r requirements.txt
    2. Copy .env.example to .env and add STRIPE_SECRET_KEY (starts with sk_live_ or sk_test_)
    3. python sync_to_stripe.py            # dry run — prints what WOULD be created
       python sync_to_stripe.py --apply    # actually creates Products/Prices in Stripe

Get your Stripe secret key from: https://dashboard.stripe.com/apikeys
"""

import os
import sys
import json
import argparse
from pathlib import Path

import stripe
from dotenv import load_dotenv

load_dotenv()

# Windows consoles default to cp1252, which can't print the arrows/em-dashes
# used below — force UTF-8 stdout so this doesn't crash mid-way through --apply.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
DATA_FILE = Path(__file__).resolve().parent / "modules_pricing.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "stripe_price_ids.json"
SOURCE_TAG = "ai-digital-dealer-sync"


def load_data() -> dict:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def all_modules(data: dict) -> list[dict]:
    seen = {}
    for stage in data["stages"]:
        for m in stage["modules"]:
            seen.setdefault(m["id"], {**m, "stage": stage["name"]})
    return list(seen.values())


def find_existing_price(metadata_key: str, metadata_value: str):
    """Search existing Prices (not just Products) for one already tagged
    with this module/tier, so re-running the script never duplicates."""
    for price in stripe.Price.list(limit=100, expand=["data.product"]).auto_paging_iter():
        product = price.product
        if isinstance(product, str):
            continue
        meta = product.metadata.to_dict()  # StripeObject has no .get(); to_dict() gives a plain dict
        if meta.get(metadata_key) == metadata_value and meta.get("source") == SOURCE_TAG:
            return price
    return None


def create_module_price(module: dict, currency: str, apply: bool):
    existing = find_existing_price("module_id", module["id"])
    if existing:
        print(f"  = skip '{module['name']}' — already exists (price {existing.id})")
        return existing.id if existing else None

    label = f"[DRY RUN] would create" if not apply else "→ creating"
    print(f"  {label} '{module['name']}' — ${module['price']}/mo")

    if not apply:
        return None

    product = stripe.Product.create(
        name=module["name"],
        metadata={"source": SOURCE_TAG, "module_id": module["id"], "stage": module.get("stage", "")},
    )
    price = stripe.Price.create(
        product=product.id,
        unit_amount=module["price"] * 100,
        currency=currency,
        recurring={"interval": "month"},
    )
    print(f"    ✅ created product {product.id} / price {price.id}")
    return price.id


def create_setup_fee_price(tier: dict, currency: str, apply: bool):
    tier_key = tier["name"].lower().replace(" ", "_")
    existing = find_existing_price("tier_setup_fee", tier_key)
    if existing:
        print(f"  = skip '{tier['name']} setup fee' — already exists (price {existing.id})")
        return existing.id if existing else None

    label = "[DRY RUN] would create" if not apply else "→ creating"
    print(f"  {label} '{tier['name']} — One-Time Setup Fee' — ${tier['setupFee']} one-time")

    if not apply:
        return None

    product = stripe.Product.create(
        name=f"{tier['name']} — One-Time Setup Fee",
        metadata={"source": SOURCE_TAG, "tier_setup_fee": tier_key},
    )
    price = stripe.Price.create(
        product=product.id,
        unit_amount=tier["setupFee"] * 100,
        currency=currency,
    )
    print(f"    ✅ created product {product.id} / price {price.id}")
    return price.id


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="Actually create Products/Prices in Stripe (default: dry run)")
    args = parser.parse_args()

    if not STRIPE_SECRET_KEY:
        sys.exit("❌ Missing STRIPE_SECRET_KEY. Copy .env.example to .env and add your key.")
    stripe.api_key = STRIPE_SECRET_KEY

    if not args.apply:
        print("=== DRY RUN — nothing will be created. Re-run with --apply to actually push to Stripe. ===\n")
    else:
        mode = "LIVE" if STRIPE_SECRET_KEY.startswith("sk_live_") else "TEST"
        print(f"=== APPLYING to Stripe in {mode} mode ===\n")

    data = load_data()
    modules = all_modules(data)
    result = {"modules": {}, "tiers": {}}

    print(f"Base agent + {len(modules) - 1} add-on modules:")
    for m in modules:
        price_id = create_module_price(m, data["currency"], args.apply)
        if price_id:
            result["modules"][m["id"]] = price_id

    print("\nOne-time setup fees per tier:")
    for tier in data["tiers"]:
        price_id = create_setup_fee_price(tier, data["currency"], args.apply)
        if price_id:
            result["tiers"][tier["name"]] = price_id

    if args.apply:
        OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"\n✅ Saved created price IDs to {OUTPUT_FILE}")
    else:
        print("\nNo file written (dry run). Run with --apply when ready.")


if __name__ == "__main__":
    main()
