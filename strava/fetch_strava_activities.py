import requests
import csv
import time
import os

# Strava API-Konstanten
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")  # Initialer Platzhalter
TOKEN_EXPIRATION = 0  # Zeitpunkt, wann der Token abläuft (Unix-Zeitstempel)


def get_access_token():
    global ACCESS_TOKEN, TOKEN_EXPIRATION, REFRESH_TOKEN

    # Überprüfen, ob der Access Token abgelaufen ist
    if time.time() >= TOKEN_EXPIRATION:
        print("Access Token ist abgelaufen, hole neuen Token...")
        token_url = "https://www.strava.com/oauth/token"
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            data = response.json()
            ACCESS_TOKEN = data["access_token"]
            # Aktualisierter Refresh Token
            REFRESH_TOKEN = data["refresh_token"]
            # Token-Ablaufzeit (Unix-Zeit)
            TOKEN_EXPIRATION = data["expires_at"]
            print("Neuer Access Token erfolgreich abgerufen.")
        else:
            raise Exception(
                f"Fehler beim Abrufen des Access Tokens: {response.status_code} {response.text}")
    else:
        print("Access Token ist noch gültig.")

    return ACCESS_TOKEN


def fetch_activities():
    global ACCESS_TOKEN
    ACCESS_TOKEN = get_access_token()  # Hole den aktuellen Access Token

    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        activities = response.json()

        # Speichern in einer CSV-Datei
        with open("strava_activities.csv", "w", newline="") as csvfile:
            fieldnames = [
                "name", "distance", "moving_time", "elapsed_time",
                "total_elevation_gain", "average_speed", "max_speed",
                "type", "start_date", "start_date_local", "timezone",
                "start_latlng", "end_latlng", "achievement_count",
                "kudos_count", "comment_count", "athlete_count",
                "average_cadence", "average_watts", "weighted_average_watts",
                "kilojoules", "device_name", "calories", "has_heartrate",
                "average_heartrate", "max_heartrate", "suffer_score"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for activity in activities:
                writer.writerow({
                    "name": activity.get("name"),
                    "distance": activity.get("distance"),
                    "moving_time": activity.get("moving_time"),
                    "elapsed_time": activity.get("elapsed_time"),
                    "total_elevation_gain": activity.get("total_elevation_gain"),
                    "average_speed": activity.get("average_speed"),
                    "max_speed": activity.get("max_speed"),
                    "type": activity.get("type"),
                    "start_date": activity.get("start_date"),
                    "start_date_local": activity.get("start_date_local"),
                    "timezone": activity.get("timezone"),
                    "start_latlng": activity.get("start_latlng"),
                    "end_latlng": activity.get("end_latlng"),
                    "achievement_count": activity.get("achievement_count"),
                    "kudos_count": activity.get("kudos_count"),
                    "comment_count": activity.get("comment_count"),
                    "athlete_count": activity.get("athlete_count"),
                    "average_cadence": activity.get("average_cadence"),
                    "average_watts": activity.get("average_watts"),
                    "weighted_average_watts": activity.get("weighted_average_watts"),
                    "kilojoules": activity.get("kilojoules"),
                    "device_name": activity.get("device_name"),
                    "calories": activity.get("calories"),
                    "has_heartrate": activity.get("has_heartrate"),
                    "average_heartrate": activity.get("average_heartrate"),
                    "max_heartrate": activity.get("max_heartrate"),
                    "suffer_score": activity.get("suffer_score")
                })

        print("Daten erfolgreich exportiert.")
    else:
        raise Exception(
            f"Fehler beim Abrufen der Aktivitäten: {response.status_code} {response.text}")


# Skript ausführen
if __name__ == "__main__":
    fetch_activities()
