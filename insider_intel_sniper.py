# 🚀 Insider Intelligence Engine v2.0
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import time, re, csv, os
from ai_trainer import predict_viral_score

# === CONFIG ===
api_id = 24339763
api_hash = "9a3fadf2e761e921546a00b565ccec2e"
phone_number = "+916399813966"
GROUP_FILE = "/mnt/data/groups_list.txt"
SEEN_MESSAGES_FILE = "seen_insider_messages.txt"
LOG_CSV = "insider_logs.csv"
JOINED_GROUPS_FILE = "joined_groups.txt"

INSIDER_KEYWORDS = [
    "whitelist", "airdrop", "stealth", "presale", "alpha", "launch", "private sale", "new gem", "whale", "buy now"
]

client = TelegramClient('multi_group_session', api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input("Enter Telegram Code: "))

# ✅ Load groups from file
def load_groups(file=GROUP_FILE):
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# ✅ Load seen messages (avoid re-scanning)
def load_seen_messages():
    if not os.path.exists(SEEN_MESSAGES_FILE):
        return set()
    with open(SEEN_MESSAGES_FILE, "r") as f:
        return set(line.strip() for line in f)

# ✅ Save seen message ID
def mark_seen(msg_id):
    with open(SEEN_MESSAGES_FILE, "a") as f:
        f.write(str(msg_id) + "\n")

# ✅ Log viral insider calls
def log_insider(msg_id, group, score, text):
    with open(LOG_CSV, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([msg_id, group, score, text[:150]])

# ✅ Extract and auto-save Telegram group links
def extract_and_save_group_links(text):
    links = re.findall(r"https://t\.me/[a-zA-Z0-9_]+", text)
    if links:
        with open(JOINED_GROUPS_FILE, "a") as f:
            for link in links:
                f.write(link + "\n")

# ✅ Main scanner per group
def scan_group(group, seen_messages):
    try:
        entity = client.get_entity(group)
        history = client(GetHistoryRequest(peer=entity, limit=20, offset_date=None,
                                           offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))

        for msg in history.messages:
            if not msg.message: continue
            if msg.id in seen_messages: continue

            text = msg.message.lower()
            if any(kw in text for kw in INSIDER_KEYWORDS):
                prediction, score = predict_viral_score(text)
                if prediction and score >= 80:
                    print(f"\n🚨 Insider Alert from {group}")
                    print(f"🧠 Score: {score}%")
                    print(f"📨 Message: {text[:200]}")
                    log_insider(msg.id, group, score, text)
                    extract_and_save_group_links(text)
            mark_seen(msg.id)

    except Exception as e:
        print(f"❌ Error scanning {group}: {e}")

# 🔁 Main loop
def run_insider_loop():
    groups = load_groups()
    seen = load_seen_messages()

    while True:
        print("\n🔍 Starting Insider Group Scan...")
        for group in groups:
            scan_group(group, seen)
        print("⏳ Sleeping 10 mins...\n")
        time.sleep(600)

if __name__ == "__main__":
    run_insider_loop()
