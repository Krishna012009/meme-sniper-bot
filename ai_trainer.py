# 📦 ai_trainer.py — FINAL PHASE: AI BRAIN V2 (Military-Grade Intelligence)

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import os
import schedule
import time
import threading

# === Global AI Engine
vectorizer = CountVectorizer()
model = LogisticRegression()

# === Dataset Path
DATASET_PATH = "ai_training_dataset.csv"

# === Load + Train
def train_from_file(csv_file=DATASET_PATH):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"❌ File missing: {csv_file}")

    df = pd.read_csv(csv_file)
    if "message" not in df.columns or "viral" not in df.columns:
        raise ValueError("Dataset must contain 'message' and 'viral' columns")

    X = vectorizer.fit_transform(df["message"].astype(str))
    y = df["viral"]
    model.fit(X, y)

    print(f"🧠 AI Brain trained on {len(df)} entries from {csv_file}")

# === Initial Training
train_from_file()

# === Prediction
def predict_viral_score(message):
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)
    probability = model.predict_proba(vector)
    return prediction[0], round(probability[0][1] * 100, 2)

# === Schedule Retraining (Every 2 Hours)
def retrain_every_2_hours():
    schedule.every(2).hours.do(train_from_file)
    while True:
        schedule.run_pending()
        time.sleep(60)

# === Run in Background Thread
threading.Thread(target=retrain_every_2_hours, daemon=True).start()

# === Manual Test (Optional)
if __name__ == "__main__":
    test_msg = "🚀 Alpha leak! Prelaunch stealth meme coin, LP locked, whale call."
    pred, score = predict_viral_score(test_msg)
    print(f"Prediction: {'VIRAL' if pred else 'Not Viral'} ({score}%)")
