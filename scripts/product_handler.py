#!/usr/bin/env python3
"""
Shayne's AI Lab — Stripe Product Handler
FastAPI server that handles checkout session creation and webhook-based delivery.

Run: python3 scripts/product_handler.py
Port: 8093
Tunnel: api.shaynesailab.com/checkout -> localhost:8093
        api.shaynesailab.com/webhook/stripe -> localhost:8093
"""

import os
import sys
import json
import base64
import logging
from datetime import datetime, timezone
from pathlib import Path

import stripe
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_DIR = BASE_DIR / "products"
DATA_DIR = PRODUCTS_DIR / "data"
ORDERS_FILE = DATA_DIR / "orders.json"
PRODUCT_MAP = PRODUCTS_DIR / "product_map.json"
BLUEPRINTS_DIR = BASE_DIR.parent / "scripts" / "products" / "blueprints"
GUIDES_DIR = BASE_DIR.parent / "scripts" / "products" / "guides"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("stripe_handler")

# ─── Config ──────────────────────────────────────────────────────────────────
def get_env(key):
    """Load key from environment, then from product_handler.env, then chipradar.env"""
    val = os.environ.get(key)
    if val:
        return val
    # Check product_handler.env
    env_file = BASE_DIR / "product_handler.env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1].strip("'\" ")
    # Fallback to chipradar.env (shared Stripe account)
    chip_env = Path.home() / ".openclaw" / "credentials" / "chipradar.env"
    if chip_env.exists():
        with open(chip_env) as f:
            for line in f:
                line = line.strip().replace("export ", "")
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1].strip("'\" ")
    return None

STRIPE_SECRET_KEY = get_env("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = get_env("STRIPE_WEBHOOK_SECRET")
AGENTMAIL_API_KEY = get_env("AGENTMAIL_API_KEY")

if not STRIPE_SECRET_KEY:
    log.error("STRIPE_SECRET_KEY not set")
    sys.exit(1)
if not STRIPE_WEBHOOK_SECRET:
    log.error("STRIPE_WEBHOOK_SECRET not set")
    sys.exit(1)

stripe.api_key = STRIPE_SECRET_KEY

# ─── Product Catalog ─────────────────────────────────────────────────────────
def load_products():
    """Load product map from Stripe (authoritative source)"""
    if PRODUCT_MAP.exists():
        with open(PRODUCT_MAP) as f:
            return json.load(f)
    return {}

PRODUCTS = load_products()

# Friendly product key lookup by Stripe product ID
PRODUCT_BY_STRIPE_ID = {}
for key, p in PRODUCTS.items():
    sid = p.get("stripe_id")
    if sid:
        PRODUCT_BY_STRIPE_ID[sid] = key

# Product names (for display)
PRODUCT_NAMES = {
    "email-triage-blueprint": "Email Triage Blueprint",
    "lead-capture-blueprint": "Lead Capture Blueprint",
    "invoice-followup-blueprint": "Invoice Follow-Up Blueprint",
    "automation-bundle": "The Automation Bundle",
    "inbox-workshop": "Build Your Inbox Workshop",
}

# Bundle definitions (what files to include)
BUNDLE_CONTENTS = {
    "automation-bundle": ["email-triage-blueprint", "lead-capture-blueprint", "invoice-followup-blueprint"],
    "inbox-workshop": ["email-triage-blueprint", "lead-capture-blueprint", "invoice-followup-blueprint"],
}

# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(title="ShayneSAI Lab Products", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shaynesailab.com", "http://localhost:8080"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Stripe-Signature"],
)

# ─── Models ──────────────────────────────────────────────────────────────────
class CheckoutRequest(BaseModel):
    product: str  # e.g., "email-triage-blueprint"

# ─── Endpoints ───────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "products": list(PRODUCTS.keys())}

@app.post("/checkout")
async def create_checkout(req: CheckoutRequest):
    """Create a Stripe Checkout Session and return the redirect URL."""
    product_key = req.product.strip().lower()
    
    if product_key not in PRODUCTS:
        raise HTTPException(status_code=400, detail=f"Unknown product: {product_key}")
    
    product = PRODUCTS[product_key]
    price_id = product.get("stripe_price_id")
    
    if price_id:
        # Use pre-created price
        line_items = [{"price": price_id, "quantity": 1}]
    else:
        # Create price on the fly
        line_items = [{
            "price_data": {
                "currency": "usd",
                "product": product["stripe_id"],
                "unit_amount": product["price"],
            },
            "quantity": 1,
        }]
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="https://shaynesailab.com/products/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://shaynesailab.com/products/",
            metadata={"product_key": product_key},
        )
        log.info(f"Checkout created: {product_key} -> {session.id}")
        return {"url": session.url}
    except stripe.error.StripeError as e:
        log.error(f"Stripe error: {e}")
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe payment completion webhook and deliver product."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_checkout_completed(session)
    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
        await handle_checkout_completed(session)
    
    return {"received": True}


