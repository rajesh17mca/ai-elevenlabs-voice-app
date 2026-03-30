import cgi
import io
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # George
TTS_MODEL = "eleven_v3"
STT_MODEL = "scribe_v1"

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ElevenLabs Studio</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0f0f13;
      --surface: #1a1a24;
      --surface2: #22222f;
      --border: #2e2e3e;
      --accent: #007bff;
      --accent-hover: #0056b3;
      --accent-light: rgba(0,123,255,0.15);
      --text: #e8e8f0;
      --text-muted: #8888a8;
      --success: #22c55e;
      --danger: #ef4444;
      --radius: 12px;
    }

    body {
      font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    header {
      width: 100%;
      padding: 24px 40px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 12px;
    }

    header .logo {
      width: 32px; height: 32px;
      background: var(--accent);
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 18px;
    }

    header h1 { font-size: 20px; font-weight: 600; letter-spacing: -0.3px; }
    header span { font-size: 13px; color: var(--text-muted); margin-left: 4px; }

    main {
      width: 100%;
      max-width: 800px;
      padding: 40px 24px;
      flex: 1;
    }

    .tabs {
      display: flex;
      gap: 4px;
      background: var(--surface);
      border-radius: var(--radius);
      padding: 4px;
      margin-bottom: 32px;
    }

    .tab-btn {
      flex: 1;
      padding: 10px 20px;
      border: none;
      border-radius: 9px;
      background: transparent;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }

    .tab-btn.active {
      background: var(--accent);
      color: #fff;
    }

    .tab-panel { display: none; }
    .tab-panel.active { display: flex; flex-direction: column; gap: 20px; }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
    }

    label {
      display: block;
      font-size: 13px;
      font-weight: 500;
      color: var(--text-muted);
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    textarea {
      width: 100%;
      min-height: 140px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 15px;
      line-height: 1.6;
      padding: 14px;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
      font-family: inherit;
    }

    textarea:focus { border-color: var(--accent); }

    .char-count {
      font-size: 12px;
      color: var(--text-muted);
      text-align: right;
      margin-top: 6px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 24px;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      text-decoration: none;
    }

    .btn-primary {
      background: var(--accent);
      color: #fff;
    }

    .btn-primary:hover:not(:disabled) { background: var(--accent-hover); }

    .btn-secondary {
      background: var(--surface2);
      color: var(--text);
      border: 1px solid var(--border);
    }

    .btn-secondary:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }

    .btn:disabled { opacity: 0.45; cursor: not-allowed; }

    .btn-row { display: flex; gap: 10px; flex-wrap: wrap; }

    .drop-zone {
      border: 2px dashed var(--border);
      border-radius: var(--radius);
      padding: 48px 24px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      background: var(--surface2);
    }

    .drop-zone:hover, .drop-zone.drag-over {
      border-color: var(--accent);
      background: var(--accent-light);
    }

    .drop-zone input[type=file] { display: none; }

    .drop-zone .icon { font-size: 36px; margin-bottom: 12px; }
    .drop-zone p { color: var(--text-muted); font-size: 14px; line-height: 1.6; }
    .drop-zone strong { color: var(--text); }

    .file-info {
      display: none;
      align-items: center;
      gap: 12px;
      background: var(--accent-light);
      border: 1px solid var(--accent);
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 14px;
    }

    .file-info.visible { display: flex; }

    .result-box {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      font-size: 15px;
      line-height: 1.7;
      min-height: 80px;
      white-space: pre-wrap;
      word-break: break-word;
    }

    audio {
      width: 100%;
      border-radius: 8px;
      accent-color: var(--accent);
    }

    .status {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      padding: 10px 16px;
      border-radius: 8px;
      display: none;
    }

    .status.info { background: var(--accent-light); color: var(--accent-hover); display: flex; }
    .status.success { background: rgba(34,197,94,0.1); color: var(--success); display: flex; }
    .status.error { background: rgba(239,68,68,0.1); color: var(--danger); display: flex; }

    .spinner {
      width: 16px; height: 16px;
      border: 2px solid currentColor;
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      flex-shrink: 0;
    }

    @keyframes spin { to { transform: rotate(360deg); } }

    footer {
      text-align: center;
      padding: 20px;
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      width: 100%;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo">RK</div>
    <h1>ElevenLabs Studio</h1>
    <span>Powered by ElevenLabs AI</span>
  </header>

  <main>
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab('tts')">Text to Speech</button>
      <button class="tab-btn" onclick="switchTab('stt')">Speech to Text</button>
    </div>

    <!-- TTS Panel -->
    <div id="tts-panel" class="tab-panel active">
      <div class="card">
        <label for="tts-input">Enter text</label>
        <textarea id="tts-input" placeholder="Type or paste your text here…" oninput="updateCharCount()"></textarea>
        <div class="char-count"><span id="char-count">0</span> characters</div>
      </div>

      <div id="tts-status" class="status"></div>

      <div class="btn-row">
        <button class="btn btn-primary" id="tts-btn" onclick="convertTTS()">
          <span>Convert to Speech</span>
        </button>
      </div>

      <div id="tts-result" class="card" style="display:none;">
        <label>Audio Output</label>
        <audio id="tts-audio" controls></audio>
        <div class="btn-row" style="margin-top:16px;">
          <a id="tts-download" class="btn btn-secondary" download="speech.mp3">
            ⬇ Download MP3
          </a>
        </div>
      </div>
    </div>

    <!-- STT Panel -->
    <div id="stt-panel" class="tab-panel">
      <div class="card">
        <label>Upload Audio File</label>
        <div class="drop-zone" id="drop-zone" onclick="document.getElementById('stt-file').click()"
             ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event)">
          <input type="file" id="stt-file" accept="audio/*,video/*" onchange="handleFileSelect(event)" />
          <div class="icon">🎵</div>
          <p><strong>Click to upload</strong> or drag and drop<br/>MP3, WAV, M4A, OGG, FLAC, MP4 supported</p>
        </div>
        <div class="file-info" id="file-info">
          <span>📄</span>
          <span id="file-name"></span>
          <span id="file-size" style="color:var(--text-muted);margin-left:auto;"></span>
        </div>
      </div>

      <div id="stt-status" class="status"></div>

      <div class="btn-row">
        <button class="btn btn-primary" id="stt-btn" onclick="convertSTT()" disabled>
          <span>Transcribe Audio</span>
        </button>
      </div>

      <div id="stt-result" class="card" style="display:none;">
        <label>Transcription</label>
        <div class="result-box" id="stt-text"></div>
        <div class="btn-row" style="margin-top:16px;">
          <button class="btn btn-secondary" onclick="downloadTXT()">⬇ Download TXT</button>
        </div>
      </div>
    </div>
  </main>

  <footer>ElevenLabs Studio &mdash; Text to Speech &amp; Speech to Text</footer>

  <script>
    let selectedFile = null;
    let ttsAudioBlob = null;

    function switchTab(tab) {
      document.querySelectorAll('.tab-btn').forEach((b, i) => {
        b.classList.toggle('active', (tab === 'tts' && i === 0) || (tab === 'stt' && i === 1));
      });
      document.getElementById('tts-panel').classList.toggle('active', tab === 'tts');
      document.getElementById('stt-panel').classList.toggle('active', tab === 'stt');
    }

    function updateCharCount() {
      const len = document.getElementById('tts-input').value.length;
      document.getElementById('char-count').textContent = len.toLocaleString();
    }

    function setStatus(id, type, message, loading = false) {
      const el = document.getElementById(id);
      el.className = 'status ' + type;
      el.innerHTML = loading
        ? `<div class="spinner"></div><span>${message}</span>`
        : `<span>${message}</span>`;
    }

    function hideStatus(id) {
      document.getElementById(id).className = 'status';
    }

    async function convertTTS() {
      const text = document.getElementById('tts-input').value.trim();
      if (!text) { setStatus('tts-status', 'error', 'Please enter some text first.'); return; }

      const btn = document.getElementById('tts-btn');
      btn.disabled = true;
      document.getElementById('tts-result').style.display = 'none';
      setStatus('tts-status', 'info', 'Converting text to speech…', true);

      try {
        const res = await fetch('/api/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text }),
        });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.error || 'Conversion failed');
        }
        const blob = await res.blob();
        ttsAudioBlob = blob;
        const url = URL.createObjectURL(blob);
        document.getElementById('tts-audio').src = url;
        document.getElementById('tts-download').href = url;
        document.getElementById('tts-result').style.display = 'block';
        setStatus('tts-status', 'success', 'Audio generated successfully!');
      } catch (e) {
        setStatus('tts-status', 'error', e.message);
      } finally {
        btn.disabled = false;
      }
    }

    function handleFileSelect(e) {
      setFile(e.target.files[0]);
    }

    function handleDragOver(e) {
      e.preventDefault();
      document.getElementById('drop-zone').classList.add('drag-over');
    }

    function handleDragLeave() {
      document.getElementById('drop-zone').classList.remove('drag-over');
    }

    function handleDrop(e) {
      e.preventDefault();
      document.getElementById('drop-zone').classList.remove('drag-over');
      const file = e.dataTransfer.files[0];
      if (file) setFile(file);
    }

    function setFile(file) {
      selectedFile = file;
      document.getElementById('file-name').textContent = file.name;
      document.getElementById('file-size').textContent = formatBytes(file.size);
      document.getElementById('file-info').classList.add('visible');
      document.getElementById('stt-btn').disabled = false;
      document.getElementById('stt-result').style.display = 'none';
      hideStatus('stt-status');
    }

    function formatBytes(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / 1048576).toFixed(1) + ' MB';
    }

    async function convertSTT() {
      if (!selectedFile) return;

      const btn = document.getElementById('stt-btn');
      btn.disabled = true;
      document.getElementById('stt-result').style.display = 'none';
      setStatus('stt-status', 'info', 'Transcribing audio…', true);

      try {
        const form = new FormData();
        form.append('file', selectedFile);

        const res = await fetch('/api/stt', { method: 'POST', body: form });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.error || 'Transcription failed');
        }
        const data = await res.json();
        document.getElementById('stt-text').textContent = data.text;
        document.getElementById('stt-result').style.display = 'block';
        setStatus('stt-status', 'success', 'Transcription complete!');
      } catch (e) {
        setStatus('stt-status', 'error', e.message);
      } finally {
        btn.disabled = false;
      }
    }

    function downloadTXT() {
      const text = document.getElementById('stt-text').textContent;
      const blob = new Blob([text], { type: 'text/plain' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'transcription.txt';
      a.click();
    }
  </script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"  {self.address_string()} - {format % args}")

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/api/tts":
            self._handle_tts()
        elif self.path == "/api/stt":
            self._handle_stt()
        else:
            self.send_json(404, {"error": "Not found"})

    def _handle_tts(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            text = data.get("text", "").strip()
            if not text:
                return self.send_json(400, {"error": "text is required"})

            audio = b"".join(client.text_to_speech.convert(
                text=text,
                voice_id=VOICE_ID,
                model_id=TTS_MODEL,
                output_format="mp3_44100_128",
            ))

            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(audio)))
            self.send_header("Content-Disposition", 'attachment; filename="speech.mp3"')
            self.end_headers()
            self.wfile.write(audio)
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    def _handle_stt(self):
        content_type = self.headers.get("Content-Type", "")
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            # Parse multipart form data
            environ = {
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": content_type,
                "CONTENT_LENGTH": str(length),
            }
            form = cgi.FieldStorage(
                fp=io.BytesIO(body),
                environ=environ,
                keep_blank_values=True,
            )
            file_item = form["file"]
            audio_bytes = file_item.file.read()
            filename = file_item.filename or "audio.mp3"

            result = client.speech_to_text.convert(
                file=(filename, io.BytesIO(audio_bytes)),
                model_id=STT_MODEL,
            )
            self.send_json(200, {"text": result.text})
        except Exception as e:
            self.send_json(500, {"error": str(e)})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"ElevenLabs Studio running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
