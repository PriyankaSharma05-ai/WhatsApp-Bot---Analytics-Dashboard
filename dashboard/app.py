"""
Hawkins WhatsApp Bot — Analytics Dashboard
Run: streamlit run dashboard/app.py
"""
import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="Hawkins Bot Analytics",
    page_icon="🍲",
    layout="wide"
)

# ---- Config ----
API_BASE = "http://localhost:5000/api"

st.title("🍲 Hawkins WhatsApp Bot — Analytics Dashboard")
st.caption("Live metrics from your WhatsApp AI Assistant")

# ---- Fetch data ----
@st.cache_data(ttl=30)
def fetch(endpoint):
    try:
        r = requests.get(f"{API_BASE}/{endpoint}", timeout=5)
        return r.json()
    except Exception as e:
        return None


stats = fetch("stats")
intents = fetch("intents")
languages = fetch("languages")
recent = fetch("recent")
claims = fetch("warranty-claims")

# ---- Summary metrics ----
if stats:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Conversations", stats.get("total_conversations", 0))
    col2.metric("Unique Users", stats.get("total_users", 0))
    col3.metric("Resolution Rate", f"{stats.get('resolution_rate', 0)}%")
    col4.metric("Today's Chats", stats.get("today_conversations", 0))
    col5.metric("Open Warranty Claims", stats.get("open_warranty_claims", 0))
else:
    st.warning("⚠️ Cannot connect to bot API. Make sure Flask server is running on port 5000.")
    st.code("python run.py", language="bash")

st.divider()

# ---- Charts row ----
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Intent Distribution")
    if intents:
        import pandas as pd
        df = pd.DataFrame(intents)
        if not df.empty:
            st.bar_chart(df.set_index("intent")["count"])
        else:
            st.info("No data yet. Send some WhatsApp messages to see this chart.")
    else:
        st.info("No intent data available.")

with col_right:
    st.subheader("Language Distribution")
    if languages:
        import pandas as pd
        df = pd.DataFrame(languages)
        if not df.empty:
            lang_labels = {"en": "English 🇬🇧", "hi": "Hindi 🇮🇳", "mr": "Marathi 🇮🇳"}
            df["language"] = df["language"].map(lambda x: lang_labels.get(x, x))
            st.bar_chart(df.set_index("language")["count"])
        else:
            st.info("No language data yet.")
    else:
        st.info("No language data available.")

st.divider()

# ---- Recent conversations ----
st.subheader("Recent Conversations")
if recent:
    import pandas as pd
    df = pd.DataFrame(recent)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%b %d, %H:%M")
        df["resolved"] = df["resolved"].map({True: "✅", False: "❌"})
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No conversations yet.")
else:
    st.info("No conversation data available.")

st.divider()

# ---- Warranty Claims ----
st.subheader("Warranty Claims")
if claims:
    import pandas as pd
    df = pd.DataFrame(claims)
    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%b %d, %Y")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No warranty claims yet.")
else:
    st.info("No warranty claim data available.")

# ---- Footer ----
st.divider()
st.caption("Built by Priyanka — Hawkins Summer Internship 2026 | IT & AI Department")
st.caption("Refresh every 30 seconds | Data from Flask API on localhost:5000")
