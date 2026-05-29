import requests
import os
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# -----------------------------
# TELEGRAM SENDER
# -----------------------------
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


# -----------------------------
# SIMULATED REAL DATA LAYER
# (Replace later with MCA / paid APIs)
# -----------------------------
def fetch_companies():
    return [
        {
            "name": "Infosys Technologies Pvt Ltd",
            "city": "Bangalore",
            "state": "Karnataka",
            "industry": "IT Services",
            "turnover": 500
        },
        {
            "name": "Urban Pay Fintech Pvt Ltd",
            "city": "Bangalore",
            "state": "Karnataka",
            "industry": "Fintech",
            "turnover": 80
        },
        {
            "name": "Small Retail Shop",
            "city": "Mysore",
            "state": "Karnataka",
            "industry": "Retail",
            "turnover": 10
        }
    ]


# -----------------------------
# SMART SCORING ENGINE (CRM v2)
# -----------------------------
def score_lead(c):

    score = 0

    name = c["name"].lower()

    # ❌ filter junk/system noise
    junk_words = ["search", "messages", "english", "login", "menu"]
    if any(j in name for j in junk_words):
        return 0

    # 📍 location boost
    if c["state"] == "Karnataka":
        score += 25

    if c["city"] == "Bangalore":
        score += 25

    # 🏦 industry intelligence
    industry = c.get("industry", "").lower()

    if "fintech" in industry:
        score += 30
    elif "finance" in industry:
        score += 20
    elif "it" in industry:
        score += 15

    # 💰 turnover scoring
    t = c.get("turnover", 0)

    if t > 500:
        score += 30
    elif t > 100:
        score += 20
    elif t > 50:
        score += 10

    return score


# -----------------------------
# LEAD QUALITY FILTER (STRICT)
# -----------------------------
def is_high_value_lead(score):
    return score >= 75


# -----------------------------
# MAIN PIPELINE
# -----------------------------
companies = fetch_companies()

sent = 0

for c in companies:

    score = score_lead(c)

    if not is_high_value_lead(score):
        continue

    msg = f"""
🏦 BANK CRM v2 LEAD

🏢 {c['name']}
📍 {c['city']}, {c['state']}
🏭 {c.get('industry','Unknown')}

💰 Turnover: {c.get('turnover','N/A')} Cr
🔥 Score: {score}/100

🎯 Status: HIGH VALUE LEAD

⏱ {datetime.now()}
"""

    send(msg)
    sent += 1

send(f"✅ CRM v2 EXECUTION COMPLETE | LEADS SENT: {sent}")
