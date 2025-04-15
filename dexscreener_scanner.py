import requests
import time
from datetime import datetime

# 🧠 Hyper-Intelligent DexScreener Scanner V2

CHAINS = [
    'ethereum', 'bsc', 'arbitrum', 'optimism', 'polygon', 'base', 'avalanche', 'solana'
]

DEXSCREENER_API = 'https://api.dexscreener.com/latest/dex/pairs/'

# Filters to apply
MIN_VOLUME_USD = 50000
MIN_LIQUIDITY_USD = 10000
MAX_AGE_MINUTES = 60


def fetch_trending_pairs():
    print("\n🧪 Fetching viral trending pairs from DexScreener...")
    viral_tokens = []

    for chain in CHAINS:
        url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            pairs = data.get('pairs', [])

            for pair in pairs:
                try:
                    if not all(k in pair for k in ('pairCreatedAt', 'liquidity', 'volume', 'url')):
                        continue

                    created = datetime.fromtimestamp(pair['pairCreatedAt'] / 1000)
                    age_minutes = (datetime.utcnow() - created).total_seconds() / 60
                    
                    volume_usd = float(pair['volume']['h1'])
                    liquidity_usd = float(pair['liquidity']['usd'])

                    if (volume_usd >= MIN_VOLUME_USD and
                        liquidity_usd >= MIN_LIQUIDITY_USD and
                        age_minutes <= MAX_AGE_MINUTES):

                        token_info = {
                            'name': pair.get('baseToken', {}).get('name', 'N/A'),
                            'symbol': pair.get('baseToken', {}).get('symbol', 'N/A'),
                            'dex_url': pair.get('url'),
                            'volume': volume_usd,
                            'liquidity': liquidity_usd,
                            'age_min': round(age_minutes, 2),
                            'chain': chain
                        }
                        viral_tokens.append(token_info)

                except Exception as e:
                    print(f"⚠️ Error parsing token: {e}")

        except Exception as e:
            print(f"❌ DexScreener error for {chain}: {e}")

    return viral_tokens


if __name__ == "__main__":
    tokens = fetch_trending_pairs()
    print(f"\n🚀 Found {len(tokens)} viral token(s) across chains:")
    for t in tokens:
        print(f"➡️ [{t['chain'].upper()}] {t['symbol']} | 💧 ${t['liquidity']:,} | 🔄 ${t['volume']:,} | 🕒 {t['age_min']} min old")
        print(f"   📈 {t['dex_url']}\n")
