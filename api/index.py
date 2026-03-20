from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# Aapka pasandeeda design
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeraPlayer Pro | Ultra Bypass</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { max-width: 500px; margin: auto; background: #1e293b; padding: 30px; border-radius: 20px; border: 2px solid #00ff88; box-shadow: 0 0 25px rgba(0,255,136,0.2); }
        h1 span { color: #00ff88; }
        input { width: 90%; padding: 14px; margin: 15px 0; border-radius: 10px; border: none; background: #334155; color: white; outline: none; }
        button { background: #00ff88; color: black; border: none; padding: 14px 30px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; }
        #status { margin-top: 20px; color: #94a3b8; font-size: 14px; }
        video { width: 100%; margin-top: 20px; border-radius: 10px; display: none; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
    </style>
</head>
<body>
    <div class="box">
        <h1>TeraPlayer <span>Pro</span></h1>
        <p>Bypassing TeraBox Security...</p>
        <input type="text" id="url" placeholder="Paste link here...">
        <button onclick="runBypass()">🚀 UNLOCK & PLAY</button>
        <div id="status">System Online.</div>
        <video id="p" controls></video>
    </div>

    <script>
        async function runBypass() {
            const url = document.getElementById('url').value;
            const status = document.getElementById('status');
            const p = document.getElementById('p');
            if(!url) return;

            status.innerHTML = "⚡ Initializing Exploit...";
            status.style.color = "#00ff88";

            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                
                if(data.status === 'success') {
                    status.innerHTML = "✅ Success: " + data.title;
                    p.src = data.download_link;
                    p.style.display = "block";
                    p.play();
                } else {
                    status.innerHTML = "❌ " + data.message;
                    status.style.color = "#ff4d4d";
                }
            } catch(e) { status.innerHTML = "❌ Connection Refused!"; }
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
        match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
        surl = match.group(1) if match else url.split('/')[-1]

        # --- ADVANCED BYPASS API ---
        # Ye aik public worker hai jo TeraBox ke cookies aur tokens manage karta hai
        api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl={surl}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.terabox.com/"
        }

        r = requests.get(api_url, headers=headers, timeout=15)
        res = r.json()

        if 'download_link' in res:
            return jsonify({
                "status": "success",
                "title": res.get('file_name', 'Bypassed Video'),
                "download_link": res['download_link']
            })
        
        return jsonify({"status": "error", "message": "TeraBox is rotating keys. Try a different link or wait 2 mins."}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": "Server Overloaded"}), 500
    
