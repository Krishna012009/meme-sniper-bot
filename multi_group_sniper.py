# 🚀 Telegram Insider Intelligence Engine
# ✅ Auto-Scan Insider Calls from Multiple Groups + AI Intelligence + Whale Filter (v1.0)

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import time
import re
import csv
from ai_trainer import predict_viral_score  # 🧠 AI pattern detector

# === CONFIG ===
api_id = 24339763
api_hash = "9a3fadf2e761e921546a00b565ccec2e"
phone_number = "+916399813966"
GROUP_FILE = "/mnt/data/groups_list.txt"
INSIDER_KEYWORDS = ["whitelist", "airdrop", "stealth", "presale", "alpha", "launching", "private sale", "call now", "new drop"]

client = TelegramClient('multi_group_session', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input("Enter Telegram Code: "))

# ✅ Load group usernames from file
def load_groups(file=GROUP_FILE):
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

GROUPS = load_groups()
print("🔁 Scanning Multiple Telegram Groups...")

# ✅ Scan Messages
def scan_group(group):
    try:
        entity = client.get_entity(group)
        history = client(GetHistoryRequest(peer=entity, limit=15, offset_date=None,
                                           offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        for msg in history.messages:
            text = msg.message.lower() if msg.message else ""
            if any(kw in text for kw in INSIDER_KEYWORDS):
                prediction, score = predict_viral_score(text)
                if prediction and score > 80:
                    print(f"\n🚨 Insider Alert from {group}")
                    print(f"🧠 Score: {score}%")
                    print(f"📨 Message: {text[:180]}\n")
    except Exception as e:
        print(f"❌ Error scanning {group}: {e}")

# 🔁 Main loop
def run_insider_loop():
    while True:
        print("\n🔍 Starting Insider Group Scan...\n")
        for group in GROUPS:
            scan_group(group)
        print("⏳ Sleeping 10 minutes...")
        time.sleep(600)

if __name__ == "__main__":
    run_insider_loop()
