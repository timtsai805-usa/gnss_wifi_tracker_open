import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Process wifi location by macs
def process_wifi_location(macs:str):

    MAP_KEY = os.getenv("MAP_KEY")
    MAP_WIFI_URL = os.getenv("MAP_WIFI_URL")

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
    url = f"{MAP_WIFI_URL}{MAP_KEY}"

    # Call google geolocation
    response = requests.post(url, json=payload, timeout=5)
    data = response.json()


    latitude = data.get("location", {}).get("lat", 0)
    longitude = data.get("location", {}).get("lng", 0)
    accuracy = data.get("accuracy", 0)

    return latitude, longitude, accuracy


# Process location address by lat, lng
def process_location_address(lat_lng:str):

    MAP_KEY = os.getenv("MAP_KEY")
    MAP_ADDR_URL = os.getenv("MAP_ADDR_URL")

    url = f"{MAP_ADDR_URL}"
    params = {
        "latlng": lat_lng,
        "key": MAP_KEY
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()
    
    if data.get("results"):
        address = data["results"][0]["formatted_address"]
    else:
        raise ValueError("No address found")
    
    return address
