import streamlit as st
from extract_audio import extract_audio_ffmpeg
from transcribe_audio import transcribe_audio
from generate_word_cloud import generate_wordcloud
from word_counter import get_word_counts

st.text("Video to Word Counter")

uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    with st.spinner('Processing...'):
        video_path = "uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

        audio_path = extract_audio_ffmpeg(video_path)
        segments = transcribe_audio(audio_path)
        counter, word_times = get_word_counts(segments)

    st.subheader("Word Frequencies")
    st.write(counter)

    st.subheader("Word Cloud")
    generate_wordcloud(counter)

    st.subheader("Words and Timestamps")
    for word, times in word_times.items():
        st.write(f"{word}: {times}")