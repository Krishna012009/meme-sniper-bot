import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# 🧠 Sample AI Training Data
training_data = [
    {"message": "🚀 New gem just launched! 100x potential! #meme", "viral": 1},
    {"message": "New stealth launch, LP locked, moon soon", "viral": 1},
    {"message": "This coin is launching... no info", "viral": 0},
    {"message": "Pump group is trying this", "viral": 0},
    {"message": "Low mcap gem alert, just dropped!", "viral": 1},
    {"message": "Alpha call from insider, early buy", "viral": 1},
    {"message": "Some random crypto tweet", "viral": 0},
]

df = pd.DataFrame(training_data)

# Step 1: Keyword Vectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["message"])
y = df["viral"]

# Step 2: Train Logistic Regression Model
model = LogisticRegression()
model.fit(X, y)

# Step 3: Predict new messages
def predict_viral_score(message):
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)
    probability = model.predict_proba(vector)
    return prediction[0], round(probability[0][1] * 100, 2)

# ✅ Test (Optional)
if __name__ == "__main__":
    msg = "🔥 New gem just dropped! LP locked! #100x"
    prediction, score = predict_viral_score(msg)
    print(f"Prediction: {'VIRAL' if prediction else 'Not viral'} ({score}%)")
