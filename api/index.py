from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# Aapka high-end UI design
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeraPlayer Pro | Parrot Engine</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { max-width: 450px; margin: auto; background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #00ff88; box-shadow: 0 0 20px rgba(0,255,136,0.2); }
        input { width: 90%; padding: 14px; margin: 15px 0; border-radius: 10px; border: none; background: #334155; color: white; outline: none; }
        button { background: #00ff88; color: black; border: none; padding: 14px; border-radius: 10px; font-weight: bold; width: 100%; cursor: pointer; font-size: 16px; }
        #status { margin-top: 20px; font-size: 14px; color: #94a3b8; }
        video { width: 100%; margin-top: 20px; border-radius: 10px; display: none; }
    </style>
</head>
<body>
    <div class="box">
        <h1>TeraPlayer <span>Pro</span></h1>
        <p>Parrot-Bypass Engine v3.0</p>
        <input type="text" id="url" placeholder="Paste TeraBox Link Here">
        <button onclick="parrotBypass()">🚀 UNLOCK & PLAY</button>
        <div id="status">Ready to decrypt...</div>
        <video id="player" controls playsinline></video>
    </div>

    <script>
        async function parrotBypass() {
            const url = document.getElementById('url').value;
            const status = document.getElementById('status');
            const player = document.getElementById('player');
            if(!url) return;

            status.innerHTML = "📡 Intercepting TeraBox Handshake...";
            status.style.color = "#00ff88";

            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                
                if(data.status === 'success') {
                    status.innerHTML = "✅ Bypassed! Playing: " + data.title;
                    player.src = data.download_link;
                    player.style.display = "block";
                    player.play();
                } else {
                    status.innerHTML = "❌ Security Error: " + data.message;
                    status.style.color = "#ff4d4d";
                }
            } catch(e) { status.innerHTML = "❌ Proxy Timeout!"; }
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
        url = data.get('url', '')
        
        # Clean SURL
        surl_match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
        surl = surl_match.group(1) if surl_match else url.split('/')[-1]

        # --- PARROT METHOD: Mobile App Emulation ---
        # Hum is API ko target karenge jo TeraBox ke liye "invisible" hai
        apis = [
            f"https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl={surl}",
            f"https://terabox-api-topaz.vercel.app/api?id={surl}"
        ]

        for target in apis:
            try:
                # App-Specific Headers
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
                    "X-Requested-With": "com.dubox.drive",
                    "Referer": "https://www.terabox.com/wap/share/filelist?surl=" + surl
                }
                
                r = requests.get(target, headers=headers, timeout=12)
                res = r.json()

                if 'download_link' in res:
                    return jsonify({
                        "status": "success",
                        "title": res.get('file_name', 'Video Found'),
                        "download_link": res['download_link']
                    })
                elif 'list' in res and len(res['list']) > 0:
                    return jsonify({
                        "status": "success",
                        "title": res['list'][0].get('server_filename'),
                        "download_link": res['list'][0].get('dlink')
                    })
            except:
                continue

        return jsonify({"status": "error", "message": "TeraBox Security updated. Please refresh."}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": "Logic Crash"}), 500
            
