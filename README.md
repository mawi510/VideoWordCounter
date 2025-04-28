# Video to Word Counter App
![Docker Build](https://github.com/mawi510/VideoWordCounter/actions/workflows/docker-build.yml/badge.svg)

Video to Word Counter is a simple and intuitive web app that:

- 📹 Takes a video file as input

- 🎵 Extracts audio from the video using ffmpeg

- 🔉 Transcribes the audio into words with timestamps using OpenAI's Whisper

- 📊 Displays an interactive word frequency bar chart

- 📲 Lets you jump to specific parts of the video by selecting words and timestamps

- Built using Streamlit, Whisper, FFmpeg, and Plotly.

## 🚀 Features

- Upload .mp4, .mov, or .avi video files

- Extract clean audio for transcription

- Whisper model (small) for accurate speech-to-text

- Interactive bar chart showing word frequency

- Timestamp-based video navigation

- Easy clearing and reprocessing of new videos

## 📦 Requirements

Python Packages:

`pip install -r requirements.txt`

System Requirements:

Install FFmpeg:

`macOS: brew install ffmpeg`

`Ubuntu: sudo apt install ffmpeg`

Windows: [Download FFmpeg](https://ffmpeg.org/download.html)

## 🔥 Getting Started (Docker)
1. Clone the repository

```
git clone https://github.com/mawi510/VideoWordCounter.git
cd video-word-counter
```

2. Build Docker Image

```
docker compose up --build
```

3. Open your browser

`Navigate to http://localhost:8501 to interact with the app.`

## 🔥 Getting Started (Manual)

1. Clone the repository

```
git clone https://github.com/mawi510/VideoWordCounter.git
cd video-word-counter
```

2. Install dependencies

`pip install -r requirements.txt`

3. Run the app

`streamlit run video_word_counter.py`

4. Open your browser

`Navigate to http://localhost:8501 to interact with the app.`
