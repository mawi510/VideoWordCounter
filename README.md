📹 Video to Word Counter App
 

Video to Word Counter is a simple and intuitive web app that:

📹 Takes a video file as input

🎵 Extracts audio from the video using ffmpeg

🔒 Transcribes the audio into words with timestamps using OpenAI's Whisper

📊 Displays an interactive word frequency bar chart

📲 Lets you jump to specific parts of the video by selecting words and timestamps

Built using Streamlit, Whisper, FFmpeg, and Plotly.

🚀 Features

Upload .mp4, .mov, or .avi video files

Extract clean audio for transcription

Whisper model (small) for accurate speech-to-text

Interactive bar chart showing word frequency

Timestamp-based video navigation

Easy clearing and reprocessing of new videos

📦 Requirements

Python Packages:

pip install -r requirements.txt

System Requirements:

Install FFmpeg:

macOS: brew install ffmpeg

Ubuntu: sudo apt install ffmpeg

Windows: Download FFmpeg

🛠️ Folder Structure

.
├── app.py                # Main Streamlit application
├── extract_audio.py       # Audio extraction from video
├── transcribe_audio.py    # Audio transcription with Whisper
├── word_counter.py        # Word frequency and timestamp counter
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation

🔥 Getting Started

1. Clone the repository

git clone https://github.com/your-username/video-word-counter.git
cd video-word-counter

2. Install dependencies

pip install -r requirements.txt

3. Run the app

streamlit run app.py

4. Open your browser

Navigate to http://localhost:8501 to interact with the app.

📈 Roadmap / Future Features

✨ Word cloud generation from transcript

🔢 Downloadable full transcripts (CSV, TXT)

⏱️ Chunked transcription support for long videos

💰 Choose Whisper model size (tiny, base, small, medium, large) via UI dropdown

🌐 Cloud deployment (Streamlit Cloud / Hugging Face Spaces)

📅 Versioning

We use SemVer for versioning. For the versions available, see the tags on this repository.

👽 Authors

Your Name - @yourusername

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

🌍 Acknowledgments

Streamlit

OpenAI Whisper

FFmpeg

Plotly