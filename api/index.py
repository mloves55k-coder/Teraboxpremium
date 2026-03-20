from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# --- UI DESIGN ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeraPlayer Pro | Parrot Mode</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { max-width: 450px; margin: auto; background: #1e293b; padding: 25px; border-radius: 15px; border: 2px solid #00ff88; }
        input { width: 90%; padding: 12px; margin: 15px 0; border-radius: 8px; border: none; background: #334155; color: white; }
        button { background: #00ff88; color: black; border: none; padding: 12px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer; }
        video { width: 100%; margin-top: 20px; border-radius: 10px; display: none; }
        #status { margin-top: 15px; font-size: 13px; color: #94a3b8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>TeraPlayer <span>Pro</span></h1>
        <p>Using Parrot-Bypass Logic</p>
        <input type="text" id="url" placeholder="Paste TeraBox Link">
        <button onclick="start()">🚀 BYPASS & PLAY</button>
        <div id="status">Ready...</div>
        <video id="p" controls></video>
    </div>
    <script>
        async function start() {
            const url = document.getElementById('url').value;
            const status = document.getElementById('status');
            if(!url) return;
            status.innerText = "⏳ Connecting to Private API...";
            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                if(data.status === 'success') {
                    status.innerText = "✅ Bypassed Successfully!";
                    const v = document.getElementById('p');
                    v.src = data.download_link;
                    v.style.display = "block";
                    v.play();
                } else { status.innerText = "❌ Blocked: " + data.message; }
            } catch(e) { status.innerText = "❌ Connection Failed!"; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/api/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        url = data.get('url', '')
        # Extract SURL
        surl = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
        surl = surl.group(1) if surl else url.split('/')[-1]

        # --- PARROT BYPASS ENDPOINT ---
        # Ye aik public proxy hai jo cookies manage karti hai
        target = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl={surl}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36",
            "Referer": "https://www.terabox.com/"
        }

        r = requests.get(target, headers=headers, timeout=15)
        res = r.json()

        if 'download_link' in res:
            return jsonify({
                "status": "success",
                "title": res.get('file_name', 'Video'),
                "download_link": res['download_link']
            })
        
        return jsonify({"status": "error", "message": "TeraBox Security is high. Try again."}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": "Proxy Offline"}), 500
            
