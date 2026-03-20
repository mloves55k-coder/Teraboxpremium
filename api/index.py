from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        url = data.get('url', '')
        
        # SURL Extract
        match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
        surl = match.group(1) if match else url.split('/')[-1]

        # TeraBox Block Protection: Using Mobile App Logic
        api_url = f"https://www.teraboxapp.com/share/list?surl={surl}&dir=%2F&cnt=1000&order=time&desc=1&web=1&app_id=250528"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36",
            "X-Requested-With": "com.dubox.drive",
            "Referer": "https://www.teraboxapp.com/main"
        }

        response = requests.get(api_url, headers=headers, timeout=15)
        res_data = response.json()

        if res_data.get('errno') == 0:
            file_info = res_data['list'][0]
            return jsonify({
                "status": "success",
                "title": file_info.get('server_filename'),
                "download_link": file_info.get('dlink')
            })
        
        return jsonify({"status": "error", "message": "TeraBox Security Blocked This IP"}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": "Server Busy"}), 500

# Vercel requirement
def handler(app, event, context):
    return app(event, context)
    
