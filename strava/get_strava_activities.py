import requests


def refresh_access_token():
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": "140610",
        "client_secret": "a329b59bd7b634db79be5c012094094eb87ccab2",
        "grant_type": "refresh_token",
        "refresh_token": "393c47541c73acfffdf3ff369b52cda0db9cd968"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        tokens = response.json()
        return tokens["access_token"]  # Neuer Access Token
    else:
        print("Fehler beim Erneuern des Access Tokens:", response.status_code)
        return None


ACCESS_TOKEN = refresh_access_token()
print("Access-Token: ", ACCESS_TOKEN)
quit

# Strava-API-Zugangsdaten
API_URL = "https://www.strava.com/api/v3/athlete/activities"

# Strava-Aktivitäten abrufen


def get_strava_activities():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Rückgabe der Aktivitäten als JSON
    else:
        print("Fehler beim Abrufen der Daten:", response.status_code)
        return None


# Abrufen und Anzeigen der Aktivitäten
activities = get_strava_activities()
if activities:
    for activity in activities:
        print(
            f"Aktivität: {activity['name']}, Distanz: {activity['distance']} Meter")
