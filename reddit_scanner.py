import requests
import re
from ai_trainer import predict_viral_score  # 🧠 Add this

SUBREDDITS = ["cryptomoonshots", "shitcoin", "satoshistreetbets"]
SNIPE_KEYWORDS = ["100", "gem", "low", "launch", "new", "coin", "meme", "airdrop", "🚀", "alpha", "buy", "presale", "pump"]

def fetch_reddit_trends():
    results = []
    for sub in SUBREDDITS:
        url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={sub}&sort=desc&limit=20"
        try:
            r = requests.get(url, timeout=10)
            posts = r.json().get("data", [])

            for post in posts:
                title = post.get("title", "").lower()
                pred, score = predict_viral_score(title)
                if pred == 1 and score >= 80:
                    if any(re.search(rf"\b{re.escape(word)}\b", title) for word in SNIPE_KEYWORDS):
                        permalink = post.get("permalink", "")
                        print(f"🧠 Reddit VIRAL ({score}%): {title}")
                        results.append({
                            "title": title,
                            "url": f"https://reddit.com{permalink}"
                        })
                else:
                    print(f"⏭️ Skipped Reddit ({score}%): {title[:60]}")

        except Exception as e:
            print(f"❌ Reddit fetch error from r/{sub}: {e}")

    return results

# 🔧 Test
if __name__ == "__main__":
    hits = fetch_reddit_trends()
    for i, post in enumerate(hits):
        print(f"🔥 Reddit Hit #{i+1}: {post['title'][:100]}\n🔗 {post['url']}\n")
