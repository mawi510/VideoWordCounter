import whisper
import streamlit as st

@st.cache_data
def transcribe_audio(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, word_timestamps=True)
    return result['segments']