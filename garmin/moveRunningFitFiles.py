import os
import shutil
from fitparse import FitFile


def is_running_activity(file_path):
    """
    Prüft, ob eine FIT-Datei eine Running-Aktivität enthält.
    """
    try:
        fitfile = FitFile(file_path)
        for message in fitfile.get_messages("sport"):
            for field in message:
                if field.name == "sport" and field.value == "running":
                    return True
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei {file_path}: {e}")
    return False


def move_running_files(source_dir, destination_dir):
    """
    Findet Running-Files in einem Quellverzeichnis und verschiebt sie in das Zielverzeichnis.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".fit"):
                file_path = os.path.join(root, file)
                if is_running_activity(file_path):
                    print(f"Running-Datei gefunden: {file_path}")
                    shutil.move(file_path, os.path.join(destination_dir, file))
                else:
                    print(f"Keine Running-Datei: {file_path}")


# Quell- und Zielverzeichnisse
source_directory = "/Users/mh/Downloads/garminAllFiles/DI_CONNECT/DI-Connect-Uploaded-Files"
destination_directory = "/Users/mh/Downloads/garminAllFiles/DI_CONNECT/isRunningActivity"

# Dateien verschieben
move_running_files(source_directory, destination_directory)
print("Lauf-Dateien wurden verschoben.")
