---
title: Video Word Counter
emoji: 🎥
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
---

# Video to Word Counter App
![Docker Build](https://github.com/mawi510/VideoWordCounter/actions/workflows/docker-build.yml/badge.svg)

Video to Word Counter is a simple and intuitive web app that:

- 🔗 Takes a video URL (YouTube, Vimeo, etc.) or an uploaded video file as input

- 🎵 Downloads only the audio stream for URLs (tens of MB instead of the full video), or extracts audio with ffmpeg for uploads

- 🔉 Transcribes the audio into words with timestamps using faster-whisper

- 📊 Displays an interactive word frequency bar chart

- 📲 Lets you jump to specific parts of the video by selecting words and timestamps

- Built using Streamlit, faster-whisper, FFmpeg, yt-dlp, and Plotly.

## 🚀 Features

- Paste a video link — the full video is never downloaded, only its audio

- Or upload .mp4, .mov, or .avi video files

- faster-whisper model (small, int8) for fast, accurate speech-to-text — override with the `WHISPER_MODEL` env var (e.g. `base` for smaller hosts)

- Interactive bar chart showing word frequency

- Timestamp-based video navigation (URL videos play from the original site, uploads from the local file)

## ☁️ Hosted App (Hugging Face Spaces)

The app runs at https://huggingface.co/spaces/mawi510/VideoWordCounter as a free Gradio Space on ZeroGPU hardware — the YAML block at the top of this README is the Space config, `app.py` is the entry point, and transcription runs on the free GPU slice via `transcribe_gpu.py` (locally the app uses faster-whisper on CPU instead). To redeploy after changes, push a history-free snapshot (the repo's git history contains an old >10MB video that Hugging Face rejects):

```
git remote add hf https://huggingface.co/spaces/mawi510/VideoWordCounter   # once
SNAP=$(git commit-tree HEAD^{tree} -m "Deploy snapshot") && git push hf "${SNAP}:refs/heads/main" --force
```

`origin` remains GitHub.

**Known limitation:** YouTube often blocks downloads from cloud/datacenter IPs ("Sign in to confirm you're not a bot"). YouTube links may fail on the hosted Space but work when running locally; most other sites work fine either way.

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
