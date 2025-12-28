# Podcast Summarizer


This project is a full-stack application that automatically transcribes and summarizes podcasts or any audio content. It uses OpenAI's Whisper for highly accurate audio-to-text transcription and a Hugging Face BART model (`facebook/bart-large-cnn`) for generating concise paragraph and bullet-point summaries.

The application features a Python FastAPI backend that handles the heavy lifting and a simple vanilla HTML/CSS/JavaScript frontend for user interaction.

## Features

- **Multiple Input Sources**: Summarize audio by uploading a file or providing a URL.
- **Versatile URL Support**: Handles direct audio links (`.mp3`, `.m4a`, etc.), YouTube video URLs, and podcast RSS feeds.
- **Dual Summaries**: Generates both a coherent paragraph summary and a concise list of bullet points.
- **Full Transcription**: Provides a full, downloadable transcript of the audio, powered by Whisper.
- **Simple Web Interface**: Easy-to-use UI to upload files, paste URLs, and view results.
- **Decoupled Architecture**: A clean separation between the FastAPI backend and vanilla JS frontend.

## Tech Stack

- **Backend**:
    - **Framework**: FastAPI
    - **Transcription**: `openai-whisper` (tiny model)
    - **Summarization**: `transformers` (Hugging Face) with `facebook/bart-large-cnn`
    - **URL Handling**: `httpx`, `feedparser`, `yt-dlp`
    - **Dependencies**: PyTorch

- **Frontend**:
    - HTML5
    - CSS3
    - Vanilla JavaScript

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

You need to have the following installed on your system:

- **Python 3.8+**
- **FFmpeg**: Required for audio processing by both `whisper` and `yt-dlp`.
  - On macOS: `brew install ffmpeg`
  - On Debian/Ubuntu: `sudo apt-get install ffmpeg`
- **yt-dlp**: Required for downloading audio from YouTube.
  - On macOS: `brew install yt-dlp`
  - On Debian/Ubuntu: `sudo apt-get install yt-dlp`

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/shazzann/Podcast-summarizer.git
    cd Podcast-summarizer
    ```

2.  **Set up the backend:**
    It's recommended to use a virtual environment.
    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Python dependencies:**
    ```sh
    pip install fastapi "uvicorn[standard]" python-multipart openai-whisper transformers torch httpx feedparser
    ```
    *Note: `torch` is a large library required by `whisper` and `transformers`.*

### Running the Application

1.  **Start the backend server:**
    From the root directory (`Podcast-summarizer/`), run:
    ```sh
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```
    The API will be available at `http://127.0.0.1:8000`.

2.  **Launch the frontend:**
    Open the `frontend/index.html` file in your web browser. You can do this by double-clicking the file or using a live server extension in your code editor.

3.  **Use the Summarizer:**
    - The frontend should already be configured to point to `http://127.0.0.1:8000`.
    - Choose your input mode: "Upload Audio" or "Use URL".
    - Select an audio file or paste a URL.
    - Click the "Summarize" button and wait for the process to complete.
    - The summary, transcript preview, and download links will appear on the page.

## API Endpoints

The FastAPI backend exposes the following endpoints:

#### `POST /summarize/upload`

Uploads an audio file for transcription and summarization.

-   **Body**: `multipart/form-data` with a `file` field containing the audio file.
-   **Supported Formats**: `.mp3`, `.wav`, `.m4a`, `.aac`, `.ogg`, `.flac`.
-   **Success Response (200)**:
    ```json
    {
        "message": "Upload successful",
        "file_id": "c1c1964a1b444f3191341d7ba0465cc7",
        "transcript_preview": "hobbies and health created by Kathobin. Engaging in hobbies provides numerous...",
        "summary_preview": "Engaging in hobbies provides numerous psychological and physical benefits, acting as...",
        "download_summary_url": "/download/summary/c1c1964a1b444f3191341d7ba0465cc7"
    }
    ```

#### `POST /summarize/url`

Downloads audio from a URL, then transcribes and summarizes it.

-   **Body**: JSON payload.
    ```json
    {
        "url": "https://example.com/podcast.mp3"
    }
    ```
-   **Success Response (200)**: Same structure as the `/summarize/upload` response.

#### `GET /download/transcript/{file_id}`

Downloads the full text transcript for a given `file_id`.

-   **Example**: `GET /download/transcript/c1c1964a1b444f3191341d7ba0465cc7`
-   **Response**: A `text/plain` file containing the full transcript.

#### `GET /download/summary/{file_id}`

Downloads the paragraph summary for a given `file_id`.

-   **Example**: `GET /download/summary/c1c1964a1b444f3191341d7ba0465cc7`
-   **Response**: A `text/plain` file containing the paragraph summary.

#### `GET /health`

A simple health check endpoint.

-   **Response**:
    ```json
    {
        "status": "ok"
    }
