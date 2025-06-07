import os

from extract_audio import extract_audio_ffmpeg
from transcribe_audio import grab_audio_segments
from word_counter import get_word_counts

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.header("Video to Word Counter")

# Cache heavy processing steps
@st.cache_data
def process_video(video_file):
    video_path = f"temp_{video_file.name}"
    with open(video_path, "wb") as f:
        f.write(video_file.read())
    audio_path = extract_audio_ffmpeg(video_path)
    segments = grab_audio_segments(audio_path)
    counter, word_times = get_word_counts(segments)
    return video_path, counter, word_times


uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])

if uploaded_video:
    if "processed" not in st.session_state or st.session_state.video_name != uploaded_video.name:
        st.session_state.video_name = uploaded_video.name
        st.session_state.video_path, st.session_state.counter, st.session_state.word_times = process_video(uploaded_video)
        st.session_state.processed = True

if st.session_state.get("processed", False):
    counter = st.session_state.counter
    word_times = st.session_state.word_times
    video_path = st.session_state.video_path
    # segments = st.session_state.segments
    # st.text(segments)

    st.subheader("Word Frequencies")
    df = pd.DataFrame.from_dict(dict(counter), 
                                orient='index').reset_index()
    df.columns=['word', 'frequency']
    df = df.sort_values(by='frequency', ascending=False)

    fig = px.bar(df, 
                x='word', 
                y='frequency')

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    word_list = sorted([i for i in df['word'].unique()])
    
    st.subheader("View Timestamps")
    word = st.selectbox('Word', word_list, placeholder='Select Word')

    timestamps = word_times.get(word, [])

    if timestamps:
        selected_time = st.selectbox("Jump to timestamp (sec):", timestamps)
        st.video(video_path, start_time=selected_time)
    else:
        st.warning("No timestamps found for the selected word.")
    
else:
    st.text("Upload your video to get started! 🎥")