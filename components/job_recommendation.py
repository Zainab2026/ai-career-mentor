import streamlit as st
from training.predict import predict_career

def job_recommendation_ui():
    st.title("🔍 Job Recommendations")
    
    skills_input = st.text_area("Enter your skills (comma-separated):")
    
    if st.button("Find Jobs"):
        if skills_input:
            results = predict_career(skills_input)
            if results:
                st.success("✅ Career Recommendations:")
                st.write(f"**🏆 Recommended Job:** {results['job_title']}")
                st.write(f"**🔢 Confidence:** {results['confidence']}%")
                st.write(f"**📍 Location:** {results['location']}")
                st.write(f"**💰 Salary Range:** {results['salary']}")
                st.write(f"**🛠 Suggested Skills:** {', '.join(results['suggested_skills'])}")

                st.subheader("🔄 Alternative Careers")
                for job, match in results["alternative_jobs"].items():
                    st.write(f"• {job} (Skill match: {match}%)")

            else:
                st.warning("⚠ No job recommendations found.")
        else:
            st.error("❌ Please enter your skills.")
