def get_chatbot_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7
    }

import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mistral API Key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Function to interact with Mistral API
def get_chatbot_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Error: Unable to fetch response. (Status Code: {response.status_code})"

# Chatbot UI
def chatbot_page():
    st.title("💬 AI Career Mentor")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Resume chat if selected from history
    if "selected_chat" in st.session_state and st.session_state.selected_chat:
        st.session_state.chat_history = st.session_state.selected_chat
        del st.session_state.selected_chat  # Clear after loading

    # Display chat history
    for chat in st.session_state.chat_history:
        st.chat_message(chat["role"]).write(chat["content"])

    # User input
    user_input = st.chat_input("Ask a career-related question:")
    if user_input:
        st.chat_message("user").write(user_input)

        # Get AI response
        ai_response = get_chatbot_response(user_input)
        st.chat_message("assistant").write(ai_response)

        # Store in chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
