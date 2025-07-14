
import requests
import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🔑 API Keys
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# ✅ Fetch Latest Networking Events from Google Search API
def fetch_google_search_results(query, num_results=5):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get("items", [])
        return results[:num_results] if results else []
    else:
        return []

# ✅ Summarize Event Details Using Mistral AI
def summarize_event_details(event_title, event_link):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}

    prompt = (
        f"Visit the event link: {event_link} and summarize its purpose, agenda, and audience in 3 lines."
    )

    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        summary = response.json()["choices"][0]["message"]["content"]
        return f"🎟 **{event_title}**\n📄 {summary}\n🔗 [Event Link]({event_link})"
    else:
        return f"🎟 **{event_title}**\n⚠ Unable to fetch details. Visit: [Click Here]({event_link})"

# ✅ AI-Powered Networking Strategies
def get_ai_networking_insights(profession, location, concern):
    query = f"Best networking strategies for {profession}s in {location} {datetime.today().year}"
    strategy_links = fetch_google_search_results(query, num_results=3)

    if not strategy_links:
        return "⚠ No recent networking strategies found. Try searching manually on LinkedIn or Google."

    formatted_links = "\n".join([f"- {link['title']}: {link['link']}" for link in strategy_links])

    prompt = (
        f"Visit the following links and summarize the latest networking strategies for {profession}s in {location}: \n\n"
        f"{formatted_links}\n\n"
        f"Summarize into 5 actionable points."
    )

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠ Error: Unable to fetch AI-powered strategies."

# ✅ Fetch Networking Insights Using Mistral AI
def get_networking_insights(profession, location, concern):
    """
    Fetches networking events, seminars, and career insights based on user inputs.
    """


    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Provide a list of upcoming networking events, seminars, or career opportunities "
        f"for a {profession} in {location}. Also, offer some general networking strategies "
        f"to address this concern: {concern}."
    )

    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response
        return data["choices"][0]["message"]["content"]
    else:
        return f"⚠ Error: Unable to fetch insights. (Status Code: {response.status_code})"

# ✅ Streamlit UI for Networking Insights
def networking_ui():
    st.title("🤝 Networking & Career Events")

    # User input fields
    profession = st.text_input("Enter Your Profession:", placeholder="e.g., Data Scientist")
    location = st.text_input("Enter Your Location:", placeholder="e.g., New York")
    concern = st.text_area("Any Specific Concerns?", placeholder="e.g., How to connect with recruiters?")

    if st.button("Find Networking Opportunities"):
        if profession and location:
            st.subheader("📌 **Live Networking Events**")

            # 🔹 Fetch event links
            event_query = f"{profession} networking events in {location} {datetime.today().year}"
            events = fetch_google_search_results(event_query)

            if events:
                for event in events:
                    st.markdown(summarize_event_details(event["title"], event["link"]))
            else:
                st.warning("⚠ No upcoming events found.")

            # 🔹 AI-Powered Networking Strategies
            st.subheader("💡 **AI-Powered Networking Strategies**")
            st.info(get_ai_networking_insights(profession, location, concern))

            # 🔹 Career Networking Insights (from Mistral)
            st.subheader("📌 Career Networking Insights")
            st.write(get_networking_insights(profession, location, concern))

        else:
            st.warning("⚠ Please enter both your profession and location!")

    # 🔹 Advance Your Network Section
    st.markdown("---")
    st.subheader("🚀 Advance Your Network")
    st.markdown(
        """
        - 🔗 [*LinkedIn*](https://www.linkedin.com) – Connect with professionals and recruiters.  
        - 🎟 [*Meetup*](https://www.meetup.com) – Join industry events and local meetups.  
        - 💼 [*Xing*](https://www.xing.com) – Expand your career network in Europe.  
        - 🎤 [*Eventbrite*](https://www.eventbrite.com) – Discover professional events and conferences.  
        - 🏢 [*AngelList*](https://angel.co) – Network with startups and investors.  
        """
    )

# ✅ Run UI
if __name__ == "__main__":
    networking_ui()
