import re
import time
import threading
import schedule
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from ai_trainer import predict_viral_score  # 🧠 Add this

# === 🔐 Secrets ===
TOKEN = "8104354787:AAHyyCUEX-gpZzvbQfub_rT-lrdGn9q6ipM"
GOOGLE_CREDS = "sniperbotsheets-456110-1d906bbd0516.json"
TELEGRAM_API_ID = 24339763
TELEGRAM_API_HASH = "9a3fadf2e761e921546a00b565ccec2e"
PHONE_NUMBER = "+916399813966"

# === 📄 Google Sheets Auth ===
creds = Credentials.from_service_account_file(GOOGLE_CREDS, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])
client = gspread.authorize(creds)
sheet = client.open("SniperBotLogs").sheet1  # Make sure this sheet exists
print("✅ Connected to Google Sheets")

# === 📦 Seen Tokens ===
def load_seen_tokens():
    try:
        with open("seen_tokens.txt", "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_token(token):
    with open("seen_tokens.txt", "a") as f:
        f.write(token + "\n")

seen_tokens = load_seen_tokens()

# === 🛰️ DEXSCREENER SETUP ===
CHAINS = ['ethereum', 'bsc', 'arbitrum', 'optimism', 'polygon', 'base', 'avalanche', 'solana']
MIN_VOLUME_USD = 50000
MIN_LIQUIDITY_USD = 10000
MAX_AGE_MINUTES = 60

def fetch_trending_pairs():
    print("\n🧪 Fetching from DexScreener...")
    viral_tokens = []
    for chain in CHAINS:
        try:
            url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}"
            data = requests.get(url, timeout=10).json()
            for pair in data.get("pairs", []):
                if not all(k in pair for k in ('pairCreatedAt', 'liquidity', 'volume', 'url')):
                    continue
                age = (datetime.utcnow() - datetime.fromtimestamp(pair['pairCreatedAt'] / 1000)).total_seconds() / 60
                if age > MAX_AGE_MINUTES:
                    continue
                volume = float(pair['volume']['h1'])
                liquidity = float(pair['liquidity']['usd'])
                if volume >= MIN_VOLUME_USD and liquidity >= MIN_LIQUIDITY_USD:
                    token = {
                        'symbol': pair['baseToken']['symbol'],
                        'address': pair['pairAddress'],
                        'chart': pair['url'],
                        'volume': volume,
                        'liquidity': liquidity,
                        'age': round(age, 2),
                        'chain': chain
                    }
                    viral_tokens.append(token)
        except Exception as e:
            print(f"❌ DexScreener error: {e}")
    return viral_tokens

# === ✅ Extract mock price from dexscreener link ===
def get_mock_price(dex_url):
    try:
        response = requests.get(dex_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        match = re.search(r"\$([0-9.]+)", text)
        return float(match.group(1)) if match else 0.0001
    except Exception as e:
        print(f"[ERROR] Failed to extract price: {e}")
        return 0.0001

# === 🧪 Paper Trade Logic ===
def paper_trade(token, chart):
    print(f"📈 New Trade Detected:\nToken: {token}\nChart: {chart}")
    mock_price = get_mock_price(chart)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([now, "PAPER_TRADE", token, chart, mock_price, "Gas: 0.002 ETH", "Not Bought"])
    print(f"📒 Logged Paper Trade: {token} @ ${mock_price:.6f}")

# === 🔁 Scheduled Sniper Loop ===
def run_sniper_loop():
    print("🛰️ Running scheduled sniper scan...")
    tokens = fetch_trending_pairs()
    for t in tokens:
        token_address = t['address']
        if token_address not in seen_tokens:
            paper_trade(token_address, t['chart'])
            seen_tokens.add(token_address)
            save_token(token_address)
            print(f"📒 Logged {t['symbol']} ({token_address})")

def start_schedule():
    schedule.every(10).minutes.do(run_sniper_loop)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=start_schedule, daemon=True).start()
print("🔁 Sniper Auto-Scan activated — running every 10 mins.")

# === 📩 Telegram Handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat = update.effective_chat
    prediction, score = predict_viral_score(text)
    if prediction == 1 and score >= 80:
        await context.bot.send_message(chat_id=chat.id, text=f"🧠 Viral Score: {score}% — Triggering sniper...")
        token_match = re.search(r'0x[a-fA-F0-9]{40}', text)
        chart_match = re.search(r'(https?://dexscreener\.com/\S+)', text)
        if token_match and chart_match:
            token = token_match.group(0)
            chart = chart_match.group(1)
            if token not in seen_tokens:
                paper_trade(token, chart)
                seen_tokens.add(token)
                save_token(token)
                await context.bot.send_message(chat_id=chat.id, text=f"✅ Token logged!\n{chart}")
            else:
                await context.bot.send_message(chat_id=chat.id, text="⏸️ Already logged earlier.")
        else:
            await context.bot.send_message(chat_id=chat.id, text="⚠️ No token/chart found in viral message.")
    else:
        print(f"⏭️ Skipped. Viral Score: {score}%")

# === 🔃 /start Command ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Meme Sniper Bot Activated!")

# === 🚀 Launch Bot ===
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("🚀 Bot is live. Waiting for Telegram messages...")
app.run_polling()

# === Telegram Sniper Scanner ===
client = TelegramClient('sniper_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(PHONE_NUMBER)
    client.sign_in(PHONE_NUMBER, input("Enter code: "))

def fetch_latest_messages(group_username, limit=10):
    group = client.get_entity(group_username)
    history = client(
        GetHistoryRequest(peer=group,
                          limit=limit,
                          offset_date=None,
                          offset_id=0,
                          max_id=0,
                          min_id=0,
                          add_offset=0,
                          hash=0))

    filtered = []
    for msg in history.messages:
        if msg.message:
            pred, score = predict_viral_score(msg.message)
            if pred == 1 and score >= 80:
                print(f"🧠 Telegram VIRAL ({score}%) → {msg.message[:80]}")
                filtered.append(msg.message)
            else:
                print(f"⏭️ Skipped ({score}%) → {msg.message[:60]}")
    return filtered

# ✅ TEST RUN
if __name__ == "__main__":
    print("🚀 Telegram Sniper Scanner Online...")
    group = "@krishnamemecoinsniperbot"
    messages = fetch_latest_messages(group)
    for msg in messages:
        print("📨", msg[:120])


