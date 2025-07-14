import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv("data/processed_data/processed_skills_data.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower()

# Load trained model and vectorizer
model = joblib.load("data/models/career_recommendation_model.pkl")
vectorizer = joblib.load("data/models/vectorizer.pkl")
label_encoder = joblib.load("data/models/label_encoder.pkl")  # Load label encoder

# Transform skills text data
X = vectorizer.transform(df["skills"])
y = label_encoder.transform(df["job title"])  # Encode job titles to match training format

# Split data for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Predict using the trained model
y_pred = model.predict(X_test)

# Convert predictions back to original job titles
y_pred_decoded = label_encoder.inverse_transform(y_pred)
y_test_decoded = label_encoder.inverse_transform(y_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Model Accuracy: {accuracy:.4f}")

print("\n📊 Classification Report:\n", classification_report(y_test_decoded, y_pred_decoded))
