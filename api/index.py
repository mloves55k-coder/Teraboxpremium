from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

# --- YE HAI AAPKA FRONTEND (HTML + CSS + JS) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeraPlayer Pro | Vercel Edition</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #00ff88; --bg: #0f172a; --card: #1e293b; }
        body { background: var(--bg); color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: var(--card); padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 span { color: var(--primary); }
        input { width: 80%; padding: 12px; border-radius: 8px; border: none; margin-bottom: 10px; background: #334155; color: white; }
        button { background: var(--primary); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .hidden { display: none; }
        video { width: 100%; border-radius: 10px; margin-top: 20px; background: #000; }
        .btn-dl { display: inline-block; margin-top: 15px; background: #3b82f6; color: white; text-decoration: none; padding: 10px 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TeraPlayer <span>Pro</span></h1>
        <p>Vercel Powered Bypass</p>
        <input type="text" id="url" placeholder="Paste TeraBox link here...">
        <br>
        <button onclick="getLink()">PLAY NOW</button>
        <div id="msg" style="margin-top:10px;"></div>
        
        <div id="result" class="hidden">
            <video id="player" controls></video>
            <br>
            <a id="dl" href="#" class="btn-dl" target="_blank">Download Video</a>
        </div>
    </div>

    <script>
        async function getLink() {
            const url = document.getElementById('url').value;
            const msg = document.getElementById('msg');
            if(!url) return alert("Link toh dalo bhai!");
            
            msg.innerHTML = "🚀 Extracting... Please wait";
            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                if(data.status === 'success') {
                    msg.innerHTML = "✅ Found: " + data.title;
                    document.getElementById('result').classList.remove('hidden');
                    document.getElementById('player').src = data.download_link;
                    document.getElementById('dl').href = data.download_link;
                } else {
                    msg.innerHTML = "❌ Error: " + data.message;
                }
            } catch(e) { msg.innerHTML = "❌ Server Error!"; }
        }
    </script>
</body>
</html>
"""

# --- YE HAI AAPKA BACKEND (LOGIC) ---

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

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36",
            "X-Requested-With": "com.dubox.drive",
            "Referer": "https://www.teraboxapp.com/"
        }

        api_url = f"https://www.teraboxapp.com/share/list?surl={surl}&dir=%2F&cnt=1000&web=1&app_id=250528"
        response = requests.get(api_url, headers=headers, timeout=15)
        res_data = response.json()

        if res_data.get('errno') == 0:
            return jsonify({
                "status": "success",
                "title": res_data['list'][0].get('server_filename'),
                "download_link": res_data['list'][0].get('dlink')
            })
        return jsonify({"status": "error", "message": "TeraBox Security Block"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel ko app object chahiye hota hai
app = app
                
