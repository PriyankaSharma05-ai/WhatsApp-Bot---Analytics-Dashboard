import re
import logging
from app.language import get_text

logger = logging.getLogger(__name__)


def handle_order(msg: str, session: dict, phone: str) -> str:
    lang = session.get("lang", "en")
    step = session.get("order_step", None)

    # Try to extract order ID from message
    order_match = re.search(r'HWK\d+', msg.upper())

    if order_match:
        order_id = order_match.group()
        session.pop("order_step", None)
        # Simulate order lookup (replace with real API in production)
        status, eta = _lookup_order(order_id)
        return get_text("order_info", lang, order_id=order_id, status=status, eta=eta)

    if step is None:
        session["order_step"] = "awaiting_id"
        return get_text("order_prompt", lang)

    # Still waiting for order ID
    return (
        "Please share a valid Hawkins order ID starting with *HWK* "
        "(e.g., HWK123456). You can find it in your order confirmation email."
    )


def _lookup_order(order_id: str) -> tuple[str, str]:
    """
    Simulated order lookup.
    In production: call Hawkins ERP/OMS API here.
    """
    # Mock responses based on last digit
    last = order_id[-1]
    statuses = {
        "0": ("Processing", "3-5 business days"),
        "1": ("Dispatched", "Tomorrow by 6 PM"),
        "2": ("Out for Delivery", "Today by 8 PM"),
        "3": ("Delivered", "Already delivered"),
        "4": ("Processing", "4-6 business days"),
        "5": ("Dispatched", "2-3 business days"),
        "6": ("Out for Delivery", "Today by 9 PM"),
        "7": ("Processing", "3-5 business days"),
        "8": ("Dispatched", "2-4 business days"),
        "9": ("Delivered", "Already delivered"),
    }
    status, eta = statuses.get(last, ("Processing", "3-5 business days"))
    return status, eta
