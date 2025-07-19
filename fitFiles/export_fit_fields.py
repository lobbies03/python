import os
import glob
import json
import datetime
from fitparse import FitFile

# Verzeichnis mit FIT-Dateien
FIT_DIR = "/Users/mh/Downloads/expTpFitFiles/"


def get_unique_id(file_id_fields):
    """
    Bestimmt eine eindeutige ID anhand von garmin_product, product_name oder serial_number.
    """
    garmin_product = file_id_fields.get('garmin_product', {}).get('value')
    product_name = file_id_fields.get('product_name', {}).get('value')
    serial_number = file_id_fields.get('serial_number', {}).get('value')

    if garmin_product:
        unique = str(garmin_product)
    elif product_name:
        unique = str(product_name)
    elif serial_number:
        unique = str(serial_number)
    else:
        unique = "unknown"

    # Für Dateinamen unproblematisch machen
    return unique.replace(" ", "_").replace("/", "_")


def serialize_value(val):
    """
    Wandelt nicht-serialisierbare Typen (z.B. datetime, date, time, timedelta) in Strings oder primitive Datentypen um.
    """
    if isinstance(val, datetime.datetime):
        return val.isoformat()
    if isinstance(val, datetime.date):
        return val.isoformat()
    if isinstance(val, datetime.time):
        return val.isoformat()
    if isinstance(val, datetime.timedelta):
        return val.total_seconds()
    return val


def extract_all_fields(fit_path):
    """
    Extrahiert alle Nachrichten und Felder aus einer FIT-Datei.
    Rückgabe: dict mit message_type -> Liste von field-Dicts mit 'value' und 'visible'.
    """
    fitfile = FitFile(fit_path)
    data = {}

    for msg in fitfile.get_messages():
        mtype = msg.name
        if mtype not in data:
            data[mtype] = []

        fields_info = {}
        for field in msg.fields:
            raw = field.value
            val = serialize_value(raw)
            visible = raw is not None
            fields_info[field.name] = {
                'value': val,
                'visible': visible
            }

        data[mtype].append(fields_info)

    return data


def main():
    for fit_path in glob.glob(os.path.join(FIT_DIR, "*.fit")):
        # Zuerst File-ID extrahieren, um den Dateinamen zu bestimmen
        fitfile = FitFile(fit_path)
        file_id_msg = next(fitfile.get_messages('file_id'), None)
        if not file_id_msg:
            print(f"[!] Kein file_id in: {fit_path}")
            continue

        # Bereite file_id-Felder vor und hole Unique ID
        file_id_fields = {}
        for field in file_id_msg.fields:
            raw = field.value
            val = serialize_value(raw)
            file_id_fields[field.name] = {
                'value': val,
                'visible': raw is not None
            }

        unique_id = get_unique_id(file_id_fields)
        json_filename = os.path.join(FIT_DIR, f"{unique_id}.json")

        if os.path.exists(json_filename):
            print(f"[→] übersprungen: {os.path.basename(json_filename)}")
            continue

        # Jetzt alle Felder exportieren
        all_data = extract_all_fields(fit_path)

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)

        print(f"[✓] {fit_path} → {json_filename}")


if __name__ == "__main__":
    main()

