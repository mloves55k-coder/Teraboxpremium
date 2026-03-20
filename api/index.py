from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

# ❌ YAHAN PELE @app.route('/') THA, USE DELETE KAR DEIN

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
        return jsonify({"status": "error", "message": "Bypass failed"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
        
