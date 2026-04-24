from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    model_no = db.Column(db.String(50), unique=True)
    category = db.Column(db.String(50))  # pressure_cooker, cookware, accessory
    capacity_liters = db.Column(db.Float)
    material = db.Column(db.String(50))  # aluminium, stainless_steel, hard_anodised
    induction_compatible = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    buy_url = db.Column(db.String(300))
    image_url = db.Column(db.String(300))
    in_stock = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model_no": self.model_no,
            "category": self.category,
            "capacity_liters": self.capacity_liters,
            "material": self.material,
            "induction_compatible": self.induction_compatible,
            "price": self.price,
            "description": self.description,
            "buy_url": self.buy_url,
        }


class Conversation(db.Model):
    __tablename__ = "conversations"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    user_message = db.Column(db.Text)
    bot_response = db.Column(db.Text)
    intent = db.Column(db.String(50))
    language = db.Column(db.String(10), default="en")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=True)


class WarrantyClaim(db.Model):
    __tablename__ = "warranty_claims"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20))
    model_no = db.Column(db.String(50))
    purchase_date = db.Column(db.String(50))
    complaint = db.Column(db.Text)
    ticket_id = db.Column(db.String(20))
    status = db.Column(db.String(20), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    language_pref = db.Column(db.String(10), default="en")
    owned_model = db.Column(db.String(50))
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    total_messages = db.Column(db.Integer, default=0)
