from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend.transcription import transcribe_audio
from backend.summarizer import summarize_transcript_file
from pydantic import BaseModel
from backend.url_audio import get_audio_from_url
from pathlib import Path
import shutil
import uuid

app = FastAPI(title="Podcast Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "data" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUMMARIES_DIR = BASE_DIR / "data" / "summaries"
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR = BASE_DIR / "data" / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}

@app.post("/summarize/upload")
async def upload_audio(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()

    if ext not in ALLOWED_EXTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type {ext}. Allowed: {sorted(ALLOWED_EXTS)}"
        )

    # unique filename to avoid collisions
    file_id = uuid.uuid4().hex
    save_path = AUDIO_DIR / f"{file_id}{ext}"

    with save_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    transcript_path = transcribe_audio(save_path)

    transcript_preview = Path(transcript_path).read_text(encoding="utf-8")[:2000]


    summary_path = summarize_transcript_file(transcript_path, SUMMARIES_DIR)
    summary_data = summarize_transcript_file(transcript_path, SUMMARIES_DIR)


    return {
        "message": "Upload successful",
        "file_id": file_id,

        "transcript_preview": Path(transcript_path).read_text(encoding="utf-8")[:2000],

        "summary_preview": summary_data["paragraph"][:800],
        "bullet_points": summary_data["bullets"],

        "download_summary_url": f"/download/summary/{file_id}",
        "download_bullets_url": f"/download/bullets/{file_id}",
    }


@app.get("/health")
def health():
    return {"status": "ok"}

class UrlRequest(BaseModel):
    url: str
@app.post("/summarize/url")
def summarize_from_url(payload: UrlRequest):
    # 1) get audio file from URL
    audio_path = get_audio_from_url(payload.url, AUDIO_DIR)

    # 2) transcribe
    transcript_path = transcribe_audio(audio_path)

    transcript_preview = Path(transcript_path).read_text(encoding="utf-8")[:2000]

    # 3) summarize
    summary_path = summarize_transcript_file(Path(transcript_path), SUMMARIES_DIR)

    # Extract file_id from transcript filename (without .txt extension)
    file_id = Path(transcript_path).stem

    return {
        "message": "Upload successful",
        "file_id": file_id,

        "transcript_preview": Path(transcript_path).read_text(encoding="utf-8")[:2000],

        "summary_preview": summary_data["paragraph"][:800],
        "bullet_points": summary_data["bullets"],

        "download_summary_url": f"/download/summary/{file_id}",
        "download_bullets_url": f"/download/bullets/{file_id}",
    }

    
@app.get("/download/transcript/{file_id}")
def download_transcript(file_id: str):
    path = BASE_DIR / "data" / "transcripts" / f"{file_id}.txt"
    return FileResponse(path, media_type="text/plain", filename=f"{file_id}.txt")

@app.get("/download/summary/{file_id}")
def download_summary(file_id: str):
    path = BASE_DIR / "data" / "summaries" / f"{file_id}_summary.txt"
    return FileResponse(path, media_type="text/plain", filename=f"{file_id}_summary.txt")

@app.get("/download/bullets/{file_id}")
def download_bullets(file_id: str):
    path = BASE_DIR / "data" / "summaries" / f"{file_id}_bullets.txt"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Bullets not found")
    return FileResponse(path, media_type="text/plain", filename=f"{file_id}_bullets.txt")
