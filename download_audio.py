import glob
import re
import uuid

import yt_dlp

def is_valid_url(url):
    """Check if the input is a valid URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def download_audio_from_url(url, output_path=None):
    """Download only the audio stream using yt-dlp; the video itself is never fetched.

    Returns (audio_path, playback) where playback describes how to embed the video
    for timestamp playback:
      {"kind": "youtube", "video_id": ..., "url": <watch page URL>}
      {"kind": "direct", "url": <direct video stream or original URL>}
    """
    if output_path is None:
        # Unique name so concurrent users on a shared host don't collide
        output_path = f"temp_audio_{uuid.uuid4().hex}"
    ydl_opts = {
        'format': 'bestaudio/best',  # Audio stream only — tens of MB instead of the full video
        'outtmpl': f'{output_path}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    matches = glob.glob(f"{output_path}.*")
    if not matches:
        raise FileNotFoundError(f"Downloaded audio file not found: {output_path}.*")
    audio_path = matches[0]

    # YouTube videos are embedded client-side by video id; for other sites find a
    # direct video stream URL among the formats yt-dlp already extracted (no extra request)
    if info.get('extractor_key', '').lower().startswith('youtube'):
        playback = {
            "kind": "youtube",
            "video_id": info.get('id'),
            "url": info.get('webpage_url', url),
        }
    else:
        playback_url = url
        video_formats = [
            f for f in info.get('formats', [])
            if f.get('vcodec') not in (None, 'none') and f.get('url', '').startswith('http')
        ]
        if video_formats:
            playback_url = video_formats[-1]['url']  # formats are sorted worst-to-best
        playback = {"kind": "direct", "url": playback_url}

    return audio_path, playback
