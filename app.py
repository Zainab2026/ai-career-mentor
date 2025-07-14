
import streamlit as st
from components.chatbot import chatbot_page
from components.networking import networking_ui
from components.resume_upload import resume_upload_ui
from training.predict import get_job_recommendation
from components.youtube_search import youtube_search_ui

st.set_page_config(page_title="AI Career Mentor", layout="wide")

# ✅ Ensure session state exists
if "is_mobile" not in st.session_state:
    st.session_state.is_mobile = False  # Default to Desktop Mode

# ✅ Toggle Button for Mobile/Desktop Mode
if st.sidebar.button("📱 Switch Mobile/Desktop Mode"):
    st.session_state.is_mobile = not st.session_state.is_mobile  # Toggle state

# ✅ Apply Responsive Layout
if st.session_state.is_mobile:
    st.write("📱 **Mobile Mode Enabled**")
    st.markdown("<style>body { font-size: 16px; }</style>", unsafe_allow_html=True)
else:
    st.write("💻 **Desktop Mode Enabled**")

# ✅ Main Content
PAGES = {
    "💬 Chatbot": chatbot_page,
    "🤝 Networking": networking_ui,
    "📂 Resume Upload": resume_upload_ui,
    "🎥 YouTube Career Search": youtube_search_ui,
    "🏆 Job Prediction": "job_prediction"  # Placeholder for handling Job Prediction separately
}

st.sidebar.title("📍 Navigation")
selection = st.sidebar.radio("Go to:", list(PAGES.keys()))

# 🎯 **Handle Job Prediction Section**
if selection == "🏆 Job Prediction":
    st.title("🏆 AI-Powered Career Recommendation")
    skills_input = st.text_area("📝 **Enter Your Skills (comma-separated):**", placeholder="e.g., Python, Machine Learning, SQL")
    if st.button("🔍 Get Career Prediction"):
        if skills_input.strip():
            # Pass the skills input as a string
            result = get_job_recommendation(skills_input)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"🏅 **Recommended Job Role:** {result['job_title']}  \n🎯 **Confidence Score:** {result['confidence']}%")
                # 🔹 Salary & Demand Insights Section
                st.markdown("---")
                st.subheader("💰 Salary & Demand Insights")
                st.markdown(f"**💵 Salary Range:** {result['avg_salary']}" )
                st.markdown(f"**📈 Demand Level:** {result['demand_level']}")
                # 📊 Market Insights Section
                st.markdown("---")
                st.subheader("📊 Market Insights")
                st.markdown(result["market_insights"], unsafe_allow_html=True)
                # 🚀 Skills Improvement Section
                st.markdown("---")
                st.subheader("🚀 Key Skills to Improve")
                st.write(result["skills_improvement"])
                # 🔄 Alternative Career Paths Section
                st.markdown("---")
                st.subheader("🎯 Alternative Career Paths")
                if result["alternative_jobs"]:
                    st.markdown(result["alternative_jobs"], unsafe_allow_html=True)
                else:
                    st.write("⚠ No strong alternative career matches found.")
        else:
            st.warning("⚠ **Please enter your skills to get a career recommendation.**")
else:
    if PAGES[selection] != "job_prediction":  # Check if it's not the placeholder
        PAGES[selection]()  # ✅ Correctly call UI functions

# ✅ Footer - Made by Zainab (LinkedIn) at the bottom
st.markdown("<style>body { padding-bottom: 60px; }</style>", unsafe_allow_html=True)
st.markdown(
    "<p style='position: fixed; bottom: 10px; width: 100%; text-align: center; font-size: 14px; color: blue; text-decoration: underline;'>Made by <a href='https://www.linkedin.com/in/zainab-khushrez-a63154254/' target='_blank'>Zainab🔥</a></p>",
    unsafe_allow_html=True
)
