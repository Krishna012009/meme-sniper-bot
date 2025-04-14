from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from ai_trainer import predict_viral_score  # 🧠 Add this

api_id = 24339763
api_hash = "9a3fadf2e761e921546a00b565ccec2e"
phone_number = "+916399813966"

client = TelegramClient('sniper_session', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input("Enter code: "))

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
