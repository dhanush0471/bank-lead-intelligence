import requests
import os
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# -----------------------------
# REAL DATA INGESTION LAYER (SIMULATED API STRUCTURE)
# In production, replace this with MCA / licensed data provider API
# -----------------------------

def fetch_companies():
    # This mimics real MCA-style structured response
    return [
        {
            "name": "Infosys Technologies Pvt Ltd",
            "city": "Bangalore",
            "state": "Karnataka",
            "industry": "IT Services"
        },
        {
            "name": "Urban Finance Solutions Pvt Ltd",
            "city": "Bangalore",
            "state": "Karnataka",
            "industry": "Fintech"
        },
        {
            "name": "Sharma Traders",
            "city": "Delhi",
            "state": "Delhi",
            "industry": "Trading"
        }
    ]

def score_company(c):
    score = 0

    if c["state"] == "Karnataka":
        score += 35

    if "Bangalore" in c["city"]:
        score += 25

    if "Pvt" in c["name"]:
        score += 10

    if c["industry"] in ["Fintech", "IT Services"]:
        score += 25

    return score

companies = fetch_companies()

for c in companies:
    score = score_company(c)

    if score < 60:
        continue

    msg = f"""
🏦 BANK CRM v2 LEAD

🏢 {c['name']}
📍 {c['city']}, {c['state']}
🏭 Industry: {c['industry']}

⭐ Score: {score}/100
⏱ {datetime.now()}

Source: MCA-style Registry Layer
"""

    send(msg)

send("✅ CRM v2 RUN COMPLETED")
