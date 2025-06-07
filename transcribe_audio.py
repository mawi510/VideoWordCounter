import subprocess
import os
from multiprocessing import Pool, cpu_count

import whisper

# Global model for multiprocessing
model = None

def init_model():
    global model
    model = whisper.load_model("small")

#Split the audio into 30 second increments

def split_audio(input_audio_path, chunk_duration_sec=60, output_dir="audio_chunks"):
    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, "chunk_%03d.wav")

    command = [
        "ffmpeg",
        "-i", input_audio_path,
        "-f", "segment",
        "-segment_time", str(chunk_duration_sec),
        "-c", "copy",
        output_template,
        "-y"
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sorted([
        os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".wav")
        ])

#Transcribe the audio

def transcribe_audio(args):
    global model
    index, filepath, chunk_duration = args
    offset = index * chunk_duration

    result = model.transcribe(filepath, word_timestamps=True, fp16=False)

    for segment in result["segments"]:
        segment["start"] += offset
        segment["end"] += offset
        # if "words" in segment:
        #     for word in segment["words"]:
        #         word["start"] += offset
        #         word["end"] += offset

    return result["segments"]

def grab_audio_segments(input_audio_path):

    audio_chunks = split_audio(input_audio_path)

    args = [(i, path, 60) for i, path in enumerate(audio_chunks)]

    with Pool(processes=6, initializer=init_model) as pool:
        all_segments = pool.map(transcribe_audio, args)

    # Flatten and print result
    return [seg for chunk in all_segments for seg in chunk]


    # def transcribe_audio(audio_path):
    #     model = whisper.load_model("small")
    #     result = model.transcribe(audio_path, word_timestamps=True)
    #     return result['segments']