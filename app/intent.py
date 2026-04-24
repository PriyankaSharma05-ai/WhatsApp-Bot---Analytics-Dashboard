import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)

SYSTEM_PROMPT = """You are an intent classifier for Hawkins Cookers Limited's WhatsApp chatbot.
Classify the user's message into exactly one of these intents:

- greeting: Hello, hi, start, help, menu, welcome messages
- product_query: Questions about buying products, product recommendations, prices, specifications,
  which cooker to buy, capacity questions, induction compatibility
- recipe_help: Cooking recipes, how to cook something, cooking tips, cook times, pressure cooker recipes
- warranty_claim: Warranty issues, product complaints, defects, repair requests, damaged product
- order_tracking: Order status, delivery tracking, where is my order, shipping
- fallback: Anything else, complaints, unclear messages, out-of-scope

Also extract key entities:
- capacity: numeric value in liters if mentioned (e.g., "5 liter" -> 5)
- material: aluminium, stainless_steel, hard_anodised if mentioned
- induction: true/false if induction compatibility is mentioned
- model: model number if mentioned (e.g., "A10", "Futura")

Respond ONLY with valid JSON, no other text:
{
  "intent": "<intent_name>",
  "confidence": <0.0 to 1.0>,
  "entities": {
    "capacity": null or number,
    "material": null or string,
    "induction": null or boolean,
    "model": null or string
  }
}"""


def classify_intent(message: str, session: dict) -> tuple[str, float]:
    """Classify user intent using Google Gemini (free). Returns (intent, confidence)."""

    context = ""
    if session.get("last_intent"):
        context = f"\nPrevious intent: {session['last_intent']}"
    if session.get("warranty_step"):
        context += f"\nIn warranty flow, step: {session['warranty_step']}"

    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set — using rule-based fallback")
        return _rule_based_fallback(message), 0.5

    try:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{SYSTEM_PROMPT}\n\nMessage: {message}{context}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 200,
            },
        }

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Strip markdown code fences if Gemini wraps in ```json
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)

        intent = result.get("intent", "fallback")
        confidence = float(result.get("confidence", 0.5))

        entities = result.get("entities", {})
        if entities:
            session["entities"] = entities

        logger.info(f"Intent: {intent} ({confidence:.2f}) for: {message[:50]}")
        return intent, confidence

    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error in intent: {e}")
        return _rule_based_fallback(message), 0.5
    except Exception as e:
        logger.error(f"Gemini intent error: {e}")
        return _rule_based_fallback(message), 0.5


def _rule_based_fallback(message: str) -> str:
    """Simple keyword-based fallback if AI is unavailable."""
    msg = message.lower()

    greetings = ["hello", "hi", "hey", "start", "help", "menu", "namaste", "namaskar"]
    warranty_kw = ["warranty", "complaint", "broken", "defect", "repair", "damage",
                   "problem", "issue", "kharab", "toota"]
    order_kw = ["order", "delivery", "track", "shipping", "dispatch", "kahan hai"]
    product_kw = ["buy", "price", "purchase", "recommend", "suggest", "which cooker",
                  "show me", "want a", "need a", "liter", "litre", "induction",
                  "aluminium", "steel", "capacity", "kharidna", "kitne ka"]
    recipe_kw = ["recipe", "cook", "dal", "rice", "khichdi", "biryani", "how to make",
                 "banana", "pakana", "kaise banaye", "banane"]

    if any(w in msg for w in greetings):
        return "greeting"
    if any(w in msg for w in warranty_kw):
        return "warranty_claim"
    if any(w in msg for w in order_kw):
        return "order_tracking"
    if any(w in msg for w in product_kw):
        return "product_query"
    if any(w in msg for w in recipe_kw):
        return "recipe_help"
    return "fallback"
