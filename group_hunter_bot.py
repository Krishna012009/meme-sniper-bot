# 📦 group_hunter_bot.py - GOD MODE: Auto Telegram Group Discovery + Joiner
import re
import requests
import time
from bs4 import BeautifulSoup
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

# === TELEGRAM CREDENTIALS ===
api_id = 24339763
api_hash = "9a3fadf2e761e921546a00b565ccec2e"
phone_number = "+916399813966"

client = TelegramClient("auto_group_hunter", api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input("Enter Telegram Code: "))

# === INSIDER KEYWORDS ===
KEYWORDS = [
    "100x", "crypto alpha", "insider group", "meme gem", "whale buy",
    "prelaunch", "airdrop", "link in bio", "dm me", "telegram group",
    "crypto leak", "next pepe", "new gem", "low mcap"
]

# === SEARCH SOURCES ===
SEARCH_URLS = [
    "https://www.google.com/search?q=telegram+crypto+alpha+group",
    "https://www.google.com/search?q=100x+meme+coin+telegram+group",
    "https://www.google.com/search?q=crypto+airdrop+telegram+leak",
]

# === UTILITY ===
def fetch_page_links(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = re.findall(r"https://t\.me/[a-zA-Z0-9_]+", soup.get_text())
        return list(set(links))
    except Exception as e:
        print(f"❌ Failed to fetch: {url} => {e}")
        return []

# === MAIN FUNCTION ===
def hunt_and_join():
    print("\n🧠 Auto Telegram Group Hunter Running...")
    found_groups = set()

    for url in SEARCH_URLS:
        links = fetch_page_links(url)
        for link in links:
            if link in found_groups:
                continue

            print(f"🔗 Found potential group: {link}")
            username_match = re.search(r"https://t\.me/([a-zA-Z0-9_]+)", link)
            if username_match:
                username = username_match.group(1)
                try:
                    client(JoinChannelRequest(username))
                    print(f"✅ Joined group: {username}")
                    found_groups.add(link)
                    with open("joined_groups.txt", "a") as f:
                        f.write(f"{link}\n")
                except Exception as e:
                    print(f"❌ Failed to join {username}: {e}")
            time.sleep(2)

# === LOOP FOREVER ===
if __name__ == "__main__":
    while True:
        hunt_and_join()
        print("⏳ Sleeping for 15 minutes...")
        time.sleep(900)  # 15 minutes
