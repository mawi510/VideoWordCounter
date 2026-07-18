import os
import uuid

import gradio as gr
import pandas as pd
import plotly.express as px
import yt_dlp

from download_audio import is_valid_url, download_audio_from_url
from extract_audio import extract_audio_ffmpeg
from word_counter import get_word_counts

# On Hugging Face Spaces transcribe with PyTorch Whisper on the free ZeroGPU
# slice; locally fall back to faster-whisper on CPU
if os.environ.get("SPACE_ID"):
    from transcribe_gpu import grab_audio_segments
else:
    from transcribe_audio import grab_audio_segments


def build_outputs(counter, word_times, playback):
    if not counter:
        raise gr.Error("No speech was detected in this video's audio.")
    df = pd.DataFrame.from_dict(dict(counter), orient='index').reset_index()
    df.columns = ['word', 'frequency']
    df = df.sort_values(by='frequency', ascending=False)
    fig = px.bar(df, x='word', y='frequency')

    word_list = sorted(df['word'].unique())
    state = {"word_times": word_times, "playback": playback}

    is_file = playback["kind"] == "file"
    return (
        fig,
        gr.Dropdown(choices=word_list, value=None),
        gr.Dropdown(choices=[], value=None),
        state,
        "",  # reset HTML player
        gr.Video(value=playback["url"] if is_file else None, visible=is_file),
    )


def process_url(url):
    url = (url or "").strip()
    if not url or not is_valid_url(url):
        raise gr.Error("Please enter a valid video URL")

    try:
        audio_path, playback = download_audio_from_url(url)
    except yt_dlp.utils.DownloadError as e:
        if "not a bot" in str(e):
            raise gr.Error(
                "This site blocked the download from the cloud server "
                "(YouTube often does this to hosted apps). Try a different site, "
                "or run the app locally where YouTube links work."
            )
        raise gr.Error(f"Could not download audio from that URL: {e}")
    # Normalize to 16kHz mono WAV: transformers' pipeline pipes audio bytes into
    # ffmpeg stdin, which fails on seek-dependent containers like mp4/m4a
    wav_path = f"temp_audio_{uuid.uuid4().hex}.wav"
    try:
        extract_audio_ffmpeg(audio_path, wav_path)
        segments = grab_audio_segments(wav_path)
    finally:
        for path in (audio_path, wav_path):
            if os.path.exists(path):
                os.remove(path)
    counter, word_times = get_word_counts(segments)
    return build_outputs(counter, word_times, playback)


def process_upload(video_path):
    if not video_path:
        raise gr.Error("Please upload a video first")

    audio_path = extract_audio_ffmpeg(video_path, f"temp_audio_{uuid.uuid4().hex}.wav")
    try:
        segments = grab_audio_segments(audio_path)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    counter, word_times = get_word_counts(segments)
    return build_outputs(counter, word_times, {"kind": "file", "url": video_path})


def list_timestamps(word, state):
    if not word or not state:
        return gr.Dropdown(choices=[], value=None)
    times = state["word_times"].get(word, [])
    choices = [(f"{int(t // 60)}:{t % 60:04.1f}", float(t)) for t in times]
    return gr.Dropdown(choices=choices, value=choices[0][1] if choices else None)


def update_player(timestamp, state):
    if timestamp is None or not state:
        return ""
    playback = state["playback"]
    start = max(0, int(float(timestamp)))
    if playback["kind"] == "youtube":
        return (
            f'<iframe width="100%" height="480" '
            f'src="https://www.youtube.com/embed/{playback["video_id"]}?start={start}&autoplay=1" '
            f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
        )
    elif playback["kind"] == "direct":
        return (
            f'<video width="100%" height="480" controls autoplay '
            f'src="{playback["url"]}#t={start}"></video>'
        )
    return ""  # file uploads seek the gr.Video player via JS instead


SEEK_JS = """
(t) => {
    const v = document.querySelector('#player video');
    if (v && t !== null && t !== undefined) {
        v.currentTime = parseFloat(t);
        v.play();
    }
}
"""

with gr.Blocks(title="Video to Word Counter") as demo:
    gr.Markdown("# Video to Word Counter 🎥")
    gr.Markdown(
        "Paste a video link (only the audio is fetched — never the full video) "
        "or upload a file. Then pick a word to jump to every place it was said."
    )
    state = gr.State()

    with gr.Tab("Video link"):
        url_in = gr.Textbox(
            label="Video URL (YouTube, Vimeo, etc.)",
            placeholder="https://www.youtube.com/watch?v=...",
        )
        url_btn = gr.Button("Process link", variant="primary")
    with gr.Tab("Upload file"):
        file_in = gr.Video(label="Upload your video")
        file_btn = gr.Button("Process upload", variant="primary")

    plot = gr.Plot(label="Word Frequencies")
    with gr.Row():
        word_dd = gr.Dropdown(label="Word", choices=[], interactive=True)
        ts_dd = gr.Dropdown(label="Jump to timestamp", choices=[], interactive=True)
    player_html = gr.HTML()
    player_video = gr.Video(label="Player", visible=False, elem_id="player", interactive=False)

    outputs = [plot, word_dd, ts_dd, state, player_html, player_video]
    url_btn.click(process_url, inputs=[url_in], outputs=outputs)
    file_btn.click(process_upload, inputs=[file_in], outputs=outputs)

    word_dd.change(list_timestamps, inputs=[word_dd, state], outputs=[ts_dd])
    ts_dd.change(update_player, inputs=[ts_dd, state], outputs=[player_html])
    ts_dd.change(None, inputs=[ts_dd], outputs=None, js=SEEK_JS)

if __name__ == "__main__":
    demo.launch()
