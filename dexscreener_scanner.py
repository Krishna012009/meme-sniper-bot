import requests

def fetch_dex_trends():
    print("🧪 Fetching viral trending pairs from DexScreener...")

    try:
        url = "https://api.dexscreener.com/latest/trending"  # ⬅️ New endpoint
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"❌ DexScreener Status Error: {r.status_code}")
            return []

        data = r.json()
        hot = []

        for section in data.get("data", []):
            for pair in section.get("pairs", []):
                try:
                    base = pair["baseToken"]
                    name = base.get("name", "Unknown")
                    symbol = base.get("symbol", "")
                    token = pair.get("pairAddress")
                    chart = pair.get("url", "")
                    change = float(pair.get("priceChange", {}).get("m5", 0))
                    vol = float(pair.get("volume", {}).get("h24", 0))
                    lp = float(pair.get("liquidity", {}).get("usd", 0))
                    chain = pair.get("chainId", "unknown")

                    if change > 20 and vol > 5000 and lp > 1000:
                        hot.append({
                            "name": f"{name} ({symbol})",
                            "token": token,
                            "url": chart,
                            "change_5min": change,
                            "volume": vol,
                            "lp": lp,
                            "chain": chain
                        })
                except:
                    continue

        return hot

    except Exception as e:
        print(f"❌ DexScreener Exception: {e}")
        return []

if __name__ == "__main__":
    coins = fetch_dex_trends()
    if not coins:
        print("⚠️ No trending tokens right now.")
    else:
        for c in coins:
            print(f"\n🔥 {c['name']} [{c['chain'].upper()}]")
            print(f"Token: {c['token']} | Change: {c['change_5min']}%")
            print(f"📈 Chart: {c['url']}")
            print(f"💧 LP: ${c['lp']:.0f} | 📊 Volume: ${c['volume']:.0f}")
