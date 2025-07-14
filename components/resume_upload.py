
import re
import json
import requests
import streamlit as st
import pdfplumber
import docx
import webbrowser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🔑 API Keys
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL")
GOOGLE_SEARCH_URL = os.getenv("GOOGLE_SEARCH_URL")

# 📌 Resume Analyzer Websites
RESUME_ANALYZERS = {
    "📝 Resumeworded": "https://resumeworded.com/",
    "📊 Jobscan": "https://www.jobscan.co/resume",
    "📄 Zety": "https://zety.com/resume-check",
    "🔍 Enhancv": "https://enhancv.com/resume-check"
}

# 📂 Extract Resume Text
def extract_text_from_resume(uploaded_file):
    """Extracts text from a PDF or DOCX resume."""
    text = ""
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_file.type == "application/vnd.openxmlformat":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraph])
    return text.strip()

# 🔍 AI-Based Resume Analysis
def fetch_resume_analysis(text):
    """Analyzes resume and provides AI feedback using Mistral AI."""
    prompt = f"""
    Analyze the following resume and provide structured feedback with ratings:

    1️⃣ **Clarity & Structure (1-10):** Formatting, readability, and section organization.
    2️⃣ **Skill Relevance (1-10):** Do listed skills match job market needs?
    3️⃣ **Overall Impact (1-10):** How strong is this resume for recruiters?
    4️⃣ **ATS Compatibility (Yes/No):** Is this resume ATS-friendly?
    
    Key improvement suggestions should be provided.

    Resume Content:
    {text}

    **Response Format:**
    - Clarity & Structure: X/10
    - Skill Relevance: X/10
    - Overall Impact: X/10
    - ATS Compatibility: Yes/No
    - Key Improvements:
      - [Improvement 1]
      - [Improvement 2]
    """

    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "mistral-medium", "messages": [{"role": "system", "content": prompt}], "temperature": 0.7}

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        feedback = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No feedback available.")

        # Extract structured ratings
        clarity_match = re.search(r"Clarity & Structure: (\d+)/10", feedback)
        skills_match = re.search(r"Skill Relevance: (\d+)/10", feedback)
        impact_match = re.search(r"Overall Impact: (\d+)/10", feedback)
        ats_match = re.search(r"ATS Compatibility: (Yes|No)", feedback)

        clarity_rating = int(clarity_match.group(1)) if clarity_match else None
        skills_rating = int(skills_match.group(1)) if skills_match else None
        impact_rating = int(impact_match.group(1)) if impact_match else None
        ats_compatible = ats_match.group(1) if ats_match else "N/A"

        # Extract improvement suggestions
        improvements_match = re.search(r"Key Improvements:\n(.*)", feedback, re.DOTALL)
        improvements = improvements_match.group(1).strip() if improvements_match else "No major improvements needed."

        return feedback, clarity_rating, skills_rating, impact_rating, ats_compatible, improvements
    except requests.exceptions.RequestException as e:
        st.error(f"⚠ Error analyzing resume: {e}")
        return "⚠ Error retrieving feedback.", None, None, None, "N/A", ""

# 📌 Streamlit UI - Resume Analysis
def resume_upload_ui():
    st.title("📄 **AI-Powered Resume Analyzer**")

    uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")

        # 📂 Extract text for analysis
        resume_text = extract_text_from_resume(uploaded_file)

        # 🔍 AI-Based Resume Analysis
        with st.container():
            st.subheader("🔍 **AI-Based Resume Feedback**")
            with st.spinner("Analyzing your resume..."):
                feedback, clarity_rating, skills_rating, impact_rating, ats_compatible, improvements = fetch_resume_analysis(resume)
            st.write(feedback)

            # 🎭 **Single** Resume Rating with Color Coding
            def get_color_coded_rating(rating):
                """Returns color-coded rating based on value."""
                if rating >= 8:
                    return f"🟢 **{rating}/10 - Excellent!**"
                elif rating >= 5:
                    return f"🟡 **{rating}/10 - Needs Improvement**"
                else:
                    return f"🔴 **{rating}/10 - Consider Updating**"

            st.subheader("⭐ **Resume Ratings**")
            if clarity_rating:
                st.write(f"📜 **Clarity & Structure:** {get_color_coded_rating(clarity_rating)}")
            if skills_rating:
                st.write(f"🎯 **Skill Relevance:** {get_color_coded_rating(skills_rating)}")
            if impact_rating:
                st.write(f"🚀 **Overall Impact:** {get_color_coded_rating(impact_rating)}")

            if not (clarity_rating or skills_rating or impact_rating):
                st.warning("⚠ Unable to determine ratings. Please review your resume.")

            # ✅ ATS Compatibility Check
            st.subheader("🖥 **ATS Compatibility Check**")
            if ats_compatible == "Yes":
                st.success("✅ This resume is **ATS-friendly**!")
            else:
                st.error("⚠ This resume may **not be ATS-compatible**. Consider using a simple format.")

            # 🔧 Display Improvement Suggestions
            st.subheader("🔧 **Key Improvement Suggestions**")
            st.write(improvements)

        # 📊 Additional Resume Analyzers
        with st.container():
            st.subheader("📊 **More Resume Analyzers**")
            col1, col2 = st.columns(2)
            with col1:
                for name, url in list(RESUME_ANALYZERS.items())[:2]:
                    if st.button(f"🔗 Analyze on {name}"):
                        webbrowser.open(url)
            with col2:
                for name, url in list(RESUME_ANALYZERS.items())[2:]:
                    if st.button(f"🔗 Analyze on {name}"):
                        webbrowser.open(url)

