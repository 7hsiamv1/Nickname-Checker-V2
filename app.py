from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

GARENA_API_URL = "https://shop.garena.my/api/auth/player_id_login"

HEADERS = {
    "sec-ch-ua-platform": "\"Android\"",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Infinix X6837 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7727.55 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Android WebView\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?1",
    "Origin": "https://shop.garena.my",
    "X-Requested-With": "mark.via.gp",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://shop.garena.my/?channel=202953",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": (
        "source=mb; region=MY; language=en; "
        "mspid2=5a0d9bcdd4dfc077158dcebd20bd0035; "
        "_fbp=fb.1.1777226630722.236627174334749579; "
        "datadome=mWe_SuotviZaUJY6jNlmjo6nyuxArpSTftTi5IDEvpn6n6gsZZRv7xO0e_nQ4UEq6N0Zf7TPkZUHkgFdinG6SsLRlwmRuT8wGj_U10ZVeDmbsIhkbRRracgoME2~8TLV"
    ),
    "Connection": "keep-alive",
}

APP_IDS = {
    "BD": 100067,
    "MY": 100067,
    "SG": 100067,
    "TH": 100067,
    "ID": 100067,
    "PH": 100067,
    "VN": 100067,
    "TW": 100067,
}


@app.route("/<region>/player-info", methods=["GET"])
def player_info(region):
    region = region.upper()

    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "uid parameter is required"}), 400

    app_id = APP_IDS.get(region, 100067)

    payload = {
        "app_id": app_id,
        "login_id": uid
    }

    try:
        response = requests.post(
            GARENA_API_URL,
            json=payload,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({"error": f"Garena API returned status {response.status_code}"}), 502

        data = response.json()

        nickname = data.get("nickname")
        if not nickname:
            return jsonify({"error": "Player not found or invalid UID"}), 404

        return jsonify({"nickname": nickname})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Garena API timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Free Fire UID Checker</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --ff-orange: #ff6b00;
      --ff-yellow: #ffd700;
      --ff-dark: #0a0a0f;
      --ff-card: #111118;
      --ff-border: #2a2a3a;
    }
    body {
      min-height: 100vh;
      background: var(--ff-dark);
      font-family: 'Rajdhani', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow-x: hidden;
      position: relative;
    }
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(255,107,0,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(255,34,68,0.08) 0%, transparent 60%);
      pointer-events: none;
      z-index: 0;
    }
    body::after {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,107,0,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,107,0,0.04) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
      z-index: 0;
    }
    .container {
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 520px;
      padding: 20px;
    }
    .logo-area {
      text-align: center;
      margin-bottom: 40px;
      animation: fadeDown 0.7s ease both;
    }
    .flame-icon {
      font-size: 52px;
      display: block;
      margin-bottom: 10px;
      animation: pulse 2s ease-in-out infinite;
      filter: drop-shadow(0 0 18px var(--ff-orange));
    }
    .logo-title {
      font-family: 'Orbitron', monospace;
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 4px;
      text-transform: uppercase;
      background: linear-gradient(135deg, var(--ff-orange), var(--ff-yellow));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .logo-sub {
      font-size: 13px;
      color: rgba(255,255,255,0.35);
      letter-spacing: 6px;
      text-transform: uppercase;
      margin-top: 6px;
    }
    .card {
      background: var(--ff-card);
      border: 1px solid var(--ff-border);
      border-radius: 20px;
      padding: 36px 32px;
      position: relative;
      overflow: hidden;
      animation: fadeUp 0.7s ease 0.1s both;
      box-shadow: 0 0 0 1px rgba(255,107,0,0.1), 0 20px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--ff-orange), var(--ff-yellow), var(--ff-orange), transparent);
      animation: scanline 3s ease-in-out infinite;
    }
    .field-label {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: rgba(255,255,255,0.4);
      margin-bottom: 10px;
      display: block;
    }
    .region-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 24px;
    }
    .region-btn {
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--ff-border);
      border-radius: 8px;
      color: rgba(255,255,255,0.5);
      font-family: 'Orbitron', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 7px 14px;
      cursor: pointer;
      transition: all 0.2s ease;
      letter-spacing: 1px;
    }
    .region-btn:hover { border-color: var(--ff-orange); color: var(--ff-orange); background: rgba(255,107,0,0.08); }
    .region-btn.active {
      background: linear-gradient(135deg, rgba(255,107,0,0.25), rgba(255,215,0,0.1));
      border-color: var(--ff-orange);
      color: var(--ff-yellow);
      box-shadow: 0 0 12px rgba(255,107,0,0.3);
    }
    .input-wrap { position: relative; margin-bottom: 22px; }
    .uid-input {
      width: 100%;
      background: rgba(255,255,255,0.04);
      border: 1.5px solid var(--ff-border);
      border-radius: 12px;
      color: #fff;
      font-family: 'Orbitron', monospace;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 2px;
      padding: 16px 20px 16px 54px;
      outline: none;
      transition: all 0.3s ease;
    }
    .uid-input::placeholder { color: rgba(255,255,255,0.18); font-size: 14px; letter-spacing: 3px; font-weight: 400; }
    .uid-input:focus { border-color: var(--ff-orange); background: rgba(255,107,0,0.06); box-shadow: 0 0 0 3px rgba(255,107,0,0.15), 0 0 20px rgba(255,107,0,0.1); }
    .input-icon { position: absolute; left: 18px; top: 50%; transform: translateY(-50%); font-size: 20px; opacity: 0.5; pointer-events: none; }
    .check-btn {
      width: 100%;
      background: linear-gradient(135deg, #ff6b00, #ff9500, #ffd700);
      border: none;
      border-radius: 12px;
      color: #000;
      font-family: 'Orbitron', monospace;
      font-size: 14px;
      font-weight: 900;
      letter-spacing: 4px;
      text-transform: uppercase;
      padding: 17px;
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(255,107,0,0.4);
    }
    .check-btn::before {
      content: '';
      position: absolute;
      top: 0; left: -100%;
      width: 100%; height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
      transition: left 0.5s ease;
    }
    .check-btn:hover::before { left: 100%; }
    .check-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(255,107,0,0.6); }
    .check-btn:active { transform: translateY(0); }
    .check-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
    .spinner {
      display: inline-block;
      width: 16px; height: 16px;
      border: 2px solid rgba(0,0,0,0.3);
      border-top-color: #000;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      vertical-align: middle;
      margin-right: 8px;
    }
    .result-box {
      margin-top: 24px;
      border-radius: 14px;
      padding: 22px 24px;
      opacity: 0;
      transform: translateY(10px);
      transition: all 0.4s ease;
      display: none;
    }
    .result-box.show { opacity: 1; transform: translateY(0); display: block; }
    .result-box.success { background: linear-gradient(135deg, rgba(0,255,128,0.07), rgba(0,200,100,0.04)); border: 1px solid rgba(0,255,128,0.25); }
    .result-box.error { background: linear-gradient(135deg, rgba(255,34,68,0.08), rgba(255,0,50,0.04)); border: 1px solid rgba(255,34,68,0.25); }
    .result-label { font-size: 10px; letter-spacing: 4px; text-transform: uppercase; font-weight: 700; margin-bottom: 10px; }
    .result-box.success .result-label { color: rgba(0,255,128,0.6); }
    .result-box.error .result-label { color: rgba(255,34,68,0.6); }
    .result-icon { font-size: 28px; margin-bottom: 8px; display: block; }
    .result-nickname { font-family: 'Orbitron', monospace; font-size: 22px; font-weight: 900; color: #fff; word-break: break-all; line-height: 1.4; }
    .result-uid-badge { display: inline-block; background: rgba(255,255,255,0.06); border-radius: 6px; padding: 3px 10px; font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 10px; font-family: 'Orbitron', monospace; letter-spacing: 1px; }
    .error-msg { font-size: 16px; color: rgba(255,80,100,0.9); font-weight: 600; }
    .footer { text-align: center; margin-top: 28px; font-size: 11px; color: rgba(255,255,255,0.18); letter-spacing: 2px; text-transform: uppercase; animation: fadeUp 0.7s ease 0.3s both; }
    @keyframes fadeDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0%, 100% { transform: scale(1); filter: drop-shadow(0 0 18px var(--ff-orange)); } 50% { transform: scale(1.08); filter: drop-shadow(0 0 30px var(--ff-orange)); } }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes scanline { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
    @media (max-width: 480px) { .card { padding: 28px 20px; } .logo-title { font-size: 20px; } .uid-input { font-size: 15px; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo-area">
      <span class="flame-icon">🔥</span>
      <div class="logo-title">Free Fire</div>
      <div class="logo-sub">UID Checker</div>
    </div>
    <div class="card">
      <label class="field-label">Select Region</label>
      <div class="region-grid" id="regionGrid">
        <button class="region-btn active" data-region="BD">BD</button>
        <button class="region-btn" data-region="MY">MY</button>
        <button class="region-btn" data-region="SG">SG</button>
        <button class="region-btn" data-region="TH">TH</button>
        <button class="region-btn" data-region="ID">ID</button>
        <button class="region-btn" data-region="PH">PH</button>
        <button class="region-btn" data-region="VN">VN</button>
        <button class="region-btn" data-region="TW">TW</button>
      </div>
      <label class="field-label" for="uidInput">Player UID</label>
      <div class="input-wrap">
        <span class="input-icon">🎮</span>
        <input type="text" id="uidInput" class="uid-input" placeholder="Enter UID..." maxlength="20" autocomplete="off" inputmode="numeric"/>
      </div>
      <button class="check-btn" id="checkBtn" onclick="checkUID()">⚡ CHECK PLAYER</button>
      <div class="result-box" id="resultBox">
        <span class="result-icon" id="resultIcon"></span>
        <div class="result-label" id="resultLabel"></div>
        <div id="resultContent"></div>
      </div>
    </div>
    <div class="footer">Powered by Garena API &nbsp;•&nbsp; Free Fire</div>
  </div>
  <script>
    let selectedRegion = 'BD';
    document.getElementById('regionGrid').addEventListener('click', function(e) {
      const btn = e.target.closest('.region-btn');
      if (!btn) return;
      document.querySelectorAll('.region-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedRegion = btn.dataset.region;
    });
    document.getElementById('uidInput').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') checkUID();
    });
    async function checkUID() {
      const uid = document.getElementById('uidInput').value.trim();
      const btn = document.getElementById('checkBtn');
      const resultBox = document.getElementById('resultBox');
      if (!uid) {
        showResult('error', '⚠️', 'Missing UID', '<div class="error-msg">Please enter a valid Player UID.</div>');
        return;
      }
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner"></span> CHECKING...';
      resultBox.classList.remove('show');
      resultBox.style.display = 'none';
      try {
        const res = await fetch('/' + selectedRegion + '/player-info?uid=' + encodeURIComponent(uid));
        const data = await res.json();
        if (res.ok && data.nickname) {
          showResult('success', '✅', 'Player Found',
            '<div class="result-nickname">' + escapeHtml(data.nickname) + '</div>' +
            '<div class="result-uid-badge">UID: ' + escapeHtml(uid) + ' &nbsp;•&nbsp; ' + selectedRegion + '</div>'
          );
        } else {
          const msg = data.error || 'Player not found or invalid UID.';
          showResult('error', '❌', 'Not Found', '<div class="error-msg">' + escapeHtml(msg) + '</div>');
        }
      } catch (err) {
        showResult('error', '⚠️', 'Network Error', '<div class="error-msg">Could not connect. Please try again.</div>');
      } finally {
        btn.disabled = false;
        btn.innerHTML = '⚡ CHECK PLAYER';
      }
    }
    function showResult(type, icon, label, content) {
      const box = document.getElementById('resultBox');
      document.getElementById('resultIcon').textContent = icon;
      document.getElementById('resultLabel').textContent = label;
      document.getElementById('resultContent').innerHTML = content;
      box.className = 'result-box ' + type;
      box.style.display = 'block';
      requestAnimationFrame(() => box.classList.add('show'));
    }
    function escapeHtml(str) {
      return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }
  </script>
</body>
</html>"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
