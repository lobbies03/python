#!/usr/bin/env python3
import os
import json
import csv
from fitparse import FitFile
from zoneinfo import ZoneInfo

# Konfiguration
DIR_PATH = '/Users/mh/Downloads/expTpFitFiles'
FIELDS_DIR = os.path.join(DIR_PATH, 'field_lists')  # JSON-Felddefinitionen
UTC = ZoneInfo('UTC')
LOCAL = ZoneInfo('Europe/Berlin')

# Lädt JSON-Felddefinitionen und filtert Felder mit show=1


def load_fields_def(product):
    safe = product.replace(' ', '_').replace('/', '_')
    path = os.path.join(FIELDS_DIR, f"{safe}_fields.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Keine Felddefinition für Produkt: {product}")
    with open(path, 'r', encoding='utf-8') as jf:
        return json.load(jf)


if __name__ == '__main__':
    for fname in sorted(f for f in os.listdir(DIR_PATH) if f.lower().endswith('.fit')):
        fit_path = os.path.join(DIR_PATH, fname)
        fit = FitFile(fit_path)

        # Produktname aus file_id
        product = 'unknown'
        for msg in fit.get_messages('file_id'):
            for f in msg:
                if f.name == 'product_name' and f.value:
                    product = str(f.value)
                    break
            if product != 'unknown':
                break
        safe_prod = product.replace(' ', '_').replace('/', '_')

        # JSON-Felder laden
        try:
            fields_def = load_fields_def(product)
        except FileNotFoundError as e:
            print(e)
            continue

        # Session-Felder mit show=1
        session_defs = fields_def.get('session', [])
        session_fields = [item['name']
                          for item in session_defs if item.get('show', 1) == 1]
        # Lap-Felder mit show=1
        lap_defs = fields_def.get('lap', [])
        lap_fields = [item['name']
                      for item in lap_defs if item.get('show', 1) == 1]
        # Record-Felder mit show=1
        record_defs = fields_def.get('record', [])
        record_fields = [item['name']
                         for item in record_defs if item.get('show', 1) == 1]

        if not session_fields or not lap_fields:
            print(
                f"Keine definierten Felder zum Export für Produkt: {product}")
            continue

        # Session-Daten auslesen (erste Session)
        session_data = {}
        for session in fit.get_messages('session'):
            for f in session:
                session_data[f.name] = f.value
            break

        # Startzeit konvertieren
        start_time = session_data.get('start_time')
        if not start_time:
            print(f"Keine start_time in Session von {fname}")
            continue
        start_local = start_time.replace(tzinfo=UTC).astimezone(LOCAL)
        ts = start_local.strftime('%Y-%m-%d_%H-%M-%S')

        # Sport für Dateiname
        sport = session_data.get('sport', 'unknown')
        sport_str = str(sport).replace(' ', '_')

        # CSV-Dateiname
        stem = os.path.splitext(fname)[0]
        csv_name = f"{stem}_{ts}_{sport_str}_{safe_prod}.csv"
        out_path = os.path.join(DIR_PATH, csv_name)
        if os.path.exists(out_path):
            print(f"Übersprungen (existiert): {csv_name}")
            continue

        # Laps sammeln
        laps = list(fit.get_messages('lap'))
        if not laps:
            print(f"Keine Laps in {fname}")
            continue

        # CSV schreiben
        with open(out_path, 'w', newline='') as fcsv:
            writer = csv.writer(fcsv, delimiter=';')
            # 1. Zeile: Session-Felder
            writer.writerow(session_fields)
            # 2. Zeile: Werte oder N/A
            writer.writerow([session_data.get(f, 'N/A')
                            for f in session_fields])
            # 3. Leerzeile
            writer.writerow([])
            # 4. Zeile: Lap-Felder
            writer.writerow(lap_fields)
            # 5+: Lap-Werte
            for lap in laps:
                lap_data = {f.name: f.value for f in lap}
                writer.writerow([lap_data.get(f, 'N/A') for f in lap_fields])
            # Leerzeile nach Laps
            writer.writerow([])
            # Message-Header und Werte
            message_defs = fields_def.get('message', [])
            message_fields = [item['name']
                              for item in message_defs if item.get('show', 1) == 1]
            if message_fields:
                writer.writerow(message_fields)
                for m in fit.get_messages('message'):
                    msg_data = {f.name: f.value for f in m}
                    writer.writerow([msg_data.get(f, 'N/A')
                                    for f in message_fields])
            # Record-Header und Werte und Werte
            if record_fields:
                writer.writerow(record_fields)
                for rec in fit.get_messages('record'):
                    rec_data = {f.name: f.value for f in rec}
                    writer.writerow([rec_data.get(f, 'N/A')
                                    for f in record_fields])

        print(f"Exportiert: {csv_name}")
