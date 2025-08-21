def get_job_recommendation(skills_input):
    """
    Given a comma-separated string of skills, return a dictionary with job recommendation and insights.
    """
    try:
        model, vectorizer = load_model()
        market_data = load_market_data()
        skills_list = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
        if not skills_list:
            return {"error": "No skills provided."}
        skills_vectorized = vectorizer.transform([" ".join(skills_list)])
        predicted_job_id = model.predict(skills_vectorized)[0]
        if "Job Id" not in market_data.columns or "Job Title" not in market_data.columns:
            return {"error": "Required columns missing in market data."}
        job_row = market_data[market_data["Job Id"] == predicted_job_id]
        if job_row.empty:
            return {"error": "No matching job found for the prediction."}
        predicted_job_title = job_row["Job Title"].values[0]
        confidence = float(model.predict_proba(skills_vectorized).max() * 100)
        # Market insights
        market_insights_row = get_market_insights(predicted_job_title, market_data)
        avg_salary = market_insights_row["Salary Range"] if market_insights_row is not None and "Salary Range" in market_insights_row else "N/A"
        demand_level = market_insights_row["Demand Level"] if market_insights_row is not None and "Demand Level" in market_insights_row else "N/A"
        market_insights_html = ""
        if market_insights_row is not None:
            for col in market_insights_row.index:
                if col not in ["Job Title", "Salary Range", "Demand Level", "Job Id"]:
                    market_insights_html += f"<b>{col}:</b> {market_insights_row[col]}<br>"
        # Dummy skills improvement and alternative jobs (customize as needed)
        skills_improvement = "Consider improving your communication, teamwork, and leadership skills."
        alternative_jobs = "<ul><li>Data Analyst</li><li>Business Analyst</li></ul>" if predicted_job_title != "Data Analyst" else "<ul><li>Software Engineer</li><li>Product Manager</li></ul>"
        return {
            "job_title": predicted_job_title,
            "confidence": f"{confidence:.1f}",
            "avg_salary": avg_salary,
            "demand_level": demand_level,
            "market_insights": market_insights_html or "No additional insights available.",
            "skills_improvement": skills_improvement,
            "alternative_jobs": alternative_jobs
        }
    except FileNotFoundError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}
import os
import pickle
import pandas as pd

# Paths to model and vectorizer
MODEL_PATH = "data/models/career_recommendation_model.pkl"
VECTORIZER_PATH = "data/models/vectorizer.pkl"
MARKET_DATA_PATH = "data/market_data.csv"

def load_model():
    """Load the trained model and vectorizer."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Model files not found! Please train the model first using train.py.")

    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
    with open(VECTORIZER_PATH, "rb") as vec_file:
        vectorizer = pickle.load(vec_file)

    print("✅ Model & Vectorizer loaded successfully.")
    return model, vectorizer

def load_market_data():
    """Load market data CSV."""
    if not os.path.exists(MARKET_DATA_PATH):
        raise FileNotFoundError("Market data file not found!")
    
    market_data = pd.read_csv(MARKET_DATA_PATH)
    print("✅ Reference data loaded successfully.")
    return market_data

def get_market_insights(job_title, market_data):
    """Fetch job market insights for the predicted job title."""
    if "Job Title" not in market_data.columns:
        print("\n❌ ERROR: 'Job Title' column missing in market data.")
        exit(1)
    
    job_info = market_data[market_data["Job Title"] == job_title]

    if job_info.empty:
        print("\n⚠ No market insights available for this job title.")
        return None
    
    return job_info.iloc[0]

def main():
    """Main function to predict career recommendation."""
    model, vectorizer = load_model()
    market_data = load_market_data()

    # User input
    skills = input("\n📝 Enter your skills (comma-separated): ")
    skills_list = [s.strip().lower() for s in skills.split(",")]

    # Transform input skills
    skills_vectorized = vectorizer.transform([" ".join(skills_list)])

    # Predict job
    predicted_job_id = model.predict(skills_vectorized)[0]

    # Fetch job title from market data
    if "Job Id" not in market_data.columns or "Job Title" not in market_data.columns:
        print("\n❌ ERROR: Required columns missing in market data.")
        exit(1)

    job_row = market_data[market_data["Job Id"] == predicted_job_id]

    if job_row.empty:
        print("\n⚠ No matching job found for the prediction.")
        exit(1)

    predicted_job_title = job_row["Job Title"].values[0]
    confidence = model.predict_proba(skills_vectorized).max() * 100

    print("\n🎯 Career Recommendation")
    print("=" * 40)
    print(f"🏆 Recommended Job Title: {predicted_job_title}")
    print(f"🔍 Confidence: {confidence:.1f}%")

    # Fetch market insights
    market_insights = get_market_insights(predicted_job_title, market_data)
    if market_insights is not None:
        print(f"💼 Company: {market_insights['Company']}")
        print(f"📍 Location: {market_insights['location']}")
        print(f"💰 Salary Range: {market_insights['Salary Range']}")

if __name__ == "__main__":
    main()
