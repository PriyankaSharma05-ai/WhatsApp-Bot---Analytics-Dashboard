import re
import logging

logger = logging.getLogger(__name__)

# Hindi Unicode range: \u0900-\u097F
# Marathi uses same Devanagari script as Hindi but has distinct words
HINDI_WORDS = {"kaise", "kya", "mujhe", "chahiye", "hai", "hain", "nahi", "karo",
               "mera", "meri", "aur", "lekin", "banana", "pakana", "kharidna", "batao",
               "dikhao", "kahan", "kitna", "wala"}
MARATHI_WORDS = {"kasa", "aahe", "mala", "pahije", "karaa", "majha", "majhi",
                 "aani", "banvaycha", "vikat", "sanga", "kuthe", "kiti", "wala"}


def detect_language(text: str) -> str:
    """Detect language: en, hi, or mr."""
    
    # Check for Devanagari script (Hindi/Marathi)
    if re.search(r'[\u0900-\u097F]', text):
        words = set(text.lower().split())
        marathi_score = len(words & MARATHI_WORDS)
        hindi_score = len(words & HINDI_WORDS)
        # Default to Hindi unless clear Marathi match
        return "mr" if marathi_score > hindi_score and marathi_score >= 2 else "hi"
    
    # Check for romanized Hindi/Marathi keywords
    lower = text.lower()
    words = set(lower.split())
    
    marathi_score = len(words & MARATHI_WORDS)
    hindi_score = len(words & HINDI_WORDS)
    
    if marathi_score > hindi_score and marathi_score > 0:
        return "mr"
    if hindi_score > 0:
        return "hi"
    
    return "en"


def get_text(key: str, lang: str, **kwargs) -> str:
    """Get localized string."""
    template = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


