from app.language import get_text
from app.session import clear_session


def handle_greeting(msg: str, session: dict, phone: str) -> str:
    session.clear()  # fresh start
    lang = session.get("lang", "en")
    return get_text("welcome", lang)
