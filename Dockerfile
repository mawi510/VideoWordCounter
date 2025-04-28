# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "video_word_counter.py", "--server.port=8501", "--server.address=0.0.0.0"]
