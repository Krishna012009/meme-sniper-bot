import re
import datetime
import threading
import time
import requests
from bs4 import BeautifulSoup
import schedule
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from ai_trainer import predict_viral_score

# ✅ Your Bot Token
TOKEN = "8104354787:AAHyyCUEX-gpZzvbQfub_rT-lrdGn9q6ipM"

# === 🔐 Persistent Seen Tokens ===
def load_seen_tokens():
    try:
        with open("seen_tokens.txt", "r") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def save_token(token):
    with open("seen_tokens.txt", "a") as f:
        f.write(token + "\n")

seen_tokens = load_seen_tokens()

# ✅ Google Sheets Auth
creds = Credentials.from_service_account_file(
    "sniperbotsheets-456110-1d906bbd0516.json",
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)
client = gspread.authorize(creds)
sheet = client.open("SniperBotLogs").sheet1
print("✅ Connected to Google Sheets")

# ✅ Sniper logic every 10 minutes (can expand later)
def run_sniper_loop():
    print("🛰️ Running scheduled sniper scan...")
    token_address = "0x123456789abcdef123456789abcdef12345678"
    chart_link = f"https://dexscreener.com/ethereum/{token_address}"
    if token_address not in seen_tokens:
        paper_trade(token_address, chart_link)
        seen_tokens.add(token_address)
        save_token(token_address)

# ✅ Background loop
def start_schedule():
    schedule.every(10).minutes.do(run_sniper_loop)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=start_schedule, daemon=True).start()
print("🔁 Sniper Auto-Scan activated — running every 10 mins.")

# ✅ Telegram Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat = update.effective_chat

    # 🧠 AI Predict
    prediction, viral_score = predict_viral_score(text)

    if prediction == 1 and viral_score >= 80:
        await context.bot.send_message(
            chat_id=chat.id,
            text=f"🧠 *Viral Message Detected!*\nScore: `{viral_score}%`\n\nTriggering Sniper Logic...",
            parse_mode='Markdown'
        )

        # Extract token + chart
        token_match = re.search(r'0x[a-fA-F0-9]{40}', text)
        chart_match = re.search(r'(https?://dexscreener\.com/\S+)', text)

        if token_match and chart_match:
            token_address = token_match.group(0)
            chart_link = chart_match.group(1)

            if token_address in seen_tokens:
                await context.bot.send_message(
                    chat_id=chat.id,
                    text="⏸️ Token already logged earlier. Skipping duplicate."
                )
                return

            # Log trade
            paper_trade(token_address, chart_link)
            seen_tokens.add(token_address)
            save_token(token_address)

            await context.bot.send_message(
                chat_id=chat.id,
                text=f"📒 Token logged for paper trade!\n\n*Token:* `{token_address}`\n[Chart Link]({chart_link})",
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        else:
            await context.bot.send_message(
                chat_id=chat.id,
                text="⚠️ Viral but no token or chart link found."
            )
    else:
        print(f"⏭️ Message skipped - Viral Score: {viral_score}%")

# ✅ Start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Sniper Bot Activated and Listening!")

# ✅ Launch bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 Bot is live. Waiting for Telegram messages...")
app.run_polling()
