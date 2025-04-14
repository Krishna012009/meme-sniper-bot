# 📦 risk_filters.py - Honeypot & LP Detector

import random
import re
import requests

# ✅ Simulate Honeypot Check (Mock)
def is_honeypot(token_address):
    # TODO: Replace with real honeypot API or contract checker
    fake_risk_score = random.random()
    if fake_risk_score > 0.9:
        return True  # suspicious
    return False

# ✅ Extract LP Lock from Dexscreener chart link
def get_lp_info(dex_url):
    try:
        response = requests.get(dex_url, timeout=10)
        text = response.text

        # Simulated LP % via keyword extraction
        match = re.search(r'Locked LP.*?(\d{1,3})%', text)
        if match:
            return int(match.group(1))
        return 100  # Assume 100% LP if not found
    except Exception as e:
        print(f"❌ LP Info Error: {e}")
        return 0
