from pathlib import Path
from transformers import pipeline

# A solid summarization model for general text
_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text: str, max_chars: int = 3000):
    """Simple chunking by character length to avoid model limits."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end
    return chunks

def summarize_text(text: str) -> str:
    chunks = chunk_text(text)

    partial_summaries = []
    for c in chunks:
        out = _summarizer(
            c,
            max_length=180,
            min_length=60,
            do_sample=False
        )
        partial_summaries.append(out[0]["summary_text"])

    # If there were many chunks, summarize the summaries again
    combined = "\n".join(partial_summaries)
    if len(partial_summaries) > 3:
        out = _summarizer(
            combined[:4000],
            max_length=220,
            min_length=80,
            do_sample=False
        )
        return out[0]["summary_text"]

    return combined

def summarize_transcript_file(transcript_path: Path, summaries_dir: Path) -> dict:
    text = transcript_path.read_text(encoding="utf-8").strip()

    paragraph_summary = summarize_text(text)
    bullet_summary = summarize_text_bullets(text)

    summaries_dir.mkdir(parents=True, exist_ok=True)

    base = transcript_path.stem

    para_path = summaries_dir / f"{base}_summary.txt"
    para_path.write_text(paragraph_summary, encoding="utf-8")

    bullets_path = summaries_dir / f"{base}_bullets.txt"
    bullets_path.write_text(
        "\n".join(f"- {b}" for b in bullet_summary),
        encoding="utf-8"
    )

    return {
        "paragraph": paragraph_summary,
        "bullets": bullet_summary,
        "paragraph_path": para_path,
        "bullets_path": bullets_path
    }

def summarize_text_bullets(text: str) -> list[str]:
    """
    Returns a list of bullet points summarizing the text
    """
    chunks = chunk_text(text)

    bullet_points = []

    for c in chunks:
        out = _summarizer(
            "Summarize the following text into concise bullet points:\n\n" + c,
            max_length=180,
            min_length=60,
            do_sample=False
        )

        # Split model output into bullet-like lines
        raw = out[0]["summary_text"]
        lines = [l.strip("-• ").strip() for l in raw.split("\n") if l.strip()]
        bullet_points.extend(lines)

    # Deduplicate + keep top bullets
    seen = set()
    final_bullets = []
    for b in bullet_points:
        if b not in seen:
            seen.add(b)
            final_bullets.append(b)
        if len(final_bullets) >= 8:
            break

    return final_bullets
