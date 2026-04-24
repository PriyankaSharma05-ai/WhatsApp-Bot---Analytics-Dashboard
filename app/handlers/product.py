from app.models import Product
from app.language import get_text
import logging

logger = logging.getLogger(__name__)


def handle_product(msg: str, session: dict, phone: str) -> str:
    lang = session.get("lang", "en")
    entities = session.get("entities", {})

    # Build query
    query = Product.query.filter_by(in_stock=True)

    capacity = entities.get("capacity")
    material = entities.get("material")
    induction = entities.get("induction")
    model = entities.get("model")

    msg_lower = msg.lower()

    # Parse from message if entities not extracted
    if not capacity:
        import re
        cap_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:l|ltr|liter|litre|L)', msg, re.IGNORECASE)
        if cap_match:
            capacity = float(cap_match.group(1))

    if not induction:
        induction_kw = ["induction", "induction compatible", "induction base", "inducton"]
        if any(k in msg_lower for k in induction_kw):
            induction = True

    if not material:
        if any(w in msg_lower for w in ["aluminium", "aluminum", "alloy"]):
            material = "aluminium"
        elif any(w in msg_lower for w in ["stainless", "steel", "ss"]):
            material = "stainless_steel"
        elif any(w in msg_lower for w in ["hard anodised", "hard anodized", "anodised"]):
            material = "hard_anodised"

    # Budget filter
    budget = None
    import re
    budget_match = re.search(r'(?:under|below|less than|within|budget|rs\.?|₹)\s*(\d+)', msg_lower)
    if budget_match:
        budget = float(budget_match.group(1))

    # Apply filters
    if capacity:
        query = query.filter(Product.capacity_liters == capacity)
    if material:
        query = query.filter(Product.material == material)
    if induction is True:
        query = query.filter(Product.induction_compatible == True)
    if budget:
        query = query.filter(Product.price <= budget)

    # Category filter
    if any(w in msg_lower for w in ["cookware", "pan", "kadai", "tawa"]):
        query = query.filter(Product.category == "cookware")
    elif any(w in msg_lower for w in ["pressure cooker", "cooker", "prestige"]):
        query = query.filter(Product.category == "pressure_cooker")

    products = query.limit(3).all()

    if not products:
        # Try broader search
        products = Product.query.filter_by(in_stock=True).limit(3).all()
        if not products:
            return get_text("product_none", lang)

    formatted = _format_products(products, lang)
    return get_text("product_found", lang, products=formatted)


def _format_products(products, lang):
    lines = []
    for i, p in enumerate(products, 1):
        induction_tag = " | ⚡ Induction" if p.induction_compatible else ""
        price_str = f"₹{p.price:,.0f}" if p.price else "Price on request"
        lines.append(
            f"*{i}. {p.name}*\n"
            f"   📦 {p.capacity_liters}L | {p.material.replace('_', ' ').title()}{induction_tag}\n"
            f"   💰 {price_str}\n"
            f"   🛒 {p.buy_url or 'www.hawkinscookers.com'}"
        )
    return "\n\n".join(lines)
