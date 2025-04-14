# 📦 reddit_praw_scanner.py using Reddit API (praw)
import praw
import re

# ✅ Reddit API credentials
REDDIT_CLIENT_ID = "QNYgB_mZJNWpYPqEnd_GAg"
REDDIT_SECRET = "7DuQqpDsEynwb41i7vqo3VSmQZYEAw"
REDDIT_USER_AGENT = "MemeSniperBot/0.1 by commander"

# ✅ Subreddits and Keywords
SUBREDDITS = ["cryptomoonshots", "shitcoin", "satoshistreetbets"]
SNIPE_KEYWORDS = [
    "100x", "gem", "low", "launch", "new", "coin", "meme", "airdrop",
    "🚀", "alpha", "buy", "presale", "pump"
]

# 🔧 Create Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# 🔍 Fetch new posts
def fetch_reddit_trends():
    results = []
    for sub in SUBREDDITS:
        print(f"🔍 Scanning r/{sub}...")
        try:
            for post in reddit.subreddit(sub).new(limit=25):
                title = post.title.lower()
                print(f"[TITLE] {title}")
                if any(re.search(rf"\b{re.escape(word)}\b", title) for word in SNIPE_KEYWORDS):
                    results.append({"title": post.title, "url": post.url, "permalink": f"https://reddit.com{post.permalink}"})
        except Exception as e:
            print(f"❌ Error fetching r/{sub}: {e}")
    return results

# 🔧 Test run
if __name__ == "__main__":
    hits = fetch_reddit_trends()
    for i, post in enumerate(hits):
        print(f"\n🔥 Reddit Hit #{i+1}: {post['title']}\n🔗 {post['permalink']}")
