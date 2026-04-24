import json
import os
import re
import logging
from app.language import get_text

logger = logging.getLogger(__name__)

# Load recipes from JSON file
_recipes = None


def _load_recipes():
    global _recipes
    if _recipes is None:
        path = os.path.join(os.path.dirname(__file__), "../../data/recipes.json")
        try:
            with open(path) as f:
                _recipes = json.load(f)
        except Exception as e:
            logger.error(f"Could not load recipes: {e}")
            _recipes = {}
    return _recipes


def handle_recipe(msg: str, session: dict, phone: str) -> str:
    lang = session.get("lang", "en")
    recipes = _load_recipes()
    msg_lower = msg.lower()

    # Find matching recipe
    matched = None
    for key, recipe in recipes.items():
        aliases = recipe.get("aliases", [key])
        if any(alias in msg_lower for alias in aliases):
            matched = recipe
            break

    if not matched:
        # Default: show popular recipes
        popular = list(recipes.values())[:5]
        names = ", ".join([r["name"] for r in popular])
        return (
            f"👩‍🍳 I can help you with Hawkins pressure cooker recipes!\n\n"
            f"Popular recipes: *{names}*\n\n"
            f"Just ask me: 'How to cook dal' or 'Rice recipe' or 'Biryani in pressure cooker'"
        )

    steps_text = _format_steps(matched.get("steps", []), lang)
    return get_text("recipe_intro", lang,
                    dish=matched["name"],
                    steps=steps_text,
                    time=matched.get("total_time", "30 mins"))


def _format_steps(steps, lang):
    if not steps:
        return "Steps not available."
    return "\n".join(f"{i}. {step}" for i, step in enumerate(steps, 1))
