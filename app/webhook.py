from flask import Blueprint, request, current_app
from twilio.twiml.messaging_response import MessagingResponse
from app.intent import classify_intent
from app.session import get_session, save_session
from app.language import detect_language
from app.models import Conversation, User, db
from app.handlers.product import handle_product
from app.handlers.recipe import handle_recipe
from app.handlers.warranty import handle_warranty
from app.handlers.order import handle_order
from app.handlers.greeting import handle_greeting
from app.handlers.fallback import handle_fallback
from datetime import datetime
import logging

bp = Blueprint("webhook", __name__)
logger = logging.getLogger(__name__)


@bp.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip()
    from_number = request.form.get("From", "")

    if not incoming_msg or not from_number:
        return "Bad Request", 400

    logger.info(f"Received from {from_number}: {incoming_msg}")

    # Load or create session
    session = get_session(from_number)

    # Detect language
    lang = detect_language(incoming_msg)
    session["lang"] = lang

    # Update/create user record
    _update_user(from_number, lang)

    # Classify intent
    intent, confidence = classify_intent(incoming_msg, session)
    session["last_intent"] = intent
    session["turn"] = session.get("turn", 0) + 1

    # Route to handler
    reply = _route(intent, incoming_msg, session, from_number)

    # Save session
    save_session(from_number, session)

    # Log conversation
    _log_conversation(from_number, incoming_msg, reply, intent, lang)

    # Send WhatsApp reply
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)


def _route(intent, msg, session, phone):
    handlers = {
        "greeting": handle_greeting,
        "product_query": handle_product,
        "recipe_help": handle_recipe,
        "warranty_claim": handle_warranty,
        "order_tracking": handle_order,
        "fallback": handle_fallback,
    }
    handler = handlers.get(intent, handle_fallback)
    return handler(msg, session, phone)


def _update_user(phone, lang):
    try:
        user = User.query.filter_by(phone=phone).first()
        if not user:
            user = User(phone=phone, language_pref=lang)
            db.session.add(user)
        else:
            user.last_seen = datetime.utcnow()
            user.total_messages = (user.total_messages or 0) + 1
            if lang != "en":
                user.language_pref = lang
        db.session.commit()
    except Exception as e:
        logger.error(f"User update error: {e}")
        db.session.rollback()


def _log_conversation(phone, user_msg, bot_reply, intent, lang):
    try:
        conv = Conversation(
            phone=phone,
            user_message=user_msg,
            bot_response=bot_reply,
            intent=intent,
            language=lang,
            resolved=(intent != "fallback"),
        )
        db.session.add(conv)
        db.session.commit()
    except Exception as e:
        logger.error(f"Logging error: {e}")
        db.session.rollback()


@bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "Hawkins WhatsApp Bot"}, 200
