# utils.py 🚀 — Token Persistence Utility

def save_token(token):
    with open("seen_tokens.txt", "a") as f:
        f.write(token + "\n")

def load_seen_tokens():
    try:
        with open("seen_tokens.txt", "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()
