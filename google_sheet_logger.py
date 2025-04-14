import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ✅ Extract mock price from dexscreener link
def get_mock_price(dex_url):
    try:
        response = requests.get(dex_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        match = re.search(r"\$([0-9.]+)", text)
        return float(match.group(1)) if match else 0.0001
    except Exception as e:
        print(f"[ERROR] Failed to extract price: {e}")
        return 0.0001

# ✅ Google Sheets Auth
creds = Credentials.from_service_account_file(
    "sniperbotsheets-456110-1d906bbd0516.json",
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)
client = gspread.authorize(creds)
sheet = client.open("SniperBotLogs").sheet1  # Make sure this sheet exists

# ✅ Log paper trade
def paper_trade(token_address, chart_link):
    mock_price = get_mock_price(chart_link)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([
        now, "PAPER_TRADE", token_address, chart_link, mock_price, "Gas: 0.002 ETH", "Not Bought"
    ])
    print(f"📒 Logged Paper Trade: {token_address} @ ${mock_price:.6f}")

# ✅ Log general trade with full intelligence
def log_trade(source, token, link, price=0.0001, score=0, lp=0, honeypot=False):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([
        now,
        source,
        token,
        link,
        f"${price:.6f}",
        f"{score}%",
        f"{lp}%",
        "❌" if honeypot else "✅"
    ])
    print(f"📒 [LOGGED] {token} | {source} | {score}% | LP: {lp}% | Honeypot: {'YES' if honeypot else 'NO'}")
