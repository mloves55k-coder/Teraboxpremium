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
        if not url:
            return jsonify({"status": "error", "message": "No URL provided"}), 400
        
        # Extract SURL
        match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
        surl = match.group(1) if match else url.split('/')[-1]

        # Professional Headers to mimic a real user
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.terabox.com",
            "Referer": f"https://www.terabox.com/sharing/link?surl={surl}",
            "X-Requested-With": "XMLHttpRequest"
        }

        # Official App ID used by TeraBox
        api_url = f"https://www.teraboxapp.com/share/list?surl={surl}&dir=%2F&cnt=1000&order=time&desc=1&web=1&app_id=250528"
        
        response = requests.get(api_url, headers=headers, timeout=15)
        res_data = response.json()

        if res_data.get('errno') == 0:
            file_info = res_data['list'][0]
            return jsonify({
                "status": "success",
                "title": file_info.get('server_filename'),
                "download_link": file_info.get('dlink'),
                "thumbnail": file_info.get('thumbs', {}).get('url3', '')
            })
        
        # If blocked or captcha needed
        return jsonify({
            "status": "captcha",
            "verify_url": f"https://www.teraboxapp.com/sharing/link?surl={surl}"
        }), 403

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Required for Vercel
def handler(app, event, context):
    return app(event, context)
          
