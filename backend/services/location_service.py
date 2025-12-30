import requests

def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }
        res = requests.get(url, params=params, headers={"User-Agent": "civic-app"})
        data = res.json()
        address = data.get("address", {})
        return (
            address.get("state_district", "Unknown District"),
            address.get("state", "Unknown State")
        )
    except:
        return ("Unknown District", "Unknown State")
