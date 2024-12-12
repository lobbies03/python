from garminconnect import Garmin
from datetime import datetime, timedelta
import os

# Garmin-Login-Daten
email = "lobbies03.cheroot@icloud.com"
password = "Qefpaf-8nabhi-nunkyk"

# Anmelden bei Garmin Connect
client = Garmin(email, password)
client.login()

# Verzeichnis für den Export erstellenp
export_dir = "garmin_fit_files"
os.makedirs(export_dir, exist_ok=True)

# Zeitraum der letzten 30 Tage berechnen
end_date = datetime.now()
start_date = end_date - timedelta(days=10)

# Aktivitäten abrufen
print("Lade Aktivitäten der letzten 10 Tage herunter...")
activities = client.get_activities_by_date(
    start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

for activity in activities:
    activity_id = activity["activityId"]
    print(f"Lade Aktivität {activity_id} herunter...")

    # FIT-Datei exportieren
    try:
        fit_data = client.download_activity(activity_id, dl_fmt="original")
        fit_file_path = os.path.join(export_dir, f"{activity_id}.fit")

        # Datei speichern
        with open(fit_file_path, "wb") as fit_file:
            fit_file.write(fit_data)
        print(f"Gespeichert: {fit_file_path}")
    except Exception as e:
        print(f"Fehler beim Herunterladen von Aktivität {activity_id}: {e}")

print("Export abgeschlossen!")
