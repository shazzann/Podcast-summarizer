const uploadBox = document.getElementById("uploadBox");
const urlBox = document.getElementById("urlBox");
const runBtn = document.getElementById("runBtn");

const audioFile = document.getElementById("audioFile");
const audioUrl = document.getElementById("audioUrl");
const backendUrl = document.getElementById("backendUrl");

const statusEl = document.getElementById("status");
const errorEl = document.getElementById("error");
const summaryEl = document.getElementById("summary");
const detailsEl = document.getElementById("details");


const transcriptEl = document.getElementById("transcript");
const dlTranscriptBtn = document.getElementById("dlTranscript");
const dlSummaryBtn = document.getElementById("dlSummary");
const bulletsEl = document.getElementById("bullets");


let lastResult = null;

function setMode(mode) {
  if (mode === "upload") {
    uploadBox.classList.remove("hidden");
    urlBox.classList.add("hidden");
  } else {
    urlBox.classList.remove("hidden");
    uploadBox.classList.add("hidden");
  }

  statusEl.textContent = "";
  errorEl.textContent = "";
  summaryEl.textContent = "";
  detailsEl.textContent = "";
  transcriptEl.textContent = "";
  lastResult = null;
}

document.querySelectorAll('input[name="mode"]').forEach(r => {
  r.addEventListener("change", (e) => setMode(e.target.value));
});

function setLoading(isLoading, msg = "") {
  runBtn.disabled = isLoading;
  statusEl.textContent = msg;
}

function showError(msg) {
  errorEl.textContent = msg;
}

function showResult(data) {
  lastResult = data;

  summaryEl.textContent = data.summary_preview || "";

  bulletsEl.innerHTML = "";
  (data.bullet_points || []).forEach(b => {
    const li = document.createElement("li");
    li.textContent = b;
    bulletsEl.appendChild(li);
  });

  detailsEl.textContent = JSON.stringify(data, null, 2);
}


async function runUpload(base) {
  if (!audioFile.files.length) throw new Error("Please choose an audio file.");

  const form = new FormData();
  form.append("file", audioFile.files[0]);

  const res = await fetch(`${base}/summarize/upload`, {
    method: "POST",
    body: form
  });

  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Upload failed (${res.status}): ${t}`);
  }

  return res.json();
}

async function runUrl(base) {
  const url = audioUrl.value.trim();
  if (!url) throw new Error("Please paste a URL.");

  const res = await fetch(`${base}/summarize/url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  if (!res.ok) {
    const t = await res.text();
    throw new Error(`URL request failed (${res.status}): ${t}`);
  }

  return res.json();
}

runBtn.addEventListener("click", async () => {
  errorEl.textContent = "";
  summaryEl.textContent = "";
  detailsEl.textContent = "";
  transcriptEl.textContent = "";
  lastResult = null;

  const base = backendUrl.value.trim().replace(/\/$/, "");
  const mode = document.querySelector('input[name="mode"]:checked').value;

  try {
    setLoading(true, "Working... (upload/download → transcribe → summarize)");
    const data = mode === "upload" ? await runUpload(base) : await runUrl(base);
    setLoading(false, "Done ✅");
    showResult(data);
  } catch (err) {
    setLoading(false, "");
    showError(err.message || String(err));
  }
});

// Download buttons
dlTranscriptBtn.addEventListener("click", () => {
  if (!lastResult?.download_transcript_url) return showError("No transcript download link yet.");
  const base = backendUrl.value.trim().replace(/\/$/, "");
  window.open(base + lastResult.download_transcript_url, "_blank");
});

dlSummaryBtn.addEventListener("click", () => {
  if (!lastResult?.download_summary_url) return showError("No summary download link yet.");
  const base = backendUrl.value.trim().replace(/\/$/, "");
  window.open(base + lastResult.download_summary_url, "_blank");
});
