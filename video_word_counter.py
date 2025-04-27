import os
from io import StringIO

import pandas as pd
import streamlit as st
import plotly.express as px
import whisper

from extract_audio import extract_audio_ffmpeg
from transcribe_audio import transcribe_audio
from word_counter import get_word_counts

st.header("Video to Word Counter")

uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])

st.text("Click below to clear cache and transcribe a new video")

if st.button("Clear", type='primary'):
    st.cache_data.clear()
else:
    pass

if uploaded_video is not None:
    with st.spinner('Processing...'):
        video_path = uploaded_video.name
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

    audio_path = extract_audio_ffmpeg(video_path)

#Get audio segments

@st.cache_data
def transcribe_audio(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, word_timestamps=True)
    return result['segments']

segments = transcribe_audio(audio_path)
counter, word_times = get_word_counts(segments)


st.subheader("Word Frequencies")
df = pd.DataFrame.from_dict(dict(counter), 
                            orient='index').reset_index()
df.columns=['word', 'frequency']
df = df.sort_values(by='frequency', ascending=False)

fig = px.bar(df, 
             x='word', 
             y='frequency')

st.plotly_chart(fig, theme='streamlit', use_container_width=True)


st.subheader("View Timestamps")
word = st.selectbox('Word', df['word'].unique(), placeholder='Select Word')

timestamps = word_times[word]
timestamp = st.selectbox('Timestamp', timestamps, placeholder='Select Timestamp')

@st.cache_data
def load_video(start_time):
    st.video("uploaded_video.mp4", start_time=start_time, muted=True)

load_video(timestamp)