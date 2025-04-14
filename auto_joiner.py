# 📦 auto_joiner.py – Telegram Group Auto-Joiner (GOD MODE)
from telethon.sync import TelegramClient
from telethon.errors import UserAlreadyParticipantError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
import re
import time

# === Your Telegram Credentials ===
api_id = 24339763
api_hash = "9a3fadf2e761e921546a00b565ccec2e"
phone_number = "+916399813966"

# === Initialize client
client = TelegramClient('auto_join_session', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input("Enter Telegram Code: "))

# === Load Group Links
def load_links(file="extracted_group_links.txt"):
    with open(file, "r") as f:
        return list(set([line.strip() for line in f if "t.me" in line]))

# === Join Logic
def join_group(link):
    try:
        print(f"🔗 Trying to join: {link}")
        if "joinchat" in link or "+" in link:
            # Private invite hash
            invite_hash = link.split("/")[-1].replace("+", "")
            client(ImportChatInviteRequest(invite_hash))
        else:
            # Public group
            username = link.split("/")[-1]
            client(JoinChannelRequest(username))
        print(f"✅ Joined: {link}")
        return True
    except UserAlreadyParticipantError:
        print(f"🟢 Already a member: {link}")
    except Exception as e:
        print(f"❌ Failed to join: {link} | Reason: {e}")
    return False

# === MAIN EXECUTION
if __name__ == "__main__":
    links = load_links()
    print(f"📥 {len(links)} group links loaded.")

    for link in links:
        join_group(link)
        time.sleep(5)  # ⏳ Sleep between joins to avoid flood control

    print("✅ Auto Joiner Completed.")
