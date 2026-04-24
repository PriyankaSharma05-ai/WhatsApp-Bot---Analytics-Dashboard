# 🍲 Hawkins Cookers WhatsApp AI Chatbot

**Hawkins Summer Internship 2026 — IT & AI Department**  
Built by: Priyanka | Project: WhatsApp Chatbot

---

## What This Does

A production-ready WhatsApp chatbot for Hawkins Cookers that:
- Recommends products from 20+ catalog items based on user needs
- Provides step-by-step pressure cooker recipes (8 dishes, EN/HI/MR)
- Handles warranty claims with ticket generation and DB logging
- Tracks orders via order ID
- Supports **English, Hindi, and Marathi**
- Logs all conversations to a database
- Provides a live analytics dashboard (Streamlit)

---

## Project Structure

```
hawkins-whatsapp-bot/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── webhook.py           # Twilio webhook — main entry point
│   ├── intent.py            # Claude AI intent classifier
│   ├── session.py           # Redis session manager
│   ├── language.py          # Language detection + all translations
│   ├── models.py            # SQLAlchemy DB models
│   ├── api.py               # REST API for dashboard
│   └── handlers/
│       ├── greeting.py      # Welcome message
│       ├── product.py       # Product recommendation engine
│       ├── recipe.py        # Recipe suggestions
│       ├── warranty.py      # Multi-turn warranty claim flow
│       ├── order.py         # Order tracking
│       └── fallback.py      # Human handoff
├── data/
│   ├── seed_products.py     # 20+ Hawkins product catalog
│   └── recipes.json         # 8 pressure cooker recipes
├── dashboard/
│   └── app.py               # Streamlit analytics dashboard
├── tests/
│   └── test_app.py          # 20+ pytest test cases
├── docker-compose.yml       # Full stack: Flask + PostgreSQL + Redis + Dashboard
├── Dockerfile
├── Procfile                 # For Railway/Heroku deployment
├── railway.json
├── requirements.txt
├── run.py                   # Dev server entry point
└── .env.example             # Copy to .env and fill credentials
```

---

## Quick Start (Local Development)

### Step 1 — Clone & setup

```bash
git clone <your-repo-url>
cd hawkins-whatsapp-bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Configure environment

```bash
cp .env.example .env
# Edit .env and fill in:
#   ANTHROPIC_API_KEY   → get from console.anthropic.com (free tier works)
#   TWILIO_ACCOUNT_SID  → get from console.twilio.com (free sandbox)
#   TWILIO_AUTH_TOKEN   → same
```

### Step 3 — Run the server

```bash
python run.py
# Server starts on http://localhost:5000
# Health check: http://localhost:5000/health
```

### Step 4 — Expose to Twilio with ngrok

```bash
# Install ngrok from https://ngrok.com (free)
ngrok http 5000
# Copy the HTTPS URL: e.g. https://abc123.ngrok-free.app
```

### Step 5 — Connect Twilio WhatsApp Sandbox

1. Go to [console.twilio.com](https://console.twilio.com) → Messaging → Try it out → Send a WhatsApp message
2. Follow instructions to join sandbox (send "join <word>" to their number)
3. Go to Sandbox Settings → set **"When a message comes in"** to:
   ```
   https://abc123.ngrok-free.app/webhook
   ```
4. Save. Now send a WhatsApp message to the Twilio sandbox number — your bot replies!

### Step 6 — Run analytics dashboard

```bash
# In a separate terminal:
streamlit run dashboard/app.py
# Opens at http://localhost:8501
```

### Step 7 — Run tests

```bash
pytest tests/ -v
```

---

## Docker (Full Stack)

```bash
cp .env.example .env
# Fill in ANTHROPIC_API_KEY in .env

docker-compose up --build
# Flask API: http://localhost:5000
# Dashboard: http://localhost:8501
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

---

## Deploy to Railway (Free Hosting — Live URL)

Railway gives you a free live URL so Twilio can actually call your webhook without ngrok.

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/hawkins-whatsapp-bot.git
git push -u origin main
```

### Step 2 — Deploy on Railway

1. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Select your repo
3. Add services: **PostgreSQL** and **Redis** (click "+ New" → Database)
4. Add environment variables in Railway dashboard:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   TWILIO_ACCOUNT_SID=AC...
   TWILIO_AUTH_TOKEN=...
   SECRET_KEY=any-random-string
   ```
   Railway auto-sets `DATABASE_URL` and `REDIS_URL` when you add those services.
5. Railway auto-deploys. Copy your public URL (e.g., `https://hawkins-bot-production.up.railway.app`)

### Step 3 — Update Twilio webhook

In Twilio sandbox settings, change webhook URL to:
```
https://hawkins-bot-production.up.railway.app/webhook
```

**You now have a live WhatsApp chatbot with a real URL!**

---

## Conversation Demo

```
You:  hello
Bot:  👋 Welcome to Hawkins Cookers!
      1️⃣ Browse Products  2️⃣ Recipe  3️⃣ Warranty  4️⃣ Order

You:  I need a 5 liter induction pressure cooker
Bot:  🍳 Here are the best matches:
      1. Hawkins Futura Induction Compatible 5L
         📦 5L | Hard Anodised | ⚡ Induction
         💰 ₹4,199
         🛒 hawkinscookers.com/...

You:  how to cook dal
Bot:  👩‍🍳 Dal Tadka recipe in Hawkins pressure cooker:
      1. Wash 1 cup toor dal and soak...
      ⏱ Total time: 25 mins

You:  mujhe warranty chahiye
Bot:  [Switches to Hindi]
      असुविधा के लिए खेद है। Model number बताएं:

You:  A10
Bot:  खरीद की तारीख बताएं:

You:  Jan 2023
Bot:  समस्या का विवरण दें:

You:  whistle nahi baj raha
Bot:  ✅ Warranty claim दर्ज!
      🎫 Ticket ID: HWK839201
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/webhook` | POST | Twilio WhatsApp webhook |
| `/health` | GET | Health check |
| `/api/stats` | GET | Summary metrics |
| `/api/intents` | GET | Intent distribution |
| `/api/languages` | GET | Language breakdown |
| `/api/recent` | GET | Last 20 conversations |
| `/api/warranty-claims` | GET | All warranty tickets |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ Yes | Claude AI for intent classification |
| `TWILIO_ACCOUNT_SID` | ✅ Yes | Twilio account |
| `TWILIO_AUTH_TOKEN` | ✅ Yes | Twilio auth |
| `DATABASE_URL` | ✅ Yes | SQLite (local) or PostgreSQL (prod) |
| `SECRET_KEY` | ✅ Yes | Flask secret key |
| `REDIS_URL` | Optional | Session storage (falls back to memory) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| API server | Python 3.11 + Flask 3.0 |
| WhatsApp | Twilio WhatsApp Business API |
| AI / NLP | Anthropic Claude (claude-haiku) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Sessions | Redis (optional) |
| Dashboard | Streamlit |
| Container | Docker + Docker Compose |
| Hosting | Railway.app |

---

## For Hawkins IT Team — Production Handoff

To take this to Hawkins' production WhatsApp Business number:

1. Apply for [WhatsApp Business API](https://www.twilio.com/en-us/whatsapp/api) via Twilio (or Meta directly)
2. Replace mock order lookup in `app/handlers/order.py` with actual ERP API call
3. Add product catalog sync job (weekly CSV import from Hawkins inventory system)
4. Set `FLASK_ENV=production` and use gunicorn with 4+ workers
5. Enable Railway/AWS auto-scaling for peak load

---

*Hawkins Summer Internship 2026 | IT & AI Department*
