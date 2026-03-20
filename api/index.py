from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# --- PREMIUM DESIGN (No Changes Needed) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeraPlayer Pro | Ultra Bypass</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { max-width: 500px; margin: auto; background: #1e293b; padding: 30px; border-radius: 15px; border: 2px solid #00ff88; box-shadow: 0 0 20px rgba(0,255,136,0.2); }
        h1 span { color: #00ff88; }
        input { width: 90%; padding: 12px; margin: 15px 0; border-radius: 8px; border: none; background: #334155; color: white; outline: none; }
        button { background: #00ff88; color: black; border: none; padding: 12px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; transition: 0.3s; }
        button:hover { background: #00cc6e; transform: scale(1.02); }
        #status { margin-top: 20px; color: #94a3b8; font-size: 14px; }
        video { width: 100%; margin-top: 20px; border-radius: 10px; display: none; border: 1px solid #334155; }
        .dl-link { display: none; margin-top: 15px; color: #00ff88; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h1>TeraPlayer <span>Pro</span></h1>
        <p>Ultra High-Speed Bypass</p>
        <input type="text" id="url" placeholder="Paste TeraBox/1024terabox Link">
        <button onclick="ultimateBypass()">PLAY VIDEO</button>
        <div id="status">Ready to stream...</div>
        <video id="player" controls playsinline></video>
        <br>
        <a id="downloadLink" class="dl-link" target="_blank">⬇️ Download Video</a>
    </div>

    <script>
        async function ultimateBypass() {
            const url = document.getElementById('url').value;
            const status = document.getElementById('status');
            const player = document.getElementById('player');
            const dl = document.getElementById('downloadLink');

            if(!url) return alert("Bhai, link toh paste karein!");
            
            status.innerHTML = "🚀 Breaking TeraBox Security...";
            status.style.color = "#00ff88";

            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                
                if(data.status === 'success') {
                    status.innerHTML = "✅ Streaming: " + data.title;
                    player.src = data.download_link;
                    player.style.display = "block";
                    dl.href = data.download_link;
                    dl.style.display = "inline-block";
                    player.play();
                } else {
                    status.innerHTML = "❌ Security Alert: " + data.message;
                    status.style.color = "#ff4d4d";
                }
            } catch(e) { 
                status.innerHTML = "❌ Connection Timeout! Try again."; 
                status.style.color = "#ff4d4d";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        original_url = data.get('url', '')
        
        # SURL Extraction
        match = re.search(r'/s/([a-zA-Z0-9_-]+)', original_url)
        surl = match.group(1) if match else original_url.split('/')[-1]

        # --- METHOD 1: THIRD PARTY OPEN API (High Success Rate) ---
        api_endpoints = [
            f"https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl={surl}",
            f"https://terabox-api.vercel.app/api?id={surl}"
        ]

        for api in api_endpoints:
            try:
                r = requests.get(api, timeout=10)
                res = r.json()
                
                # Handling different API response structures
                if 'download_link' in res:
                    return jsonify({
                        "status": "success",
                        "title": res.get('file_name', 'Video File'),
                        "download_link": res['download_link']
                    })
                elif 'list' in res:
                    return jsonify({
                        "status": "success",
                        "title": res['list'][0].get('server_filename'),
                        "download_link": res['list'][0].get('dlink')
                    })
            except:
                continue

        return jsonify({"status": "error", "message": "TeraBox Server is Busy. Please try another link or refresh."}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": "Internal Logic Error"}), 500
        
