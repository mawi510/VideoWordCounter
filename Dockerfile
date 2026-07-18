# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces runs containers as a non-root user with a writable HOME
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory
WORKDIR /home/user/app

# Copy requirements and install Python dependencies
COPY --chown=user requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK stopwords so the first request isn't slow
RUN python -c "import nltk; nltk.download('stopwords')"

# Copy all application files
COPY --chown=user *.py ./
COPY --chown=user config.toml ./.streamlit/config.toml

# Hugging Face Spaces serves the app on port 7860
EXPOSE 7860

# Command to run the app
CMD ["streamlit", "run", "video_word_counter.py", "--server.port=7860", "--server.address=0.0.0.0"]
