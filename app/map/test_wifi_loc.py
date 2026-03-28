import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

MAP_KEY = os.getenv("MAP_KEY")
if not MAP_KEY:
    raise ValueError("MAP_KEY is not found")

url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={MAP_KEY}"

payload = {
    "considerIp": False,
    "wifiAccessPoints": [
        {
            "macAddress": "e0:d3:62:6d:d7:13",
            "signalStrength": -38
        },
        {
            "macAddress": "fc:77:7b:91:01:0a",
            "signalStrength": -62
        },
        {
            "macAddress": "b4:f2:67:3d:73:40",
            "signalStrength": -65
        }
    ]
}

response = requests.post(url, json=payload)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))