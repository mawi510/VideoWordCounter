import os

from faster_whisper import WhisperModel, BatchedInferencePipeline

# Model size can be overridden without a code change (e.g. "base" on small cloud hosts)
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")

_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None:
        model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
        _pipeline = BatchedInferencePipeline(model=model)
    return _pipeline

#Transcribe the audio and return segments shaped like word_counter expects
def grab_audio_segments(input_audio_path, progress_callback=None):
    pipeline = get_pipeline()

    if progress_callback:
        progress_callback("Transcribing audio...")

    segments, info = pipeline.transcribe(
        input_audio_path,
        word_timestamps=True,
        vad_filter=True,
        batch_size=8,
    )

    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
            "words": [
                {"word": w.word, "start": w.start, "end": w.end}
                for w in (segment.words or [])
            ],
        })
    return results
