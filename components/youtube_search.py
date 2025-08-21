
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def youtube_search_ui():
    st.title("🎥 YouTube Career Video Explorer")
    query = st.text_input("🔎 Search YouTube for career help:", placeholder="e.g., career in data science")

    if query:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=5&key={YOUTUBE_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            videos = response.json().get("items", [])
            if videos:
                # Display first video large
                selected_video_id = st.session_state.get("selected_video_id", videos[0]["id"]["videoId"])
                st.video(f"https://www.youtube.com/watch?v={selected_video_id}")

                # Thumbnails horizontally
                cols = st.columns(len(videos))
                for i, video in enumerate(videos):
                    vid_id = video["id"]["videoId"]
                    title = video["snippet"]["title"]
                    thumb_url = video["snippet"]["thumbnails"]["medium"]["url"]
                    with cols[i]:
                        st.image(thumb_url, use_column_width=True)
                        st.caption(title)
                        if st.button(f"▶️ Play {i+1}", key=f"play_{i}"):
                            st.session_state["selected_video_id"] = vid_id
                            st.rerun()
            else:
                st.warning("No videos found.")
        else:
            st.error("Failed to fetch videos from YouTube.")
