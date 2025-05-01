import pandas as pd
import streamlit as st
import plotly.express as px

from extract_audio import extract_audio_ffmpeg
from transcribe_audio import transcribe_audio
from word_counter import get_word_counts

st.header("Video to Word Counter")

uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])

if uploaded_video is None:
    st.text("Upload your video to get started! 🎥")
else:
    with st.spinner('Processing...'):
        video_path = uploaded_video.name
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

    audio_path = extract_audio_ffmpeg(video_path)

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


    #This allows the user to see where a word was said
    #However we want to eliminate stop words as they're not super informative/interesting

    import nltk
    from nltk.corpus import stopwords

    #Have to download stopwords first
    nltk.download('stopwords')
    word_list = [i for i in df['word'].unique() if i not in stopwords.words('english')]
    
    st.subheader("View Timestamps")
    word = st.selectbox('Word', word_list, placeholder='Select Word')

    timestamps = word_times[word]
    timestamp = st.selectbox('Timestamp', timestamps, placeholder='Select Timestamp')

    @st.cache_data
    def load_video(start_time):
        st.video(video_path, start_time=start_time, muted=True)

    load_video(timestamp)