# 📦 insider_reels_scanner.py - GOD MODE Reel Intelligence
import requests
import time
import re
import datetime
from ai_trainer import predict_viral_score, train_from_insider_targets

# === CONFIG ===
KEYWORDS = [
    "100x", "crypto alpha", "insider group", "meme gem", "whale buy", "prelaunch", "airdrop",
    "link in bio", "dm me", "telegram group", "crypto leak", "next pepe", "new gem"
]

SAVE_FILE = "insider_targets.txt"
GROUP_LINKS_FILE = "extracted_group_links.txt"
SEARCH_INTERVAL = 900  # 15 minutes
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_API_KEY = "AIzaSyBOJITOwYL4zUg3i8-rSddPC0yX49gVV1w"  # 🔐 Your YouTube Data API Key

# === Utility ===
def save_insider_hit(title, url, score):
    with open(SAVE_FILE, "a") as f:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{now}] SCORE: {score}% | {title}\n🔗 {url}\n\n")

def extract_group_links(text):
    links = re.findall(r"(https?://t\.me/[^\s]+|https?://discord\.gg/[^\s]+)", text)
    return links

def save_group_links(links):
    with open(GROUP_LINKS_FILE, "a") as f:
        for link in links:
            f.write(link + "\n")

# === Main Search + AI Classifier ===
def search_youtube(keyword):
    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "maxResults": 10,
        "order": "date",
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=10)
        data = response.json()

        for item in data.get("items", []):
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            video_id = item["id"]["videoId"]
            url = f"https://youtube.com/watch?v={video_id}"
            text = f"{title} {description}"

            # ✅ AI Classifier
            prediction, score = predict_viral_score(text)

            if prediction == 1 and score >= 80:
                print(f"🔥 INSIDER HIT [{score}%]: {title}\n🔗 {url}")
                save_insider_hit(title, url, score)

            elif re.search(r"dm me|link in bio|telegram", text.lower()):
                print(f"🚨 Flagged Phrase: {title}\n🔗 {url}")
                save_insider_hit(title, url, score)

            # 🔗 Extract Group Links
            all_text = title + description
            links = extract_group_links(all_text)
            if links:
                save_group_links(links)

    except Exception as e:
        print(f"❌ YouTube fetch error: {e}")

# === 24/7 Loop ===
def run_reel_sniper():
    print("\n🎥 Insider Reel Sniper Activated (GOD MODE)")
    while True:
        for keyword in KEYWORDS:
            print(f"\n🔍 Searching: {keyword}")
            search_youtube(keyword)

        # 🧠 Train AI Brain from latest hits
        try:
            train_from_insider_targets(SAVE_FILE)
        except Exception as e:
            print(f"⚠️ AI Training error: {e}")

        print(f"\n⏳ Sleeping {SEARCH_INTERVAL // 60} minutes...")
        time.sleep(SEARCH_INTERVAL)

# === Run Directly ===
if __name__ == "__main__":
    run_reel_sniper()
