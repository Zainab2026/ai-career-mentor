import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

# Load cleaned dataset
df = pd.read_csv("data/processed_data/processed_skills_data.csv")

# Convert column names to lowercase for consistency
df.columns = df.columns.str.lower()

# Debugging: Print column names
print("🔍 Columns in dataset (lowercased):", df.columns.tolist())

# Ensure "job title" exists (lowercase)
if "job title" not in df.columns:
    raise ValueError("❌ ERROR: 'job title' column is missing in processed_skills_data.csv!")

# Proceed with model training
models_path = "data/models/"
os.makedirs(models_path, exist_ok=True)

label_encoder = LabelEncoder()
df["job title"] = label_encoder.fit_transform(df["job title"])
joblib.dump(label_encoder, models_path + "label_encoder.pkl")

# Vectorize skills text
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["skills"])
y = df["job title"]

joblib.dump(vectorizer, models_path + "vectorizer.pkl")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, models_path + "career_recommendation_model.pkl")

print("✅ Model training completed. Model saved in:", models_path)
