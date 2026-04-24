"""Seed the database with Hawkins product catalog."""
import logging

logger = logging.getLogger(__name__)

PRODUCTS = [
    # Aluminium Pressure Cookers
    {"name": "Hawkins Classic Aluminium Pressure Cooker 1.5L", "model_no": "B10-09",
     "category": "pressure_cooker", "capacity_liters": 1.5, "material": "aluminium",
     "induction_compatible": False, "price": 999,
     "buy_url": "https://www.hawkinscookers.com/product/classic-1-5l",
     "description": "Perfect for 1-2 persons. Lightweight and easy to use."},
    {"name": "Hawkins Classic Aluminium Pressure Cooker 3L", "model_no": "B10-09-3",
     "category": "pressure_cooker", "capacity_liters": 3.0, "material": "aluminium",
     "induction_compatible": False, "price": 1299,
     "buy_url": "https://www.hawkinscookers.com/product/classic-3l",
     "description": "Ideal for a family of 2-4."},
    {"name": "Hawkins Classic Aluminium Pressure Cooker 5L", "model_no": "B10-09-5",
     "category": "pressure_cooker", "capacity_liters": 5.0, "material": "aluminium",
     "induction_compatible": False, "price": 1699,
     "buy_url": "https://www.hawkinscookers.com/product/classic-5l",
     "description": "Great for families of 4-6."},
    {"name": "Hawkins Classic Aluminium Pressure Cooker 8L", "model_no": "B10-09-8",
     "category": "pressure_cooker", "capacity_liters": 8.0, "material": "aluminium",
     "induction_compatible": False, "price": 2199,
     "buy_url": "https://www.hawkinscookers.com/product/classic-8l",
     "description": "For large families and bulk cooking."},

    # Stainless Steel Pressure Cookers
    {"name": "Hawkins Stainless Steel Pressure Cooker 3L", "model_no": "SS3L",
     "category": "pressure_cooker", "capacity_liters": 3.0, "material": "stainless_steel",
     "induction_compatible": True, "price": 2799,
     "buy_url": "https://www.hawkinscookers.com/product/ss-3l",
     "description": "Premium stainless steel, works on all stoves including induction."},
    {"name": "Hawkins Stainless Steel Pressure Cooker 5L", "model_no": "SS5L",
     "category": "pressure_cooker", "capacity_liters": 5.0, "material": "stainless_steel",
     "induction_compatible": True, "price": 3499,
     "buy_url": "https://www.hawkinscookers.com/product/ss-5l",
     "description": "Ideal for 4-6 people, induction compatible."},
    {"name": "Hawkins Stainless Steel Pressure Cooker 8L", "model_no": "SS8L",
     "category": "pressure_cooker", "capacity_liters": 8.0, "material": "stainless_steel",
     "induction_compatible": True, "price": 4299,
     "buy_url": "https://www.hawkinscookers.com/product/ss-8l",
     "description": "Large capacity, perfect for big families."},

    # Futura Hard Anodised
    {"name": "Hawkins Futura Hard Anodised Pressure Cooker 2L", "model_no": "HA2",
     "category": "pressure_cooker", "capacity_liters": 2.0, "material": "hard_anodised",
     "induction_compatible": False, "price": 2499,
     "buy_url": "https://www.hawkinscookers.com/product/futura-2l",
     "description": "Futura range — premium hard anodised, non-stick interior."},
    {"name": "Hawkins Futura Hard Anodised Pressure Cooker 3L", "model_no": "HA3",
     "category": "pressure_cooker", "capacity_liters": 3.0, "material": "hard_anodised",
     "induction_compatible": False, "price": 2999,
     "buy_url": "https://www.hawkinscookers.com/product/futura-3l",
     "description": "Futura 3L — great for small families."},
    {"name": "Hawkins Futura Hard Anodised Pressure Cooker 5L", "model_no": "HA5",
     "category": "pressure_cooker", "capacity_liters": 5.0, "material": "hard_anodised",
     "induction_compatible": False, "price": 3699,
     "buy_url": "https://www.hawkinscookers.com/product/futura-5l",
     "description": "Futura 5L — most popular model."},
    {"name": "Hawkins Futura Hard Anodised Pressure Cooker 7L", "model_no": "HA7",
     "category": "pressure_cooker", "capacity_liters": 7.0, "material": "hard_anodised",
     "induction_compatible": False, "price": 4299,
     "buy_url": "https://www.hawkinscookers.com/product/futura-7l",
     "description": "Large family size Futura."},

    # Futura Induction Compatible
    {"name": "Hawkins Futura Induction Compatible 3L", "model_no": "FUIN3",
     "category": "pressure_cooker", "capacity_liters": 3.0, "material": "hard_anodised",
     "induction_compatible": True, "price": 3499,
     "buy_url": "https://www.hawkinscookers.com/product/futura-induction-3l",
     "description": "Futura with induction base — best seller."},
    {"name": "Hawkins Futura Induction Compatible 5L", "model_no": "FUIN5",
     "category": "pressure_cooker", "capacity_liters": 5.0, "material": "hard_anodised",
     "induction_compatible": True, "price": 4199,
     "buy_url": "https://www.hawkinscookers.com/product/futura-induction-5l",
     "description": "Best of both worlds — Futura quality with induction."},

    # Cookware
    {"name": "Hawkins Futura Non-Stick Kadai 1.5L", "model_no": "KADAI-1.5",
     "category": "cookware", "capacity_liters": 1.5, "material": "hard_anodised",
     "induction_compatible": False, "price": 1299,
     "buy_url": "https://www.hawkinscookers.com/product/kadai-1-5l",
     "description": "Perfect for stir frying and everyday cooking."},
    {"name": "Hawkins Futura Non-Stick Deep-Fry Pan 1.5L", "model_no": "DEEPFRY-1.5",
     "category": "cookware", "capacity_liters": 1.5, "material": "hard_anodised",
     "induction_compatible": False, "price": 1499,
     "buy_url": "https://www.hawkinscookers.com/product/deep-fry-pan",
     "description": "Ideal for deep frying with less oil."},
    {"name": "Hawkins Futura Non-Stick Tawa 26cm", "model_no": "TAWA-26",
     "category": "cookware", "capacity_liters": None, "material": "hard_anodised",
     "induction_compatible": False, "price": 899,
     "buy_url": "https://www.hawkinscookers.com/product/tawa-26cm",
     "description": "For perfect rotis and dosas every time."},
    {"name": "Hawkins Futura Non-Stick Sauce Pan 1L", "model_no": "SAUCE-1",
     "category": "cookware", "capacity_liters": 1.0, "material": "hard_anodised",
     "induction_compatible": False, "price": 999,
     "buy_url": "https://www.hawkinscookers.com/product/sauce-pan-1l",
     "description": "For gravies, sauces, and soups."},

    # Accessories
    {"name": "Hawkins Pressure Cooker Gasket (Classic)", "model_no": "GASKET-C",
     "category": "accessory", "capacity_liters": None, "material": "rubber",
     "induction_compatible": None, "price": 120,
     "buy_url": "https://www.hawkinscookers.com/product/gasket-classic",
     "description": "Replacement rubber gasket for Hawkins Classic cookers."},
    {"name": "Hawkins Pressure Regulator / Whistle", "model_no": "WHISTLE-C",
     "category": "accessory", "capacity_liters": None, "material": "aluminium",
     "induction_compatible": None, "price": 85,
     "buy_url": "https://www.hawkinscookers.com/product/whistle",
     "description": "Replacement pressure regulator for Classic range."},
    {"name": "Hawkins Safety Valve", "model_no": "SAFETY-V",
     "category": "accessory", "capacity_liters": None, "material": "rubber",
     "induction_compatible": None, "price": 75,
     "buy_url": "https://www.hawkinscookers.com/product/safety-valve",
     "description": "Replacement safety valve."},
    {"name": "Hawkins Futura Gasket Set", "model_no": "GASKET-F",
     "category": "accessory", "capacity_liters": None, "material": "rubber",
     "induction_compatible": None, "price": 150,
     "buy_url": "https://www.hawkinscookers.com/product/gasket-futura",
     "description": "Replacement gasket for Futura range."},
]


def seed_if_empty():
    """Seed products only if table is empty."""
    from app.models import Product, db

    try:
        if Product.query.count() > 0:
            return
        for p in PRODUCTS:
            product = Product(**p)
            db.session.add(product)
        db.session.commit()
        logger.info(f"Seeded {len(PRODUCTS)} products.")
    except Exception as e:
        logger.error(f"Seed error: {e}")
        db.session.rollback()