async def handle_checkout_completed(session):
    """Process a completed payment and deliver the product via email."""
    customer_email = session.get("customer_details", {}).get("email")
    product_key = session.get("metadata", {}).get("product_key", "")
    session_id = session.get("id", "")
    
    if not customer_email or not product_key:
        log.warning(f"Missing email or product_key in session {session_id}")
        return
    
    # Record the order
    record_order(session_id, product_key, customer_email, session["amount_total"])
    
    # Get the product files to deliver
    product_name = PRODUCT_NAMES.get(product_key, product_key.replace("-", " ").title())
    
    # Build the delivery email
    subject = f"Your {product_name} — Shayne's AI Lab"
    text = build_delivery_email(product_key, customer_email, product_name)
    attachments = build_attachments(product_key)
    
    # Send via AgentMail
    try:
        send_product_email(customer_email, subject, text, attachments)
        log.info(f"Delivered {product_key} to {customer_email}")
    except Exception as e:
        log.error(f"Delivery failed for {customer_email}: {e}")


def build_delivery_email(product_key, customer_email, product_name):
    """Build the email body for a product delivery."""
    lines = [
        f"Thanks for your purchase, {customer_email.split('@')[0]}!",
        "",
        f"Your {product_name} is ready.",
        "",
        "WHAT'S INCLUDED",
        "---------------",
    ]
    
    if product_key in BUNDLE_CONTENTS:
        for sub in BUNDLE_CONTENTS[product_key]:
            pn = PRODUCT_NAMES.get(sub, sub)
            lines.append(f"  * {pn} — blueprint JSON + setup guide")
    else:
        lines.append(f"  * {product_name} — blueprint JSON + setup guide")
    
    lines.extend([
        "",
        "BLUEPRINT SETUP",
        "---------------",
        "1. Open Make.com and create a new scenario",
        "2. Click the menu (...) and select 'Import Blueprint'",
        "3. Upload the attached JSON file",
        "4. Follow the setup guide for each module's API keys",
        "",
        "Your download links are included in the attached files.",
        "Save them somewhere accessible.",
        "",
        "NEED HELP?",
        "----------",
        "Reply to this email and I'll help you get it running.",
        "",
        "— Shayne",
        "Shayne's AI Lab",
        "https://shaynesailab.com",
    ])
    return "\n".join(lines)


def build_attachments(product_key):
    """Build attachment list for the product."""
    attachments = []
    
    # Files to include
    files_to_include = [product_key]
    if product_key in BUNDLE_CONTENTS:
        files_to_include = BUNDLE_CONTENTS[product_key]
    
    for key in files_to_include:
        # Blueprint JSON
        bp_file = BLUEPRINTS_DIR / f"{key}.json"
        if bp_file.exists():
            with open(bp_file, "rb") as f:
                content_b64 = base64.b64encode(f.read()).decode()
            attachments.append({
                "filename": f"{key}.json",
                "content_type": "application/json",
                "content": content_b64,
            })
        
        # Setup guide
        guide_file = GUIDES_DIR / f"{key}.md"
        if guide_file.exists():
            with open(guide_file, "rb") as f:
                content_b64 = base64.b64encode(f.read()).decode()
            attachments.append({
                "filename": f"{key}-setup-guide.md",
                "content_type": "text/markdown",
                "content": content_b64,
            })
    
    return attachments


def send_product_email(to_email, subject, text, attachments=None):
    """Send product delivery email via AgentMail SDK."""
    from agentmail import AgentMail
    
    client = AgentMail(api_key=AGENTMAIL_API_KEY)
    
    kwargs = {
        "inbox_id": "revenueclaw@agentmail.to",
        "to": to_email,
        "subject": subject,
        "text": text,
    }
    if attachments:
        kwargs["attachments"] = attachments
    
    result = client.inboxes.messages.send(**kwargs)
    log.info(f"Email sent to {to_email}: {result.message_id}")
    return result


def record_order(session_id, product_key, email, amount):
    """Record a completed order to orders.json."""
    orders = []
    if ORDERS_FILE.exists():
        try:
            with open(ORDERS_FILE) as f:
                orders = json.load(f)
        except (json.JSONDecodeError, IOError):
            orders = []
    
    orders.append({
        "session_id": session_id,
        "product_key": product_key,
        "email": email,
        "amount": amount,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "delivered": True,
    })
    
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)


# ─── Storage for price IDs after first creation ────────────────────────────
def save_price_ids():
    """After first successful checkout, capture the price IDs."""
    for key, product in PRODUCTS.items():
        if "stripe_price_id" not in product:
            # Fetch the price from Stripe
            prod_id = product.get("stripe_id")
            if prod_id:
                prices = stripe.Price.list(product=prod_id, limit=1)
                if prices.data:
                    product["stripe_price_id"] = prices.data[0].id
    
    with open(PRODUCT_MAP, "w") as f:
        json.dump(PRODUCTS, f, indent=2)


# ─── Startup ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    if not AGENTMAIL_API_KEY:
        log.warning("AGENTMAIL_API_KEY not set — email delivery will fail")
    else:
        log.info(f"AgentMail configured")
    
    try:
        acct = stripe.Account.retrieve()
        log.info(f"Stripe account: {acct.id}")
    except Exception as e:
        log.error(f"Stripe connection failed: {e}")
        sys.exit(1)
    
    try:
        save_price_ids()
    except Exception:
        pass  # Non-critical
    
    log.info(f"Product handler ready. {len(PRODUCTS)} products loaded.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093, log_level="info")