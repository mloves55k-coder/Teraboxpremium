from flask import Flask, request, jsonify, render_template_string
import requests
import re
import time

app = Flask(__name__)

# --- UI (Aapka Preferred Design) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeraPlayer Pro | Fixed</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #1e293b; padding: 25px; border-radius: 15px; border: 2px solid #00ff88; }
        input { width: 90%; padding: 12px; margin: 15px 0; border-radius: 8px; border: none; background: #334155; color: white; }
        button { background: #00ff88; color: black; border: none; padding: 12px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; }
        #status { margin-top: 20px; font-size: 14px; color: #94a3b8; }
        video { width: 100%; margin-top: 20px; border-radius: 10px; display: none; }
        .dl-btn { display: none; margin-top: 10px; color: #00ff88; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TeraPlayer <span>Pro</span></h1>
        <input type="text" id="url" placeholder="Paste TeraBox Link Here">
        <button onclick="startBypass()">🚀 PLAY NOW</button>
        <div id="status">Ready to bypass...</div>
        <video id="v-player" controls playsinline></video>
        <br><a id="d-link" class="dl-btn" target="_blank">Download File</a>
    </div>

    <script>
        async function startBypass() {
            const url = document.getElementById('url').value;
            const status = document.getElementById('status');
            if(!url) return alert("Link kahan hai?");
            
            status.innerText = "⚡ Cracking TeraBox Security...";
            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                if(data.status === 'success') {
                    status.innerText = "✅ Found: " + data.title;
                    const v = document.getElementById('v-player');
                    const d = document.getElementById('d-link');
                    v.src = data.download_link;
                    v.style.display = "block";
                    d.href = data.download_link;
                    d.style.display = "inline-block";
                    v.play();
                } else {
                    status.innerText = "❌ Blocked: " + data.message;
                }
            } catch(e) { status.innerText = "❌ Connection Failed!"; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        url = data.get('url', '')
        match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
        surl = match.group(1) if match else url.split('/')[-1]

        # --- REVOLUTIONARY METHOD: Using a more stable public proxy API ---
        # Ye APIs specifically TeraBox security ke liye bani hain
        proxies = [
            f"https://terabox-api-topaz.vercel.app/api?id={surl}",
            f"https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl={surl}"
        ]

        for p_api in proxies:
            try:
                r = requests.get(p_api, timeout=12)
                res = r.json()
                
                # Handling Structure 1
                if 'download_link' in res:
                    return jsonify({
                        "status": "success",
                        "title": res.get('file_name', 'TeraBox Video'),
                        "download_link": res['download_link']
                    })
                # Handling Structure 2
                elif 'list' in res and len(res['list']) > 0:
                    return jsonify({
                        "status": "success",
                        "title": res['list'][0].get('server_filename'),
                        "download_link": res['list'][0].get('dlink')
                    })
            except:
                continue

        return jsonify({"status": "error", "message": "TeraBox is too strong right now. Please try again in 5 minutes."}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": "Backend Glitch"}), 500
        
