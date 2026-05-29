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
            "turnover_est": 500
        },
        {
            "name": "Urban Pay Fintech Pvt Ltd",
            "city": "Bangalore",
            "state": "Karnataka",
            "industry": "Fintech",
            "turnover_est": 80
        },
        {
            "name": "Small Retail Shop",
            "city": "Mysore",
            "state": "Karnataka",
            "industry": "Retail",
            "turnover_est": 10
        }
    ]


# -----------------------------
# AI-STYLE SCORING ENGINE
# -----------------------------
def score_lead(c):
    score = 0

    # Location priority
    if c["state"] == "Karnataka":
        score += 20
    if c["city"] == "Bangalore":
        score += 25

    # Business type
    if c["industry"] in ["Fintech", "IT Services"]:
        score += 25
    if c["industry"] == "Retail":
        score += 10

    # Turnover intelligence
    if c["turnover_est"] > 100:
        score += 30
    elif c["turnover_est"] > 50:
        score += 15

    return score


# -----------------------------
# LEAD QUALITY FILTER
# -----------------------------
def is_hot_lead(score):
    return score >= 60


# -----------------------------
# MAIN PIPELINE
# -----------------------------
companies = fetch_companies()

for c in companies:

    score = score_lead(c)

    if not is_hot_lead(score):
        continue

    msg = f"""
🏦 CRM v3 - HOT BANKING LEAD

🏢 {c['name']}
📍 {c['city']}, {c['state']}
🏭 Industry: {c['industry']}
💰 Est. Turnover: {c['turnover_est']} Cr

🔥 Credit Score: {score}/100
🎯 Status: HOT LEAD

⏱ {datetime.now()}
"""

    send(msg)

send("✅ CRM v3 EXECUTION COMPLETE")
