# 📦 sniper_system_check.py - Ultimate SniperBot Diagnostic Suite (v3.0)

import traceback
from ai_trainer import predict_viral_score, train_from_insider_targets
from google_sheet_logger import paper_trade
from telegram_sniper import fetch_latest_messages
from reddit_scanner import fetch_reddit_trends
from geckoterminal_scanner import fetch_gecko_trends
from risk_filters import is_honeypot, get_lp_info
from insider_targets_loader import load_insider_targets

# ✅ Fallback voice alert (Replit safe)
try:
    from voice_alerts import speak
except:
    def speak(msg): print(f"[🔈] {msg} (voice fallback)")

print("\n🔧 Running Full SniperBot Health Check...\n")

# 1️⃣ AI Classifier
try:
    msg = "🔥 New 100x gem just launched"
    pred, score = predict_viral_score(msg)
    print(f"🧠 AI Classifier ✅ | Score: {score}% | Prediction: {'VIRAL' if pred else 'Not Viral'}")
except Exception as e:
    print("❌ AI Module Error:")
    traceback.print_exc()

# 2️⃣ Google Sheets Logger
try:
    paper_trade("0x123456789abcdef123456789abcdef12345678", "https://dexscreener.com/ethereum/0x123456789abcdef")
    print("📒 Google Sheets ✅ | Paper trade logged successfully")
except Exception as e:
    print("❌ Google Sheets Error:")
    traceback.print_exc()

# 3️⃣ Telegram Sniper
try:
    msgs = fetch_latest_messages("@krishnamemecoinsniperbot")
    print(f"📡 Telegram Fetch ✅ | Messages: {len(msgs)}")
except Exception as e:
    print("❌ Telegram Error:")
    traceback.print_exc()

# 4️⃣ Reddit Scanner
try:
    reddit_hits = fetch_reddit_trends()
    print(f"🧵 Reddit Fetch ✅ | Hits: {len(reddit_hits)}")
except Exception as e:
    print("❌ Reddit Error:")
    traceback.print_exc()

# 5️⃣ GeckoTerminal Scanner
try:
    coins = fetch_gecko_trends()
    print(f"💹 GeckoTerminal ✅ | Hot Pairs: {len(coins)}")
except Exception as e:
    print("❌ GeckoTerminal Error:")
    traceback.print_exc()

# 6️⃣ Risk Filters
try:
    token = "0xabc1234567890defabc1234567890defabc12345"
    honeypot = is_honeypot(token)
    lp = get_lp_info("https://geckoterminal.com/ethereum/pools/0xabc123")
    print(f"🔐 Risk Filter ✅ | Honeypot: {honeypot} | LP Lock: {lp}%")
except Exception as e:
    print("❌ Risk Filter Error:")
    traceback.print_exc()

# 7️⃣ Insider Targets AI Feed
try:
    entries = load_insider_targets()
    print(f"📄 Insider Targets ✅ | Loaded: {len(entries)} entries")
except Exception as e:
    print("⚠️ Insider Targets ⚠️ | No file or error:")
    traceback.print_exc()

# 8️⃣ Voice System (Mocked for Replit)
try:
    speak("🧪 SniperBot system check complete.")
    print("🔊 Voice Alerts ✅ | OK (or mocked fallback)")
except Exception as e:
    print("❌ Voice Alert Error:")
    traceback.print_exc()

print("\n✅ SYSTEM CHECK COMPLETE — ALL MODULES TESTED\n")
