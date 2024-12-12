import os
import time
from fitparse import FitFile
from datetime import datetime


def get_fit_file_time_created(file_path):
    """
    Extrahiert das Feld 'time_created' aus einer FIT-Datei.
    Gibt den Timestamp als datetime-Objekt zurück.
    """
    try:
        fitfile = FitFile(file_path)
        for message in fitfile.get_messages("file_id"):
            for field in message:
                if field.name == "time_created":
                    return field.value
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei {file_path}: {e}")
    return None


def update_file_modified_time(file_path, new_datetime):
    """
    Ändert das Modified-Datum einer Datei auf den angegebenen Zeitpunkt.
    :param file_path: Pfad zur Datei.
    :param new_datetime: Neuer Zeitpunkt (datetime-Objekt).
    """
    try:
        new_timestamp = time.mktime(new_datetime.timetuple())
        os.utime(file_path, (new_timestamp, new_timestamp))
        print(f"Modified-Datum aktualisiert: {file_path} -> {new_datetime}")
    except Exception as e:
        print(
            f"Fehler beim Aktualisieren des Modified-Datums für {file_path}: {e}")


def process_fit_files(folder_path):
    """
    Liest das Feld 'time_created' aus FIT-Dateien im Ordner aus und setzt das Modified-Datum.
    :param folder_path: Ordnerpfad mit FIT-Dateien.
    """
    for file in os.listdir(folder_path):
        if file.endswith(".fit"):
            file_path = os.path.join(folder_path, file)
            time_created = get_fit_file_time_created(file_path)
            if time_created:
                update_file_modified_time(file_path, time_created)
            else:
                print(f"Kein gültiges 'time_created' in Datei: {file}")


# Ordner mit FIT-Dateien
folder = "/Users/mh/Downloads/garminAllFiles/DI_CONNECT/runningActivityLast90Days"

# Dateien im Ordner bearbeiten
process_fit_files(folder)
