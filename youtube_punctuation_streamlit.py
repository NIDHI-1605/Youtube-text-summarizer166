import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from deepmultilingualpunctuation import PunctuationModel
import re

st.set_page_config(page_title="YouTube Punctuation Restorer", layout="wide")
st.title("🎬 YouTube Transcript Punctuation Enhancer")
st.write("Enter a YouTube video URL to retrieve and clean up the transcript with punctuation.")

url = st.text_input("🔗 Paste YouTube URL here:", placeholder="e.g. https://www.youtube.com/watch?v=abc123")

def extract_video_id(url_link):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_link)
    return match.group(1) if match else None

if url:
    video_id = extract_video_id(url)
    if video_id:
        try:
            st.info("📄 Fetching transcript...")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([t["text"] for t in transcript])

            st.success("✅ Transcript fetched!")

            st.info("🔤 Restoring punctuation...")
            punct_model = PunctuationModel()
            punctuated_text = punct_model.restore_punctuation(full_text)

            st.success("✅ Punctuation added!")

            st.subheader("📜 Transcript with Punctuation")
            st.write(punctuated_text)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Invalid YouTube URL.")
