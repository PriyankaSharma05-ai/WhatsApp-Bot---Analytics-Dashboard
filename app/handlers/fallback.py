from app.language import get_text


def handle_fallback(msg: str, session: dict, phone: str) -> str:
    lang = session.get("lang", "en")
    turn = session.get("turn", 1)
    consecutive_fallbacks = session.get("consecutive_fallbacks", 0) + 1
    session["consecutive_fallbacks"] = consecutive_fallbacks

    # After 2 consecutive fallbacks, offer human handoff
    if consecutive_fallbacks >= 2:
        session["consecutive_fallbacks"] = 0
        return get_text("human_handoff", lang)

    return get_text("fallback", lang)
