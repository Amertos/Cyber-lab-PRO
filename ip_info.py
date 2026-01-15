import requests

def get_ip_info(ip):
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if data["status"] == "fail": return {"Error": data["message"]}
        return {
            "IP": data["query"], "Location": f"{data['city']}, {data['country']}",
            "ISP": data["isp"], "Coordinates": f"{data['lat']}, {data['lon']}"
        }
    except Exception as e: return {"Error": str(e)}
