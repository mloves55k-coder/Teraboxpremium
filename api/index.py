from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# --- FRONTEND (Wahi design jo aapko pasand hai) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeraPlayer Pro | Bypass King</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { max-width: 500px; margin: auto; background: #1e293b; padding: 30px; border-radius: 15px; border: 1px solid #00ff88; }
        input { width: 90%; padding: 12px; margin: 10px 0; border-radius: 8px; border: none; background: #334155; color: white; }
        button { background: #00ff88; color: black; border: none; padding: 12px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; }
        video { width: 100%; margin-top: 20px; border-radius: 10px; display: none; }
        #status { margin-top: 15px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>TeraPlayer <span>Pro</span></h1>
        <input type="text" id="url" placeholder="Paste TeraBox Link Here">
        <button onclick="bypass()">PLAY NOW</button>
        <div id="status"></div>
        <video id="player" controls></video>
    </div>

    <script>
        async function bypass() {
            const url = document.getElementById('url').value;
            const status = document.getElementById('status');
            const player = document.getElementById('player');
            if(!url) return alert("Link kahan hai?");
            
            status.innerHTML = "⏳ Bypassing Security...";
            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                if(data.status === 'success') {
                    status.innerHTML = "✅ Playing: " + data.title;
                    player.src = data.download_link;
                    player.style.display = "block";
                    player.play();
                } else {
                    status.innerHTML = "❌ Blocked: " + data.message;
                }
            } catch(e) { status.innerHTML = "❌ Server Error!"; }
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
        
        # SURL Extraction
        match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
        surl = match.group(1) if match else url.split('/')[-1]

        # --- YE HAI REAL BYPASS LOGIC ---
        # Hum direct dlink fetch karenge bina kisi middleman ke
        api_url = f"https://www.teraboxapp.com/share/list?app_id=250528&surl={surl}&shorturl={surl}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            "Accept": "application/json",
            "X-Requested-With": "com.dubox.drive"
        }

        r = requests.get(api_url, headers=headers, timeout=15)
        res = r.json()

        if 'list' in res and len(res['list']) > 0:
            file_data = res['list'][0]
            # Direct link extraction
            dlink = file_data.get('dlink')
            
            return jsonify({
                "status": "success",
                "title": file_data.get('server_filename'),
                "download_link": dlink
            })
        
        return jsonify({"status": "error", "message": "TeraBox ne block kiya hai. Naya Link try karein."}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": "Server Busy"}), 500
        
