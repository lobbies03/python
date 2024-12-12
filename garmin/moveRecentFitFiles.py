import os
import shutil
from fitparse import FitFile
from datetime import datetime, timedelta


def get_fit_file_timestamp(file_path):
    """
    Extrahiert den Timestamp der FIT-Datei.
    Gibt den Timestamp als datetime-Objekt zurück, wenn vorhanden.
    """
    try:
        fitfile = FitFile(file_path)
        for message in fitfile.get_messages("session"):
            for field in message:
                if field.name == "start_time":
                    return field.value
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei {file_path}: {e}")
    return None


def move_recent_fit_files(source_dir, destination_dir, days=90):
    """
    Verschiebt FIT-Dateien, die einen Timestamp <= 90 Tage haben.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    cutoff_date = datetime.now() - timedelta(days=days)
    print(f"Schwellenwert für Timestamp: {cutoff_date}")

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".fit"):
                file_path = os.path.join(root, file)
                timestamp = get_fit_file_timestamp(file_path)
                if timestamp and timestamp >= cutoff_date:
                    print(
                        f"Verschiebe Datei: {file_path} (Timestamp: {timestamp})")
                    shutil.move(file_path, os.path.join(destination_dir, file))
                else:
                    print(
                        f"Überspringe Datei: {file_path} (Timestamp: {timestamp})")


# Quell- und Zielverzeichnisse
source_directory = "/Users/mh/Downloads/garminAllFiles/DI_CONNECT/isRunningActivity"
destination_directory = "/Users/mh/Downloads/garminAllFiles/DI_CONNECT/runningActivityLast90Days"

# Dateien verschieben
move_recent_fit_files(source_directory, destination_directory)
print("FIT-Dateien verschoben.")
