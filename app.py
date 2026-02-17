from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PW Render API Running ✅"

@app.route("/pw")
def pw():
    target_url = request.args.get("url")
    token = request.args.get("token")  # optional (future use)

    if not target_url:
        return "URL missing", 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    try:
        r = requests.get(target_url, headers=headers, stream=True, timeout=15)

        def generate():
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        return Response(
            generate(),
            content_type=r.headers.get("Content-Type", "application/octet-stream"),
            headers={
                "Content-Disposition": "inline"
            }
        )

    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}", 500


if __name__ != "__main__":
    # For gunicorn
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Local testing
    app.run(host="0.0.0.0", port=10000)
