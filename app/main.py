from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

APP_NAME = "turkcell-devops-app"

# Logs
LOG_DIR = Path("/var/log/app")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "requests.log"

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

app = FastAPI(title="DevOps Web Service")

# ✅ Custom metric: count messages by content
MESSAGE_COUNT_TOTAL = Counter(
    "message_count_total",
    "Total number of received messages grouped by content",
    ["content"],
)

# ✅ Basic HTTP metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    return """
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Request Sender</title>

  <style>
    :root{
      --bg1:#0b1220;
      --bg2:#0f172a;
      --card: rgba(255,255,255,.06);
      --card2: rgba(255,255,255,.08);
      --stroke: rgba(255,255,255,.10);
      --text: rgba(255,255,255,.92);
      --muted: rgba(255,255,255,.62);
      --shadow: 0 16px 50px rgba(0,0,0,.35);
      --radius: 18px;
      --accent: #7c3aed;   /* mor */
      --accent2:#22c55e;   /* yeşil */
      --warn:#f59e0b;
      --danger:#ef4444;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
    }

    *{ box-sizing:border-box; }
    body{
      margin:0;
      font-family: var(--sans);
      color: var(--text);
      background:
        radial-gradient(1200px 700px at 15% 10%, rgba(124,58,237,.25), transparent 60%),
        radial-gradient(900px 600px at 85% 20%, rgba(34,197,94,.20), transparent 55%),
        radial-gradient(900px 600px at 55% 90%, rgba(59,130,246,.18), transparent 55%),
        linear-gradient(180deg, var(--bg1), var(--bg2));
      min-height:100vh;
    }

    .wrap{
      max-width: 1100px;
      margin: 0 auto;
      padding: 40px 18px 60px;
    }

    header{
      display:flex;
      justify-content:space-between;
      align-items:flex-start;
      gap:16px;
      margin-bottom: 18px;
    }
    .title h1{
      margin:0;
      font-size: 34px;
      letter-spacing: -0.02em;
      line-height:1.12;
    }
    .title p{
      margin:10px 0 0;
      color: var(--muted);
      font-size: 14px;
    }

    .chips{
      display:flex;
      gap:10px;
      flex-wrap:wrap;
      justify-content:flex-end;
    }
    .chip{
      border:1px solid var(--stroke);
      background: rgba(255,255,255,.04);
      color: var(--muted);
      padding: 8px 10px;
      border-radius: 999px;
      font-size: 12px;
      display:flex;
      align-items:center;
      gap:8px;
      user-select:none;
    }
    .chip a{
      color: var(--text);
      text-decoration:none;
      font-weight:600;
    }

    .grid{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 18px;
    }

    @media (max-width: 900px){
      .grid{ grid-template-columns:1fr; }
      .chips{ justify-content:flex-start; }
    }

    .card{
      background: var(--card);
      border: 1px solid var(--stroke);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
    }
    .cardHead{
      padding: 16px 18px;
      border-bottom: 1px solid var(--stroke);
      background: linear-gradient(180deg, rgba(255,255,255,.06), transparent);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
    }
    .cardHead h2{
      margin:0;
      font-size: 16px;
      letter-spacing: -0.01em;
    }
    .badge{
      font-size: 12px;
      color: var(--muted);
      border:1px solid var(--stroke);
      background: rgba(255,255,255,.04);
      padding: 6px 10px;
      border-radius: 999px;
      display:flex;
      align-items:center;
      gap:8px;
    }
    .dot{
      width:8px;height:8px;border-radius:999px;
      background: var(--accent2);
      box-shadow: 0 0 0 3px rgba(34,197,94,.12);
    }

    .cardBody{ padding: 18px; }

    label{
      display:block;
      font-size: 13px;
      color: var(--muted);
      margin: 0 0 8px;
    }

    .row{
      display:grid;
      grid-template-columns: 1fr 180px;
      gap: 12px;
    }
    @media (max-width: 520px){
      .row{ grid-template-columns: 1fr; }
    }

    input, select{
      width:100%;
      padding: 12px 12px;
      border-radius: 12px;
      border: 1px solid var(--stroke);
      background: rgba(0,0,0,.18);
      color: var(--text);
      outline:none;
      font-size: 14px;
    }
    input::placeholder{ color: rgba(255,255,255,.35); }

    .presets{
      display:flex;
      gap:10px;
      flex-wrap:wrap;
      margin-top: 10px;
    }
    .presetBtn{
      border:1px solid var(--stroke);
      background: rgba(255,255,255,.04);
      color: var(--text);
      padding: 9px 10px;
      border-radius: 12px;
      font-size: 13px;
      cursor:pointer;
      transition: transform .08s ease, background .15s ease;
    }
    .presetBtn:hover{ background: rgba(255,255,255,.07); }
    .presetBtn:active{ transform: scale(.98); }

    .actions{
      display:flex;
      gap:10px;
      flex-wrap:wrap;
      margin-top: 14px;
    }
    .btn{
      border:1px solid var(--stroke);
      background: rgba(255,255,255,.04);
      color: var(--text);
      padding: 11px 12px;
      border-radius: 12px;
      font-weight: 650;
      letter-spacing: -0.01em;
      cursor:pointer;
      transition: transform .08s ease, background .15s ease, opacity .15s ease;
      display:inline-flex;
      align-items:center;
      gap:10px;
    }
    .btn:hover{ background: rgba(255,255,255,.07); }
    .btn:active{ transform: scale(.98); }
    .btn.primary{
      border-color: rgba(124,58,237,.55);
      background: linear-gradient(180deg, rgba(124,58,237,.35), rgba(124,58,237,.18));
    }
    .btn.primary:hover{
      background: linear-gradient(180deg, rgba(124,58,237,.45), rgba(124,58,237,.22));
    }
    .btn.ghost{ opacity:.88; }
    .btn.danger{
      border-color: rgba(239,68,68,.55);
      background: rgba(239,68,68,.10);
    }
    .btn:disabled{
      opacity:.55;
      cursor:not-allowed;
      transform:none;
    }

    .spinner{
      width:14px;height:14px;
      border:2px solid rgba(255,255,255,.25);
      border-top-color: rgba(255,255,255,.95);
      border-radius:999px;
      animation: spin .9s linear infinite;
      display:none;
    }
    @keyframes spin{ to{ transform:rotate(360deg); } }

    .hint{
      margin-top: 14px;
      color: var(--muted);
      font-size: 12.5px;
      line-height: 1.45;
    }
    code{
      font-family: var(--mono);
      font-size: 12.5px;
      background: rgba(0,0,0,.22);
      border:1px solid var(--stroke);
      padding: 2px 7px;
      border-radius: 10px;
      color: rgba(255,255,255,.86);
    }

    /* Result card */
    .statusLine{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      margin: 0 0 12px;
    }
    .ok{ color: #86efac; font-weight:700; }
    .bad{ color: #fecaca; font-weight:700; }
    .mini{
      color: var(--muted);
      font-size: 12px;
    }

    pre{
      margin:0;
      padding: 14px;
      border-radius: 16px;
      background: rgba(0,0,0,.35);
      border: 1px solid var(--stroke);
      overflow:auto;
      font-family: var(--mono);
      font-size: 12.5px;
      line-height: 1.45;
      min-height: 240px;
      max-height: 420px;
      white-space: pre-wrap;
      word-break: break-word;
    }

    .toast{
      position: fixed;
      right: 18px;
      bottom: 18px;
      background: rgba(0,0,0,.55);
      border:1px solid var(--stroke);
      color: var(--text);
      padding: 10px 12px;
      border-radius: 14px;
      box-shadow: var(--shadow);
      font-size: 13px;
      display:none;
    }
  </style>
</head>

<body>
  <div class="wrap">
    <header>
      <div class="title">
        <h1>Send a request</h1>
        <p>
          Bu ekran <code>POST /log</code> endpoint’ine JSON gönderir.
          Prometheus metrics: <code>/metrics</code>
        </p>
      </div>

      <div class="chips">
        <div class="chip"><span class="dot"></span>App: <a href="/" title="Ana sayfa">/</a></div>
        <div class="chip">Metrics: <a href="/metrics" target="_blank">/metrics</a></div>
        <div class="chip">Grafana: <a href="/grafana" target="_blank">/grafana</a></div>
        <div class="chip">Prometheus: <a href="/prometheus" target="_blank">/prometheus</a></div>
      </div>
    </header>

    <div class="grid">
      <!-- Left: form -->
      <section class="card">
        <div class="cardHead">
          <h2>Gönderim</h2>
          <div class="badge" id="envBadge">HTTPS • localhost</div>
        </div>

        <div class="cardBody">
          <div class="row">
            <div>
              <label for="message">Message</label>
              <input id="message" type="text" placeholder="deneme1" value="deneme1" />
              <div class="presets">
                <button class="presetBtn" data-preset="deneme1">deneme1</button>
                <button class="presetBtn" data-preset="deneme2">deneme2</button>
                <button class="presetBtn" data-preset="deneme3">deneme3</button>
              </div>
            </div>

            <div>
              <label for="times">Kaç kez gönderilsin?</label>
              <select id="times">
                <option value="1">1</option>
                <option value="5">5</option>
                <option value="10" selected>10</option>
                <option value="25">25</option>
                <option value="50">50</option>
              </select>
            </div>
          </div>

          <div class="actions">
            <button id="sendBtn" class="btn primary">
              <span class="spinner" id="spin"></span>
              <span>Send</span>
            </button>
            <button id="clearBtn" class="btn ghost">Clear</button>
            <button id="copyBtn" class="btn ghost">Copy curl</button>
          </div>

          <div class="hint">
            API: <code>POST /log</code> JSON: <code>{"message":"deneme1"}</code><br/>
            Not: UI, arka planda <code>fetch("/log")</code> ile çağırır (terminal şart değil).
          </div>
        </div>
      </section>

      <!-- Right: result -->
      <section class="card">
        <div class="cardHead">
          <h2>Result</h2>
          <div class="badge">
            <span id="statusDot" class="dot" style="background: var(--accent2)"></span>
            <span id="statusText">Hazır</span>
          </div>
        </div>

        <div class="cardBody">
          <div class="statusLine">
            <div>
              <div id="summary" class="mini">Henüz istek gönderilmedi.</div>
            </div>
            <div class="mini" id="lastTime">—</div>
          </div>
          <pre id="output">{ "hint": "Mesaj gönderince sonuç burada görünecek." }</pre>
        </div>
      </section>
    </div>
  </div>

  <div class="toast" id="toast">Kopyalandı ✅</div>

<script>
  const $ = (id) => document.getElementById(id);

  const messageEl = $("message");
  const timesEl = $("times");
  const sendBtn = $("sendBtn");
  const clearBtn = $("clearBtn");
  const copyBtn = $("copyBtn");
  const outEl = $("output");
  const summaryEl = $("summary");
  const lastTimeEl = $("lastTime");
  const spin = $("spin");
  const statusText = $("statusText");
  const statusDot = $("statusDot");
  const toast = $("toast");

  function setStatus(kind, text){
    statusText.textContent = text;
    if(kind === "ok"){
      statusDot.style.background = "var(--accent2)";
      statusDot.style.boxShadow = "0 0 0 3px rgba(34,197,94,.12)";
    }else if(kind === "warn"){
      statusDot.style.background = "var(--warn)";
      statusDot.style.boxShadow = "0 0 0 3px rgba(245,158,11,.12)";
    }else{
      statusDot.style.background = "var(--danger)";
      statusDot.style.boxShadow = "0 0 0 3px rgba(239,68,68,.12)";
    }
  }

  function showToast(text){
    toast.textContent = text;
    toast.style.display = "block";
    setTimeout(() => toast.style.display = "none", 1200);
  }

  function nowStr(){
    const d = new Date();
    return d.toLocaleString();
  }

  async function sendOnce(msg){
    const res = await fetch("/log", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message: msg})
    });
    let data = null;
    try{ data = await res.json(); } catch(e){}
    return { ok: res.ok, status: res.status, data };
  }

  async function sendMany(){
    const msg = (messageEl.value || "").trim();
    const times = parseInt(timesEl.value || "1", 10);

    if(!msg){
      setStatus("warn", "Message boş");
      outEl.textContent = '{ "error": "message is required" }';
      return;
    }

    // UI state
    sendBtn.disabled = true;
    clearBtn.disabled = true;
    copyBtn.disabled = true;
    spin.style.display = "inline-block";
    setStatus("warn", "Gönderiliyor...");

    let success = 0;
    let failed = 0;
    let last = null;

    for(let i=0; i<times; i++){
      try{
        last = await sendOnce(msg);
        if(last.ok) success++; else failed++;
      }catch(e){
        failed++;
        last = { ok:false, status:0, data:{ error: String(e) } };
      }
    }

    // Output
    const payload = {
      message: msg,
      times,
      success,
      failed,
      lastResponse: last
    };

    summaryEl.textContent = (failed === 0)
      ? `OK — ${success}/${times} gönderildi.`
      : `WARN — ${success}/${times} başarı, ${failed} hata.`;

    lastTimeEl.textContent = nowStr();
    outEl.textContent = JSON.stringify(payload, null, 2);

    setStatus((failed === 0) ? "ok" : "warn", (failed === 0) ? "OK" : "WARNING");

    // restore UI
    sendBtn.disabled = false;
    clearBtn.disabled = false;
    copyBtn.disabled = false;
    spin.style.display = "none";
  }

  // Preset buttons
  document.querySelectorAll("[data-preset]").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      messageEl.value = btn.getAttribute("data-preset");
      messageEl.focus();
    });
  });

  // Actions
  sendBtn.addEventListener("click", (e) => {
    e.preventDefault();
    sendMany();
  });

  clearBtn.addEventListener("click", (e) => {
    e.preventDefault();
    messageEl.value = "";
    summaryEl.textContent = "Temizlendi.";
    lastTimeEl.textContent = "—";
    outEl.textContent = '{ "hint": "Mesaj gönderince sonuç burada görünecek." }';
    setStatus("ok", "Hazır");
    messageEl.focus();
  });

  copyBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const msg = (messageEl.value || "deneme1").trim();
    const curl = `curl -sk https://localhost/log \\\n  -H "Content-Type: application/json" \\\n  -d '{"message":"${msg.replaceAll('"','\\\\\\"')}" }'`;
    try{
      await navigator.clipboard.writeText(curl);
      showToast("curl kopyalandı ✅");
    }catch(err){
      showToast("Kopyalama başarısız ❌");
    }
  });

  // Enter to send
  messageEl.addEventListener("keydown", (e) => {
    if(e.key === "Enter"){
      e.preventDefault();
      sendMany();
    }
  });
</script>

</body>
</html>
"""

@app.post("/log")
async def log_request(payload: dict, request: Request):
    message = str(payload.get("message", "")).strip()
    if not message:
        return PlainTextResponse("message is required", status_code=400)

    client_ip = request.client.host if request and request.client else "unknown"
    logger.info('message="%s" ip="%s"', message, client_ip)

    # ✅ increment metric
    MESSAGE_COUNT_TOTAL.labels(content=message).inc()

    return {"status": "ok", "message": message}
