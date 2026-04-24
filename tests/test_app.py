"""
Tests for Hawkins WhatsApp Bot
Run: pytest tests/ -v
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.intent import _rule_based_fallback
from app.language import detect_language
from app.session import get_session, save_session, clear_session


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


# ── Language detection ─────────────────────────────────────────────────────────

class TestLanguageDetection:
    def test_english_detected(self):
        assert detect_language("I need a pressure cooker") == "en"

    def test_hindi_romanized_detected(self):
        assert detect_language("mujhe cooker chahiye") == "hi"

    def test_devanagari_detected(self):
        assert detect_language("मुझे कुकर चाहिए") == "hi"

    def test_english_product_query(self):
        assert detect_language("show me 5 liter induction cooker") == "en"


# ── Intent classification (rule-based fallback) ────────────────────────────────

class TestRuleBasedIntent:
    def test_greeting_hi(self):
        assert _rule_based_fallback("hello") == "greeting"

    def test_greeting_namaste(self):
        assert _rule_based_fallback("namaste") == "greeting"

    def test_product_query_buy(self):
        assert _rule_based_fallback("I want to buy a pressure cooker") == "product_query"

    def test_product_query_price(self):
        assert _rule_based_fallback("what is the price of 5 liter cooker") == "product_query"

    def test_recipe_dal(self):
        assert _rule_based_fallback("how to make dal") == "recipe_help"

    def test_recipe_cook(self):
        assert _rule_based_fallback("cook rice in pressure cooker") == "recipe_help"

    def test_warranty_complaint(self):
        assert _rule_based_fallback("I have a complaint about my cooker") == "warranty_claim"

    def test_warranty_broken(self):
        assert _rule_based_fallback("my cooker is broken") == "warranty_claim"

    def test_order_track(self):
        assert _rule_based_fallback("track my order HWK12345") == "order_tracking"

    def test_fallback_unknown(self):
        assert _rule_based_fallback("asjdhaksjdh xyz") == "fallback"


# ── Session management ─────────────────────────────────────────────────────────

class TestSession:
    def test_empty_session(self):
        session = get_session("+919999999999_test")
        assert session == {}

    def test_save_and_retrieve(self):
        phone = "+919999999998_test"
        save_session(phone, {"lang": "hi", "turn": 3})
        retrieved = get_session(phone)
        assert retrieved.get("lang") == "hi"
        assert retrieved.get("turn") == 3

    def test_clear_session(self):
        phone = "+919999999997_test"
        save_session(phone, {"lang": "en"})
        clear_session(phone)
        assert get_session(phone) == {}


# ── Webhook endpoint ───────────────────────────────────────────────────────────

class TestWebhook:
    def test_health_check(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"

    def test_webhook_missing_body(self, client):
        resp = client.post("/webhook", data={})
        assert resp.status_code == 400

    def test_webhook_greeting(self, client):
        resp = client.post("/webhook", data={
            "Body": "hello",
            "From": "whatsapp:+911234567890"
        })
        assert resp.status_code == 200
        assert b"Hawkins" in resp.data

    def test_webhook_hindi_greeting(self, client):
        resp = client.post("/webhook", data={
            "Body": "namaste",
            "From": "whatsapp:+911234567891"
        })
        assert resp.status_code == 200

    def test_webhook_product_query(self, client):
        resp = client.post("/webhook", data={
            "Body": "show me 5 liter pressure cooker",
            "From": "whatsapp:+911234567892"
        })
        assert resp.status_code == 200

    def test_webhook_warranty_start(self, client):
        resp = client.post("/webhook", data={
            "Body": "my cooker is broken",
            "From": "whatsapp:+911234567893"
        })
        assert resp.status_code == 200

    def test_webhook_recipe(self, client):
        resp = client.post("/webhook", data={
            "Body": "how to cook dal",
            "From": "whatsapp:+911234567894"
        })
        assert resp.status_code == 200


# ── API endpoints ──────────────────────────────────────────────────────────────

class TestAPI:
    def test_stats_endpoint(self, client):
        resp = client.get("/api/stats")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total_conversations" in data
        assert "resolution_rate" in data

    def test_intents_endpoint(self, client):
        resp = client.get("/api/intents")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_languages_endpoint(self, client):
        resp = client.get("/api/languages")
        assert resp.status_code == 200

    def test_recent_endpoint(self, client):
        resp = client.get("/api/recent")
        assert resp.status_code == 200

    def test_warranty_claims_endpoint(self, client):
        resp = client.get("/api/warranty-claims")
        assert resp.status_code == 200
