# 📦 sniper_loop.py - GOD MODE: FINAL PHASE SNIPER ENGINE

import time
import re
from telegram_sniper import fetch_latest_messages
from reddit_scanner import fetch_reddit_trends
from geckoterminal_scanner import fetch_gecko_trends
from insider_targets_loader import load_insider_targets
from risk_filters import is_honeypot, get_lp_info
from google_sheet_logger import paper_trade, log_trade
from ai_trainer import predict_viral_score
from utils import load_seen_tokens, save_token
from voice_alerts import speak  # 🎙️ Voice alert system

# === CONFIG ===
SLEEP_DURATION = 600  # every 10 mins
seen_tokens = load_seen_tokens()

# === TOKEN EXTRACTOR ===
def extract_token(text):
    match = re.search(r"0x[a-fA-F0-9]{40}", text)
    return match.group(0) if match else None

# === SNIPER ENGINE ===
def sniper_engine(source, text, link=""):
    token = extract_token(text)
    if not token or token in seen_tokens:
        return

    prediction, score = predict_viral_score(text)
    if prediction == 0 or score < 80:
        print(f"⏭️ Skipped (AI Score {score}%) - {token}")
        return

    if is_honeypot(token):
        print(f"🧪 Honeypot Detected! {token}")
        return
    lp = get_lp_info(link)
    if lp < 80:
        print(f"🔐 LP too low: {lp}% for {token}")
        return

    # ✅ SUCCESS
    print(f"✅ Sniping {token} from {source} | LP: {lp}% | Score: {score}%")
    paper_trade(token, link)
    log_trade(source, token, link, score=score, lp=lp)
    save_token(token)

    # 🎙️ Speak it out
    speak(f"🚀 {source} sniper triggered! Token {token[:6]}... logged. Score: {score} percent.")

# === MAIN LOOP ===
while True:
    print("\n🚀 FINAL PHASE SNIPER LOOP STARTED\n")

    # 1️⃣ TELEGRAM
    try:
        telegram_hits = fetch_latest_messages("@krishnamemecoinsniperbot")
        for msg in telegram_hits:
            sniper_engine("Telegram", msg, link="")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

    # 2️⃣ REDDIT
    try:
        reddit_hits = fetch_reddit_trends()
        for post in reddit_hits:
            sniper_engine("Reddit", post['title'], link=post['url'])
    except Exception as e:
        print(f"❌ Reddit Error: {e}")

    # 3️⃣ INSIDER TARGETS
    try:
        insider_hits = load_insider_targets()
        for msg in insider_hits:
            sniper_engine("InsiderReel", msg)
    except Exception as e:
        print(f"❌ Insider Error: {e}")

    # 4️⃣ GECKOTERMINAL
    try:
        gecko_hits = fetch_gecko_trends()
        for coin in gecko_hits:
            text = f"{coin['name']} {coin['symbol']} {coin['url']}"
            sniper_engine("GeckoTerminal", text, link=coin['url'])
    except Exception as e:
        print(f"❌ GeckoTerminal Error: {e}")

    print(f"\n⏳ Waiting {SLEEP_DURATION // 60} minutes for next cycle...\n")
    time.sleep(SLEEP_DURATION)
