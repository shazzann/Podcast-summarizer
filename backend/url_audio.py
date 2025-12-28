from pathlib import Path
from urllib.parse import urlparse
import re
import uuid
import httpx
import feedparser
import subprocess

AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".webm"}

def _looks_like_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def _guess_ext_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in AUDIO_EXTS:
        if path.endswith(ext):
            return ext
    return ".mp3"  # fallback

def download_direct_audio(url: str, audio_dir: Path) -> Path:
    audio_dir.mkdir(parents=True, exist_ok=True)
    ext = _guess_ext_from_url(url)
    out_path = audio_dir / f"{uuid.uuid4().hex}{ext}"

    with httpx.stream("GET", url, follow_redirects=True, timeout=60) as r:
        r.raise_for_status()
        with out_path.open("wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)

    return out_path

def download_from_rss(url: str, audio_dir: Path) -> Path:
    """
    Accepts:
      - RSS feed URL, OR
      - an episode page that is itself an RSS item link (sometimes works)
    Tries to find first enclosure audio URL and download it.
    """
    feed = feedparser.parse(url)
    if not feed.entries:
        raise ValueError("No entries found in RSS feed.")

    # pick first entry; later you can allow user to choose episode
    entry = feed.entries[0]

    # find enclosure audio
    enclosure_url = None
    if "enclosures" in entry and entry.enclosures:
        # choose first enclosure
        enclosure_url = entry.enclosures[0].get("href")

    # sometimes media_content exists
    if not enclosure_url and "media_content" in entry and entry.media_content:
        enclosure_url = entry.media_content[0].get("url")

    if not enclosure_url:
        raise ValueError("No audio enclosure found in RSS entry.")

    return download_direct_audio(enclosure_url, audio_dir)

def download_youtube_audio(url: str, audio_dir: Path) -> Path:
    """
    Uses yt-dlp to download best audio and extract to mp3.
    Requires ffmpeg installed.
    """
    audio_dir.mkdir(parents=True, exist_ok=True)
    out_template = str(audio_dir / f"{uuid.uuid4().hex}.%(ext)s")

    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", out_template,
        url
    ]
    subprocess.run(cmd, check=True)

    # find the produced file (mp3)
    # yt-dlp will output something like <uuid>.mp3
    produced = sorted(audio_dir.glob("*.mp3"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not produced:
        raise FileNotFoundError("yt-dlp did not produce an mp3 file.")
    return produced[0]

def get_audio_from_url(url: str, audio_dir: Path) -> Path:
    """
    Strategy:
    1) If direct audio link -> download
    2) If YouTube -> yt-dlp
    3) Else try RSS parse -> enclosure download
    """
    u = url.strip()

    # direct audio?
    if any(urlparse(u).path.lower().endswith(ext) for ext in AUDIO_EXTS):
        return download_direct_audio(u, audio_dir)

    # youtube?
    if _looks_like_youtube(u):
        return download_youtube_audio(u, audio_dir)

    # fallback: try RSS
    return download_from_rss(u, audio_dir)
