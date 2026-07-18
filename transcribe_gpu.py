"""ZeroGPU transcription backend — used only on Hugging Face Spaces.

Uses PyTorch Whisper via transformers so the free ZeroGPU slice can be used
(faster-whisper/CTranslate2 cannot run on ZeroGPU).
"""
import os

import spaces
import torch
from transformers import pipeline

MODEL_ID = os.environ.get("WHISPER_MODEL_ID", "openai/whisper-large-v3-turbo")

pipe = pipeline(
    "automatic-speech-recognition",
    model=MODEL_ID,
    torch_dtype=torch.float16,
    device="cuda",
)

@spaces.GPU(duration=120)
def grab_audio_segments(input_audio_path, progress_callback=None):
    if progress_callback:
        progress_callback("Transcribing audio on GPU...")

    result = pipe(
        input_audio_path,
        return_timestamps="word",
        chunk_length_s=30,
        batch_size=16,
    )

    words = []
    for chunk in result.get("chunks", []):
        start, end = chunk.get("timestamp") or (None, None)
        if start is None:
            continue
        words.append({
            "word": chunk["text"],
            "start": float(start),
            "end": float(end) if end is not None else float(start),
        })

    # Single segment shaped like word_counter expects
    return [{
        "start": words[0]["start"] if words else 0.0,
        "end": words[-1]["end"] if words else 0.0,
        "text": result.get("text", ""),
        "words": words,
    }]
