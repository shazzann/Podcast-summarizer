🎙️ Podcast Summarizer

A full-stack application that transcribes and summarizes podcast episodes from either audio files or URLs, producing concise summaries, bullet points, and timestamped highlights.

Built as an end-to-end AI/NLP project using FastAPI, Whisper, Hugging Face Transformers, and a vanilla JS UI.

✨ Features

📁 Audio File Upload (mp3, wav, m4a, aac, ogg, flac)

🔗 URL Support

Direct audio URLs

RSS podcast feeds

YouTube links

📝 Automatic Transcription using OpenAI Whisper

📄 Multiple Summary Formats

Paragraph summary

Bullet-point summary

Timestamped bullet highlights

⏱️ Timestamped Insights

Key points mapped to moments in the episode

💾 Downloadable Outputs

Transcript (.txt)

Summary (.txt)

Bullet points (.txt)

Timestamped bullets (.json)

🖥️ Simple Web UI

Upload file or paste URL

View summaries instantly

🔁 Reusable Processing Pipeline

Same flow for file and URL inputs

🧠 How It Works (Architecture)
Input (File or URL)
        ↓
 Audio Extraction / Upload
        ↓
   Speech-to-Text (Whisper)
        ↓
 Transcript + Segments
        ↓
  Text Chunking
        ↓
 Summarization (BART)
        ↓
 Timestamp Matching
        ↓
   UI + Downloads

Key Design Principle

All inputs are normalized into a local audio file, then passed through a single reusable processing pipeline.

🛠️ Tech Stack
Backend

Python

FastAPI – API server

Whisper – Speech-to-text

Hugging Face Transformers – Text summarization

ffmpeg – Audio decoding

yt-dlp – YouTube audio extraction

Frontend

HTML / CSS / Vanilla JavaScript

Fetch API for backend communication

Models

Whisper tiny (fast, CPU-friendly)

facebook/bart-large-cnn for summarization

📂 Project Structure
podcast-summarizer/
├── backend/
│   ├── main.py
│   ├── transcription.py
│   ├── summarizer.py
│   └── url_audio.py
├── data/
│   ├── audio/
│   ├── transcripts/
│   ├── summaries/
│   └── segments/
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
└── README.md

🚀 Getting Started
1️⃣ Clone the repo
git clone https://github.com/your-username/podcast-summarizer.git
cd podcast-summarizer

2️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

3️⃣ Install dependencies
pip install fastapi uvicorn python-multipart whisper transformers torch sentencepiece httpx feedparser yt-dlp

4️⃣ Install ffmpeg

Make sure ffmpeg is installed and available in PATH:

ffmpeg -version

▶️ Run the Application
Backend
uvicorn backend.main:app --reload


Backend runs at:

http://127.0.0.1:8000

Frontend
cd frontend
python -m http.server 5500


Open in browser:

http://127.0.0.1:5500

📡 API Endpoints
Upload Audio
POST /summarize/upload

Summarize from URL
POST /summarize/url

Download Outputs
GET /download/transcript/{id}
GET /download/summary/{id}
GET /download/bullets/{id}
GET /download/ts-bullets/{id}

⚠️ Limitations

Spotify links are usually unsupported (DRM-protected)

Long episodes can take time on CPU

No background job queue yet (planned)

Simple timestamp matching (word overlap heuristic)

🔮 Future Improvements

Background processing + progress tracking

RSS episode selection UI

Semantic search / Q&A over transcript

Speaker diarization

Database storage

Dockerized deployment

🎯 Why This Project Matters

This project demonstrates:

End-to-end ML application development

Practical NLP techniques (chunking, hierarchical summarization)

Clean backend architecture

Real-world handling of long-running AI tasks

Thoughtful UX for AI systems

👤 Author

Your Name
AI / Backend Developer
📧 your.email@example.com

🔗 GitHub: https://github.com/your-username
