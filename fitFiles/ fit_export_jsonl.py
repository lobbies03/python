 #!/usr/bin/env python3
"""
FIT → JSON Lines Exporter (stabilisiert)
– Exportiert Session-, Lap- und Record-Daten in je eine JSONL-Datei
– Stellt sicher, dass fehlende Felder wie "altitude" mit Default-Werten belegt werden
"""
import os
import glob
import json
from datetime import timedelta
from fitparse import FitFile

# Konfiguration
FIT_DIR = "/Users/mh/Downloads/expTpFitFiles"
OUTPUT_DIR = FIT_DIR       # JSONL-Dateien landen hier
DELETE_EXISTING = True     # Alte JSONLs löschen

# FTP-Werte (für spätere TSS-Berechnung, optional)
FTP_BIKE = 230
FTP_RUN = 323


def parse_fit(path):
    fit = FitFile(path)
    # --- Session-Daten
    sess_msg = next(fit.get_messages('session'), None)
    session = {}
    if sess_msg:
        for f in sess_msg:
            session[f.name] = f.value
    session['file_name'] = os.path.basename(path)

    # --- Record-Stream
    records = []
    for msg in fit.get_messages('record'):
        rec = {
            'timestamp': msg.get_value('timestamp'),
            'distance': msg.get_value('distance') or 0,
            'speed': msg.get_value('speed') or 0,
            'power': msg.get_value('power') or 0,
            'heart_rate': msg.get_value('heart_rate') or 0,
            'cadence': msg.get_value('cadence') or 0,
            'altitude': msg.get_value('altitude') or 0
        }
        records.append(rec)
    # sort by timestamp
    records.sort(key=lambda r: r['timestamp'] or 0)

    # --- Lap-Daten
    laps = []
    # Für Elevation Gain/Loss muss records bereits sortiert sein
    for lap_msg in fit.get_messages('lap'):
        lap = {f.name: lap_msg.get_value(f.name) for f in lap_msg}
        start = lap_msg.get_value('start_time')
        end = lap_msg.get_value('timestamp')
        segment = [r for r in records if r['timestamp']
                   and start <= r['timestamp'] <= end]
        # Höhen-Deltas
        gain = loss = 0
        if len(segment) > 1:
            diffs = [segment[i+1]['altitude'] - segment[i]['altitude']
                     for i in range(len(segment)-1)]
            gain = sum(d for d in diffs if d > 0)
            loss = sum(-d for d in diffs if d < 0)
        lap['elev_gain_m'] = gain
        lap['elev_loss_m'] = loss
        # Durchschnittliche Cadence
        cads = [r['cadence'] for r in segment]
        lap['avg_cadence_rpm'] = sum(cads)/len(cads) if cads else 0
        laps.append(lap)

    return session, laps, records


def write_jsonl(data, path):
    mode = 'w' if DELETE_EXISTING else 'a'
    with open(path, mode, encoding='utf-8') as f:
        for obj in data:
            f.write(json.dumps(obj, default=str) + '\n')


def main():
    paths = {
        'session': os.path.join(OUTPUT_DIR, 'session.jsonl'),
        'laps':    os.path.join(OUTPUT_DIR, 'laps.jsonl'),
        'records': os.path.join(OUTPUT_DIR, 'records.jsonl')
    }
    # Lösche bestehende Dateien
    if DELETE_EXISTING:
        for p in paths.values():
            if os.path.exists(p):
                os.remove(p)

    # Verarbeite alle FITs
    for fit_path in sorted(glob.glob(os.path.join(FIT_DIR, '*.fit'))):
        session, laps, records = parse_fit(fit_path)
        write_jsonl([session], paths['session'])
        write_jsonl(laps,     paths['laps'])
        write_jsonl(records,  paths['records'])
        print(f"[+] verarbeitet: {os.path.basename(fit_path)}")


if __name__ == '__main__':
    main()
