import os


def replace_filename_part(folder_path, old_part, new_part):
    """
    Ersetzt einen Teil des Dateinamens in allen Dateien eines Ordners.

    :param folder_path: Pfad zum Ordner, in dem die Dateien bearbeitet werden.
    :param old_part: Der Teil des Dateinamens, der ersetzt werden soll.
    :param new_part: Der neue Teil, der anstelle des alten eingefügt wird.
    """
    # Überprüfen, ob der Ordner existiert
    if not os.path.exists(folder_path):
        print(f"Ordner existiert nicht: {folder_path}")
        return

    # Iteriere durch alle Dateien im Ordner
    for filename in os.listdir(folder_path):
        # Prüfen, ob der alte Teil im Dateinamen vorhanden ist
        if old_part in filename:
            old_file_path = os.path.join(folder_path, filename)
            new_filename = filename.replace(old_part, new_part)
            new_file_path = os.path.join(folder_path, new_filename)

            # Datei umbenennen
            os.rename(old_file_path, new_file_path)
            print(f"Umbenannt: {filename} -> {new_filename}")


# Beispielaufruf
folder = "/Users/mh/Downloads/garminAllFiles/DI_CONNECT/DI-Connect-Uploaded-Files/UploadedFiles_0-_Part3"
replace_filename_part(folder, "lobbies03.cheroot@icloud.com_", "")
