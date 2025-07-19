#!/usr/bin/env python3

import os
import csv
import glob
from datetime import datetime, date, time, timedelta
from pathlib import Path
from fitparse import FitFile
from fitparse.utils import FitParseError

# ── Konfiguration ───────────────────────────────────────────────────────────
FIT_DIR = Path("/Users/mh/Downloads/expTpFitFiles")
CSV_DIR = FIT_DIR / "csv_Files"
OVERWRITE = True
# ---------------------------------------------------------------------------

CSV_DIR.mkdir(exist_ok=True)


def as_str(val):
    if val is None:
        return ""
    if isinstance(val, (datetime, date, time, timedelta)):
        return val.isoformat()
    return str(val)


def safe_iter(fit, mtype):
    it = fit.get_messages(mtype)
    while True:
        try:
            yield next(it)
        except StopIteration:
            break
        except FitParseError as e:
            print(f"[!] {mtype}-Message übersprungen: {e}")
            continue


def export_one(path: Path):
    try:
        fit = FitFile(str(path))
    except FitParseError as e:
        print(f"[!] Parse-Fehler, Datei übersprungen: {path.name} – {e}")
        return

    # --- Startzeit + Sport für Dateinamen ----------------------------------
    sess = next(safe_iter(fit, "session"), None)
    start_time = sess.get_value("start_time") if sess else None
    sport = (sess.get_value("sport") if sess else "unknown") or "unknown"
    # +2 Stunden korrigieren
    if isinstance(start_time, datetime):
        start_time = start_time + timedelta(hours=2)
    date_str = start_time.date().isoformat() if isinstance(
        start_time, datetime) else "0000-00-00"

    fit_base = path.stem                     # ohne .fit
    csv_name = f"{date_str}_{sport}_{fit_base}.csv"
    csv_path = CSV_DIR / csv_name

    if csv_path.exists() and not OVERWRITE:
        print(f"[→] übersprungen: {csv_name}")
        return
    if csv_path.exists():
        csv_path.unlink()
        print(f"[→] gelöscht: {csv_name}")

    # Session-, Lap-, Record-Iteratoren noch einmal (neues FitFile ist ok)
    # neu öffnen, da vorherige Iteratoren verbraucht sind
    fit = FitFile(str(path))

    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)

        # Session
        for i, msg in enumerate(safe_iter(fit, "session")):
            if i == 0:
                w.writerow([fld.name for fld in msg.fields])
            w.writerow([as_str(msg.get_value(fld.name)) for fld in msg.fields])

        # Laps
        for i, msg in enumerate(safe_iter(fit, "lap")):
            if i == 0:
                w.writerow([fld.name for fld in msg.fields])
            w.writerow([as_str(msg.get_value(fld.name)) for fld in msg.fields])

        # Records
        for i, msg in enumerate(safe_iter(fit, "record")):
            if i == 0:
                w.writerow([fld.name for fld in msg.fields])
            w.writerow([as_str(msg.get_value(fld.name)) for fld in msg.fields])

    print(f"[+] CSV erstellt: {csv_name}")


if __name__ == "__main__":
    for fit_file in sorted(FIT_DIR.glob("*.fit")):
        export_one(fit_file)
