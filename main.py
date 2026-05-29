import requests
import os
import json
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# -----------------------------
# PERSISTENT STATE MANAGEMENT
# (Deduplication + History)
# -----------------------------
def load_state():
    try:
        with open("state.json", "r") as f:
            return json.load(f)
    except:
        return {"processed_cins": [], "seen_emails": [], "rank_history": []}

def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)

def is_duplicate(cin, state):
    return cin in state["processed_cins"]

def mark_processed(cin, state):
    state["processed_cins"].append(cin)


# -----------------------------
# TELEGRAM SENDER
# -----------------------------
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


# -----------------------------
# MCA-STYLE DATA STRUCTURE
# (Production-ready company model)
# -----------------------------
class Company:
    def __init__(self, name, city, state, industry, turnover, cin, employees=None, email=None):
        self.name = name
        self.city = city
        self.state = state
        self.industry = industry
        self.turnover = turnover
        self.cin = cin
        self.employees = employees or 0
        self.email = email or "N/A"
        self.established_year = None

    def to_dict(self):
        return {
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "industry": self.industry,
            "turnover": self.turnover,
            "cin": self.cin,
            "employees": self.employees,
            "email": self.email,
            "established_year": self.established_year
        }


# -----------------------------
# MCA DATA LAYER
# (Simulated MCA dataset)
# -----------------------------
def fetch_companies_mca():
    return [
        Company(
            name="Infosys Technologies Pvt Ltd",
            city="Bangalore",
            state="Karnataka",
            industry="IT Services",
            turnover=1200,
            cin="L72200KA1981PTC041609",
            employees=260000,
            email="investors@infosys.com"
        ),
        Company(
            name="Urban Pay Fintech Pvt Ltd",
            city="Bangalore",
            state="Karnataka",
            industry="Fintech",
            turnover=180,
            cin="U65100KA2015PTC083123",
            employees=250,
            email="contact@urbanpay.com"
        ),
        Company(
            name="Small Retail Shop",
            city="Mysore",
            state="Karnataka",
            industry="Retail",
            turnover=25,
            cin="U45200KA2018PTC112345",
            employees=5,
            email="N/A"
        ),
        Company(
            name="TechVision AI Solutions",
            city="Bangalore",
            state="Karnataka",
            industry="IT Services",
            turnover=450,
            cin="U72200KA2019PTC098765",
            employees=1200,
            email="hr@techvision.com"
        ),
        Company(
            name="Capital Finance Ltd",
            city="Bangalore",
            state="Karnataka",
            industry="Finance",
            turnover=350,
            cin="U65999KA2016PTC087654",
            employees=800,
            email="business@capitalfin.com"
        )
    ]


# -----------------------------
# ML-STYLE AI RANKING ENGINE
# (Intelligent lead scoring v3)
# -----------------------------
def score_lead_ai(company):
    """
    AI-powered ranking using:
    - Location signals
    - Industry classification
    - Financial strength
    - Market opportunity
    - Company maturity
    """
    
    score = 0
    name = company.name.lower()

    # ❌ Junk filtering
    junk_words = ["search", "messages", "english", "login", "menu", "test", "dummy"]
    if any(j in name for j in junk_words):
        return 0

    # 📍 Location tier scoring
    if company.state == "Karnataka":
        score += 20
    if company.city == "Bangalore":
        score += 25

    # 🏦 Industry AI classification
    industry_lower = company.industry.lower()
    
    if "fintech" in industry_lower:
        score += 35  # High priority
    elif "finance" in industry_lower:
        score += 28
    elif "it" in industry_lower or "software" in industry_lower:
        score += 25
    elif "tech" in industry_lower:
        score += 22
    else:
        score += 5

    # 💰 Financial strength scoring
    if company.turnover > 1000:
        score += 30
    elif company.turnover > 500:
        score += 28
    elif company.turnover > 200:
        score += 20
    elif company.turnover > 100:
        score += 15
    elif company.turnover > 50:
        score += 8

    # 👥 Team size (maturity indicator)
    if company.employees > 5000:
        score += 15
    elif company.employees > 1000:
        score += 12
    elif company.employees > 500:
        score += 10
    elif company.employees > 100:
        score += 6
    elif company.employees > 0:
        score += 2

    # 📧 Contact availability
    if company.email != "N/A":
        score += 5

    # 🎯 Loan readiness indicator (banking logic)
    if company.turnover > 100 and company.employees > 50:
        score += 10  # High loan readiness

    return min(score, 100)  # Cap at 100


# -----------------------------
# LEAD RANKING & FILTERING
# (Top leads only - AI sorted)
# -----------------------------
def get_ranked_leads(companies, state):
    """
    Returns top-quality leads ranked by AI score
    """
    leads = []
    
    for company in companies:
        # Skip duplicates
        if is_duplicate(company.cin, state):
            continue
        
        score = score_lead_ai(company)
        
        # Strict quality threshold (80+)
        if score < 80:
            continue
        
        leads.append((company, score))
    
    # Sort by score descending (best first)
    leads.sort(key=lambda x: x[1], reverse=True)
    
    return leads


# -----------------------------
# ALERT FORMATTING (PROFESSIONAL)
# -----------------------------
def format_lead_alert(rank, company, score, total_leads):
    msg = f"""
🏆 RANK #{rank} BANKING LEAD (CRM v3)

🏢 {company.name}
📍 {company.city}, {company.state}
🏭 Industry: {company.industry}

💰 Turnover: ₹{company.turnover} Cr
👥 Team Size: {company.employees}
📧 Contact: {company.email}

🔥 AI Score: {score}/100
💡 Loan Ready: {'YES ✅' if score >= 85 else 'MAYBE 🤔'}

📊 Total Quality Leads Today: {total_leads}
🎯 Status: HIGH PRIORITY LEAD
⏱ {datetime.now()}
"""
    return msg


# -----------------------------
# MAIN PIPELINE (CRM v3)
# -----------------------------
state = load_state()

companies = fetch_companies_mca()

# Get ranked leads
ranked_leads = get_ranked_leads(companies, state)

sent = 0

for rank, (company, score) in enumerate(ranked_leads, 1):
    
    # Format and send alert
    msg = format_lead_alert(rank, company, score, len(ranked_leads))
    send(msg)
    
    # Mark as processed
    mark_processed(company.cin, state)
    
    sent += 1

# Save updated state
save_state(state)

# Completion alert
completion_msg = f"""
✅ CRM v3 EXECUTION COMPLETE

📊 Summary:
- Leads Processed: {len(companies)}
- Quality Leads Sent: {sent}
- Duplicates Skipped: {len(state['processed_cins']) - sent}
- Total in History: {len(state['processed_cins'])}

🤖 System: AI Ranking Engine v3
🔄 Next run: in 5 minutes
"""

send(completion_msg)
