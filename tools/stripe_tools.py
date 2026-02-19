"""
Stripe API (billing, invoices, customers). Use for invoice and financing agents.
"""
import os
from typing import Any, Dict

try:
    import stripe
except ImportError:
    stripe = None

_API_KEY = os.environ.get("STRIPE_SECRET_KEY", "").strip()
if _API_KEY and stripe:
    stripe.api_key = _API_KEY


def stripe_create_customer(
    email: str,
    name: str | None = None,
    metadata: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """Create a Stripe customer. Returns { ok, customer_id?, error? }."""
    if not _API_KEY or not stripe:
        return {"ok": False, "error": "STRIPE_SECRET_KEY not set or stripe not installed", "stub": True}
    try:
        c = stripe.Customer.create(email=email, name=name or "", metadata=metadata or {})
        return {"ok": True, "customer_id": c.id}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def stripe_create_invoice(
    customer_id: str,
    amount_pence: int,
    currency: str = "gbp",
    description: str | None = None,
) -> Dict[str, Any]:
    """
    Create a Stripe invoice for a customer. amount_pence = amount in smallest unit (e.g. 1000 = £10.00).
    Returns { ok, invoice_id?, url?, error? }.
    """
    if not _API_KEY or not stripe:
        return {"ok": False, "error": "STRIPE_SECRET_KEY not set or stripe not installed", "stub": True}
    try:
        inv = stripe.Invoice.create(customer=customer_id, collection_method="send_invoice", days_until_due=30)
        stripe.InvoiceItem.create(
            customer=customer_id,
            amount=amount_pence,
            currency=currency,
            description=description or "Recruitment fee",
            invoice=inv.id,
        )
        stripe.Invoice.finalize_invoice(inv.id)
        inv = stripe.Invoice.retrieve(inv.id)
        return {"ok": True, "invoice_id": inv.id, "url": getattr(inv, "hosted_invoice_url", None) or ""}
    except Exception as e:
        return {"ok": False, "error": str(e)}
