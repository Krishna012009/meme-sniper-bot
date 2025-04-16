# 📦 ai_trainer.py — GOD MODE AI BRAIN V2

import pandas as pd
import os
import re
import schedule
import time
import threading
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# === GLOBAL AI ENGINE
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
model = RandomForestClassifier(n_estimators=150, random_state=42)

# === Dataset Path
DATASET_PATH = "ai_training_dataset.csv"

# === Clean Message Function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|t\.me\S+", "", text)  # Remove links
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.strip()

# === Load + Train Model
def train_from_file(csv_file=DATASET_PATH):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"❌ File missing: {csv_file}")
    
    df = pd.read_csv(csv_file)
    if "message" not in df.columns or "viral" not in df.columns:
        raise ValueError("Dataset must contain 'message' and 'viral' columns")

    df["message"] = df["message"].astype(str).apply(clean_text)
    X = vectorizer.fit_transform(df["message"])
    y = df["viral"]
    model.fit(X, y)

    print(f"🧠 GOD MODE AI Brain trained on {len(df)} samples 🚀")

# === Initial Training
train_from_file()

# === Predict Viral Score
def predict_viral_score(message):
    clean_msg = clean_text(message)
    vector = vectorizer.transform([clean_msg])
    pred = model.predict(vector)[0]
    prob = model.predict_proba(vector)[0][1]
    score = round(prob * 100, 2)
    return pred, score

# === Auto-Retrain Every 2 Hours
def retrain_every_2_hours():
    schedule.every(2).hours.do(train_from_file)
    while True:
        schedule.run_pending()
        time.sleep(60)

# === Launch Retrain Thread
threading.Thread(target=retrain_every_2_hours, daemon=True).start()

# === Manual Tester
if __name__ == "__main__":
    test_msg = "🚀 Alpha leak! Prelaunch stealth meme coin, LP locked, whale call!"
    pred, score = predict_viral_score(test_msg)
    emoji = "🔥" if pred else "⚠️"
    print(f"{emoji} Prediction: {'VIRAL' if pred else 'Not Viral'} — Score: {score}%")
