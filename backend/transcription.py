import whisper
from pathlib import Path

# load model once (important)
model = whisper.load_model("tiny")

TRANSCRIPTS_DIR = Path(__file__).resolve().parent.parent / "data" / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

def transcribe_audio(audio_path: Path) -> Path:
    """
    Transcribes audio and saves transcript as .txt
    Returns transcript file path
    """
    result = model.transcribe(str(audio_path))

    transcript_text = result["text"]

    transcript_path = TRANSCRIPTS_DIR / f"{audio_path.stem}.txt"
    transcript_path.write_text(transcript_text, encoding="utf-8")

    return transcript_path
