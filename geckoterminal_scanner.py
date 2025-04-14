# 📦 geckoterminal_scanner.py — Upgraded Hybrid Version
import requests
import time

CHAINS = ["eth", "bsc", "base", "arbitrum", "solana"]
GECKO_BASE = "https://api.geckoterminal.com/api/v2/networks"
HOT_PAIRS = []

def fetch_gecko_trends():
    global HOT_PAIRS
    HOT_PAIRS = []
    print("🧪 Running GeckoTerminal Scanner Test...")

    for chain in CHAINS:
        print(f"🔍 Scanning GeckoTerminal for {chain.upper()}...")

        url = f"{GECKO_BASE}/{chain}/trending_pools"

        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 404:
                print(f"⚠️ GeckoTerminal: {chain.upper()} not available (404 Skipped)")
                continue
            elif r.status_code != 200:
                print(f"⏳ Retrying {chain.upper()} due to status {r.status_code}...")
                time.sleep(3)
                r = requests.get(url, timeout=10)

            data = r.json()
            pools = data.get("data", [])

            for pool in pools:
                attributes = pool.get("attributes", {})
                token_name = attributes.get("base_token", {}).get("name")
                token_address = attributes.get("base_token", {}).get("address")
                change = attributes.get("price_change_percentage", {}).get("m5", "0")
                url = f"https://www.geckoterminal.com/{chain}/pools/{pool.get('id')}"

                if float(change) > 20:
                    HOT_PAIRS.append({
                        "name": token_name,
                        "token": token_address,
                        "url": url,
                        "change_5min": change
                    })

        except Exception as e:
            print(f"❌ GeckoTerminal Error ({chain}): {e}")

    return HOT_PAIRS

# 🔧 TEST
if __name__ == "__main__":
    hot = fetch_gecko_trends()
    if not hot:
        print("⚠️ No hot tokens detected.")
    else:
        for i, token in enumerate(hot, 1):
            print(f"🔥 {i}. {token['name']} | Change: {token['change_5min']}% | Token: {token['token']}")
            print(f"🔗 {token['url']}\n")
