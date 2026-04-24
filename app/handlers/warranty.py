import random
import string
import logging
from app.language import get_text
from app.models import WarrantyClaim, db

logger = logging.getLogger(__name__)


def handle_warranty(msg: str, session: dict, phone: str) -> str:
    lang = session.get("lang", "en")
    step = session.get("warranty_step", None)

    if step is None:
        # Start warranty flow
        session["warranty_step"] = "model"
        session["warranty_data"] = {}
        return get_text("warranty_start", lang)

    elif step == "model":
        session["warranty_data"]["model_no"] = msg.strip()
        session["warranty_step"] = "date"
        return get_text("warranty_date", lang)

    elif step == "date":
        session["warranty_data"]["purchase_date"] = msg.strip()
        session["warranty_step"] = "complaint"
        return get_text("warranty_complaint", lang)

    elif step == "complaint":
        session["warranty_data"]["complaint"] = msg.strip()
        ticket_id = _generate_ticket_id()

        # Save to DB
        try:
            claim = WarrantyClaim(
                phone=phone,
                model_no=session["warranty_data"].get("model_no", "Unknown"),
                purchase_date=session["warranty_data"].get("purchase_date", "Unknown"),
                complaint=session["warranty_data"].get("complaint", ""),
                ticket_id=ticket_id,
                status="open",
            )
            db.session.add(claim)
            db.session.commit()
        except Exception as e:
            logger.error(f"Warranty DB error: {e}")
            db.session.rollback()

        # Clear warranty flow from session
        session.pop("warranty_step", None)
        session.pop("warranty_data", None)

        return get_text("warranty_done", lang, ticket_id=ticket_id)

    # Unexpected state — restart
    session.pop("warranty_step", None)
    return handle_warranty(msg, session, phone)


def _generate_ticket_id() -> str:
    prefix = "HWK"
    suffix = "".join(random.choices(string.digits, k=6))
    return f"{prefix}{suffix}"
