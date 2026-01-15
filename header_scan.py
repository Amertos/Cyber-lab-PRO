import requests

def scan_headers(url):
    if not url.startswith("http"): url = "https://" + url
    try:
        h = requests.get(url, timeout=5).headers
        sec = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"]
        return [{"Header": s, "Status": "✅" if s in h else "❌", "Value": h.get(s, "N/A")} for s in sec]
    except Exception as e: return [{"Error": str(e)}]