STRINGS = {
    "en": {
        "welcome": "👋 Welcome to *Hawkins Cookers*!\n\nI'm your AI assistant. How can I help you today?\n\n1️⃣ Browse Products\n2️⃣ Get a Recipe\n3️⃣ Warranty / Complaint\n4️⃣ Track Order\n\nJust type your question naturally!",
        "product_found": "🍳 Here are the best matches for you:\n\n{products}\n\nType a product name for more details, or ask me to filter by budget!",
        "product_none": "😕 I couldn't find a product matching your criteria. Could you tell me:\n- What capacity do you need? (e.g., 3L, 5L)\n- Do you need induction compatible?\n- Any budget in mind?",
        "recipe_intro": "👩‍🍳 Here's a recipe for *{dish}* in your Hawkins pressure cooker:\n\n{steps}\n\n⏱ Total time: {time}\n\nWant another recipe?",
        "warranty_start": "I'm sorry to hear about the issue. Let's file a warranty claim.\n\nPlease share your *product model number* (e.g., A10, Futura 3L):",
        "warranty_date": "Got it! Now please share the *purchase date* (e.g., Jan 2023):",
        "warranty_complaint": "Almost done! Please *describe the issue* with your cooker:",
        "warranty_done": "✅ Your warranty claim has been registered!\n\n🎫 Ticket ID: *{ticket_id}*\n\nOur team will contact you within *2 business days* on this WhatsApp number. Keep your purchase receipt handy.",
        "order_prompt": "Please share your *order ID* (e.g., HWK123456) to track your order:",
        "order_info": "📦 Order *{order_id}*\nStatus: *{status}*\nEstimated delivery: *{eta}*",
        "fallback": "I'm not sure I understood that. 😊 Here's what I can help with:\n\n1️⃣ *Product recommendations* — e.g., 'Show me a 5L pressure cooker'\n2️⃣ *Recipes* — e.g., 'How to cook dal in pressure cooker'\n3️⃣ *Warranty* — e.g., 'I have a complaint about my cooker'\n4️⃣ *Order tracking* — e.g., 'Track my order HWK123'\n\nOr type *HELP* to see the menu.",
        "human_handoff": "I'll connect you to our support team now. 👤\n\nYou can also reach us at:\n📞 1800-xxx-xxxx (toll free)\n🌐 www.hawkinscookers.com\n⏰ Mon–Sat, 9am–6pm",
    },
    "hi": {
        "welcome": "👋 *Hawkins Cookers* में आपका स्वागत है!\n\nमैं आपका AI सहायक हूँ। आज मैं आपकी कैसे मदद कर सकता हूँ?\n\n1️⃣ Products देखें\n2️⃣ Recipe पाएं\n3️⃣ Warranty / Complaint\n4️⃣ Order Track करें\n\nसीधे अपना सवाल पूछें!",
        "product_found": "🍳 आपके लिए बेहतरीन विकल्प:\n\n{products}\n\nकिसी product का नाम type करें या budget बताएं!",
        "product_none": "😕 आपकी जरूरत के अनुसार कोई product नहीं मिला। कृपया बताएं:\n- कितने लीटर का चाहिए?\n- Induction पर चाहिए?\n- Budget क्या है?",
        "recipe_intro": "👩‍🍳 Hawkins pressure cooker में *{dish}* बनाने की विधि:\n\n{steps}\n\n⏱ कुल समय: {time}\n\nकोई और recipe चाहिए?",
        "warranty_start": "असुविधा के लिए खेद है। Warranty claim दर्ज करते हैं।\n\nकृपया *product का model number* बताएं (जैसे A10, Futura 3L):",
        "warranty_date": "ठीक है! अब *खरीद की तारीख* बताएं (जैसे Jan 2023):",
        "warranty_complaint": "बस थोड़ा और! कृपया *समस्या का विवरण* दें:",
        "warranty_done": "✅ आपकी warranty claim दर्ज हो गई!\n\n🎫 Ticket ID: *{ticket_id}*\n\nहमारी टीम *2 business days* में इस WhatsApp पर संपर्क करेगी।",
        "fallback": "मुझे समझ नहीं आया। 😊 मैं इनमें मदद कर सकता हूँ:\n\n1️⃣ *Products* — '5L pressure cooker दिखाओ'\n2️⃣ *Recipes* — 'dal कैसे बनाएं'\n3️⃣ *Warranty* — 'cooker में problem है'\n4️⃣ *Order* — 'HWK123 track करो'\n\n*HELP* type करें menu के लिए।",
        "human_handoff": "आपको हमारी support team से connect कर रहे हैं। 👤\n\nसंपर्क करें:\n📞 1800-xxx-xxxx (toll free)\n🌐 www.hawkinscookers.com",
    },
    "mr": {
        "welcome": "👋 *Hawkins Cookers* मध्ये आपले स्वागत आहे!\n\nमी तुमचा AI सहाय्यक आहे. आज मी तुम्हाला कशी मदत करू?\n\n1️⃣ Products पाहा\n2️⃣ Recipe मिळवा\n3️⃣ Warranty / Complaint\n4️⃣ Order Track करा\n\nसरळ प्रश्न विचारा!",
        "product_found": "🍳 तुमच्यासाठी सर्वोत्तम पर्याय:\n\n{products}\n\nProduct चे नाव type करा किंवा budget सांगा!",
        "product_none": "😕 तुमच्या गरजेनुसार product आढळले नाही. कृपया सांगा:\n- किती लिटरचे हवे?\n- Induction वर हवे?\n- Budget किती आहे?",
        "warranty_start": "त्रासासाठी माफ करा. Warranty claim नोंदवूया.\n\nकृपया *product चा model number* सांगा:",
        "warranty_done": "✅ तुमची warranty claim नोंदवली गेली!\n\n🎫 Ticket ID: *{ticket_id}*\n\nआमची टीम *2 business days* मध्ये संपर्क करेल.",
        "fallback": "मला समजले नाही. 😊 मी या गोष्टींमध्ये मदत करू शकतो:\n\n1️⃣ *Products* — '5L pressure cooker दाखवा'\n2️⃣ *Recipes* — 'dal कसा बनवायचा'\n3️⃣ *Warranty* — 'cooker मध्ये problem आहे'\n\n*HELP* type करा menu साठी.",
        "human_handoff": "तुम्हाला आमच्या support team शी connect करत आहोत. 👤",
    },
}
