import requests
import os
import json

# Request for wifi location
def wifi_location(macs:str, MAP_KEY):

    # Split macs
    ap_list = macs.split("|")

    wifi_access_points = []

    # Get mac address and signal strength
    for ap in ap_list:
        parts = ap.split(",")
        if len(parts) >= 2:
            mac = parts[0].strip()
            signal = parts[1].strip()
        wifi_access_points.append(
            {
                "macAddress": mac,
                "signalStrength": signal
            }
        )
    
    # Combine in payload
    payload = {
        "considerIp": False,
        "wifiAccessPoints": wifi_access_points
    }

    # Define url
    url = f"{os.getenv("MAP_URL")}{MAP_KEY}"

    # Call google geolocation
    response = requests.post(url, json=payload)

    data = response.json

    latitude = data["location"]["lat"]
    longitude = data["location"]["lng"]
    accuracy = data["accuracy"]

    return latitude, longitude, accuracy