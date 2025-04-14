from twitter_scraper import scrape_twitter
from telegram_sniper import fetch_latest_messages
from dexscreener_scanner import get_hot_pairs

print("🚀 Starting Full Module Test...\n")

# 1️⃣ Twitter Test
try:
    print("🐦 Testing Twitter Scraper...")
    tweets = scrape_twitter("100x gem")
    for i, tweet in enumerate(tweets[:5]):
        print(f"  {i+1}. {tweet[:100]}...")
    print("✅ Twitter Scraper: PASS\n")
except Exception as e:
    print(f"❌ Twitter Scraper Error: {e}\n")

# 2️⃣ Telegram Test
try:
    print("📡 Testing Telegram Scanner...")
    messages = fetch_latest_messages("@memecoingems", limit=5)  # replace with a group you're in
    for i, msg in enumerate(messages):
        print(f"  {i+1}. {msg[:100]}...")
    print("✅ Telegram Scanner: PASS\n")
except Exception as e:
    print(f"❌ Telegram Scanner Error: {e}\n")

# 3️⃣ Dexscreener Test
try:
    print("💹 Testing Dexscreener Scanner...")
    hot = get_hot_pairs()
    for pair in hot[:5]:
        print(f"  🔥 {pair['name']} | {pair['change_5min']}% | {pair['url']}")
    print("✅ Dexscreener Scanner: PASS\n")
except Exception as e:
    print(f"❌ Dexscreener Error: {e}\n")

print("🎯 ALL MODULE TEST COMPLETE")
