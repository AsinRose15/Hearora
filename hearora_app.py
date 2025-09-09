# hearora_app.py
import streamlit as st
from io import BytesIO
from pathlib import Path
from PyPDF2 import PdfReader
from gtts import gTTS
import base64

# ---------------------------
# App Configuration
# ---------------------------
st.set_page_config(
    page_title="Hearora - For Lazy Readers",
    page_icon="🎧",
    layout="wide"
)

# ---------------------------
# Background Themes
# ---------------------------
theme_images = {
    "City Lights": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
    "Forest": "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
    "Coffee Shop": "https://images.unsplash.com/photo-1525396314762-2b53c07b7a50",
    "Night Sky": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
    "Raining": "https://images.unsplash.com/photo-1500674425229-f692875b0ab7",
    "Yellow Sky": "https://images.unsplash.com/photo-1495567720989-cebdbdd97913",
    "Solar System": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa"
}

selected_theme = st.sidebar.selectbox("Select Background Theme", list(theme_images.keys()))

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{theme_images[selected_theme]}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        filter: brightness(0.85);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.title("Hearora Settings")
voice_gender = st.sidebar.radio("Select Voice Gender", ["Male", "Female"])
tone = st.sidebar.selectbox("Select Tone", ["Neutral", "Suspenseful", "Inspiring"])
emotion = st.sidebar.selectbox("Select Emotion", ["Neutral", "Happy", "Sad", "Romantic", "Angry", "Anxiety"])

# ---------------------------
# Text Input / PDF Import
# ---------------------------
st.title("Hearora 🎧")
st.subheader("For Lazy Readers")

user_text = ""
uploaded_file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            user_text += page.extract_text()
    else:
        user_text = str(uploaded_file.read(), "utf-8")

if not user_text:
    user_text = st.text_area("Enter or paste your text here:")

# ---------------------------
# Text-to-Speech
# ---------------------------
def generate_audio(text, voice_gender):
    tts = gTTS(text=text, lang='en', tld='co.uk' if voice_gender=="Male" else 'com')
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

if st.button("Convert to Audio"):
    if user_text.strip() == "":
        st.warning("Please enter text or upload a file first.")
    else:
        with st.spinner("Generating Audio..."):
            audio_file = generate_audio(user_text, voice_gender)
            st.audio(audio_file, format="audio/mp3")
            
            # Provide download
            b64 = base64.b64encode(audio_file.read()).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="hearora_audio.mp3">Download Audio</a>'
            st.markdown(href, unsafe_allow_html=True)

# ---------------------------
# Tone + Emotion Info
# ---------------------------
st.markdown(f"**Tone:** {tone} | **Emotion:** {emotion}")
