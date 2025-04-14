import requests
from bs4 import BeautifulSoup

def scrape_twitter(keyword):
    url = f"https://nitter.kavin.rocks/search?f=tweets&q={keyword}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    tweets = [t.text.strip() for t in soup.select(".tweet-content")]
    return tweets[:10]  # Return top 10 latest tweets
