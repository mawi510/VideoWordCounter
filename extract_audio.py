import subprocess
import os

def extract_audio_ffmpeg(video_path, output_audio_path="audio.wav"):
    # Ensure output path ends with .wav
    if not output_audio_path.endswith(".wav"):
        output_audio_path += ".wav"

    # Use ffmpeg to extract audio
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # no video
        "-acodec", "pcm_s16le",  # audio codec
        "-ar", "16000",  # sampling rate
        "-ac", "1",  # mono channel
        output_audio_path,
        "-y"  # overwrite if file exists
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_audio_path
