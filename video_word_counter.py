import os
import re
import glob
import yt_dlp

from extract_audio import extract_audio_ffmpeg
from transcribe_audio import grab_audio_segments
from word_counter import get_word_counts

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.header("Video to Word Counter")

def is_valid_url(url):
    """Check if the input is a valid URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def download_video_from_url(url, output_path="temp_downloaded_video"):
    """Download video from URL using yt-dlp"""
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # Prefer mp4, fallback to best available
        'outtmpl': f'{output_path}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # First extract info to get the extension
        info = ydl.extract_info(url, download=False)
        ext = info.get('ext', 'mp4')
        # Now download
        ydl.download([url])
        downloaded_path = f'{output_path}.{ext}'
    
    # Verify file exists
    if os.path.exists(downloaded_path):
        return downloaded_path
    else:
        # Fallback: try to find any file starting with output_path
        matches = glob.glob(f"{output_path}.*")
        if matches:
            return matches[0]
        raise FileNotFoundError(f"Downloaded video file not found: {downloaded_path}")

# Cache heavy processing steps
@st.cache_data
def process_video_file(video_file):
    video_path = f"temp_{video_file.name}"
    with open(video_path, "wb") as f:
        f.write(video_file.read())
    audio_path = extract_audio_ffmpeg(video_path)
    segments = grab_audio_segments(audio_path)
    counter, word_times = get_word_counts(segments)
    return video_path, counter, word_times

@st.cache_data
def process_video_url(url):
    video_path = download_video_from_url(url)
    audio_path = extract_audio_ffmpeg(video_path)
    segments = grab_audio_segments(audio_path)
    counter, word_times = get_word_counts(segments)
    return video_path, counter, word_times

# UI: Let user choose between file upload or URL
input_method = st.radio(
    "Choose input method:",
    ["Upload a video file", "Enter a video URL"],
    horizontal=True
)

video_processed = False
video_identifier = None

if input_method == "Upload a video file":
    uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])
    if uploaded_video:
        video_identifier = uploaded_video.name
        if "processed" not in st.session_state or st.session_state.video_name != video_identifier or st.session_state.input_method != "file":
            with st.spinner("Processing video..."):
                st.session_state.input_method = "file"
                st.session_state.video_name = video_identifier
                st.session_state.video_path, st.session_state.counter, st.session_state.word_times = process_video_file(uploaded_video)
                st.session_state.processed = True
        video_processed = True
else:
    video_url = st.text_input("Enter video URL (YouTube, Vimeo, etc.)", placeholder="https://www.youtube.com/watch?v=...")
    if video_url:
        if is_valid_url(video_url):
            video_identifier = video_url
            if "processed" not in st.session_state or st.session_state.video_name != video_identifier or st.session_state.input_method != "url":
                with st.spinner("Processing video..."):
                    st.session_state.input_method = "url"
                    st.session_state.video_name = video_identifier
                    st.session_state.video_path, st.session_state.counter, st.session_state.word_times = process_video_url(video_url)
                    st.session_state.processed = True
            video_processed = True
        else:
            st.error("Please enter a valid URL")

if st.session_state.get("processed", False) and video_processed:
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
    st.text("Upload a video file or enter a video URL to get started! 🎥")