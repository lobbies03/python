#!/usr/bin/env python3
"""
FIT → CSV Exporter Komplett
Dateiname: YYYY-MM-DD_<sport>_<fitfilename>.csv
Speichert CSVs in Unterordner "csv_Files" neben den FIT-Dateien.
– Löschen vorhandener CSVs (optional)
– Summary, Laps (mit Elev Gain/Loss, Cadence), Records (mit Altitude)
– Exakte Coggan-TSS Berechnung
"""
import os
from datetime import timedelta
import pandas as pd
from fitparse import FitFile
from fitparse.utils import FitParseError

# Konfiguration
FIT_DIR = "/Users/mh/Downloads/expTpFitFiles"
FTP_BIKE = 230   # Watt
FTP_RUN = 323    # Watt
DEBUG_THRESHOLD = 100  # max Delta-Höhe (m) pro Segment, für Filter
DELETE_EXISTING_CSV = False  # Alte CSV-Dateien löschen, sonst überspringen

CSV_SUBDIR = "csv_Files"  # Unterordner für Ausgabedateien


def rolling_np(power_series, window: int = 30):
    """30-s gleitender Durchschnitt hoch 4 → 4. Wurzel (NP)."""
    r = power_series.rolling(window, min_periods=1).mean()
    return (r.pow(4).mean()) ** 0.25


def assign_records_to_laps(records, laps):
    segments = []
    for lap in laps:
        st = lap.get_value("start_time")
        en = lap.get_value("timestamp")
        segments.append([r for r in records if st <= r["ts"] <= en])
    return segments


def build_csv_path(fit_path: str, start_time, sport: str) -> str:
    """Erzeuge Ausgabepfad in csv_Files/ nach Schema YYYY-MM-DD_<sport>_<fitfilename>.csv"""
    date_str = start_time.date().isoformat() if start_time else "0000-00-00"
    sport_str = sport.lower() if sport else "unknown"
    fit_name = os.path.splitext(os.path.basename(fit_path))[0]
    csv_name = f"{date_str}_{sport_str}_{fit_name}.csv"
    # Unterordner anlegen
    parent = os.path.dirname(fit_path)
    csv_dir = os.path.join(parent, CSV_SUBDIR)
    os.makedirs(csv_dir, exist_ok=True)
    return os.path.join(csv_dir, csv_name)


def process_fit(fit_path: str) -> None:
    try:
        fit = FitFile(fit_path)
    except FitParseError as e:
        print(f"[!] FIT nicht parsebar, übersprungen: {fit_path} – {e}")
        return

    # Session-Info
    try:
        sess = next(fit.get_messages("session"), None)
    except FitParseError as e:
        print(f"[!] session übersprungen in {fit_path}: {e}")
        sess = None
    sd = {f.name: f.value for f in sess} if sess else {}
    start_time = sd.get("start_time")
    sport = str(sd.get("sport", "")).lower()

    # Ziel-CSV
    csv_path = build_csv_path(fit_path, start_time, sport)
    basename = os.path.basename(csv_path)

    if os.path.exists(csv_path):
        if DELETE_EXISTING_CSV:
            os.remove(csv_path)
            print(f"[→] gelöscht: {basename}")
        else:
            print(f"[→] übersprungen: {basename}")
            return

    # File-ID
    try:
        fid = next(fit.get_messages("file_id"), None)
    except FitParseError as e:
        print(f"[!] file_id übersprungen in {fit_path}: {e}")
        fid = None
    fd = {f.name: f.value for f in fid} if fid else {}
    product = fd.get("product_name", "unknown")

    ftp = FTP_RUN if "run" in sport else FTP_BIKE

    # Records
    recs = []
    try:
        for r in fit.get_messages("record"):
            recs.append(
                {
                    "ts": r.get_value("timestamp"),
                    "alt": r.get_value("altitude") or 0,
                    "pow": r.get_value("power") or 0,
                    "hr": r.get_value("heart_rate") or 0,
                    "cad": r.get_value("cadence") or 0,
                    "dist": (r.get_value("distance") or 0) / 1000,
                    "spd": (r.get_value("speed") or 0) * 3.6,
                }
            )
    except FitParseError as e:
        print(f"[!] record-Messages übersprungen in {fit_path}: {e}")
    recs.sort(key=lambda x: x["ts"])

    df = pd.DataFrame(recs)
    avg_pow = df["pow"].mean() if not df.empty else 0
    work_kj = df["pow"].sum() / 1000
    avg_hr = df["hr"].mean() if not df.empty else 0
    max_hr = df["hr"].max() if not df.empty else 0
    np_val = rolling_np(df["pow"]) if not df.empty else 0
    if_val = np_val / ftp if ftp else 0
    elapsed = int(sd.get("total_timer_time", 0))
    hours = elapsed / 3600
    tss = round(np_val * if_val * hours / ftp * 100) if ftp and hours else 0

    # Laps & Segmente
    try:
        laps = list(fit.get_messages("lap"))
    except FitParseError as e:
        print(f"[!] lap-Messages übersprungen in {fit_path}: {e}")
        laps = []
    segs = assign_records_to_laps(recs, laps)

    lap_rows = []
    for i, lap in enumerate(laps, 1):
        seg = segs[i - 1]
        if len(seg) > 1:
            diffs = [seg[j + 1]["alt"] - seg[j]["alt"]
                     for j in range(len(seg) - 1)]
            gain = sum(d for d in diffs if 0 < d <= DEBUG_THRESHOLD)
            loss = sum(-d for d in diffs if 0 < -d <= DEBUG_THRESHOLD)
            avg_p = sum(r["pow"] for r in seg) / len(seg)
            avg_h = sum(r["hr"] for r in seg) / len(seg)
            avg_cad = sum(r["cad"] for r in seg) / len(seg)
        else:
            gain = loss = avg_p = avg_h = avg_cad = 0
        dist_km = (lap.get_value("total_distance") or 0) / 1000
        time_s = int(lap.get_value("total_elapsed_time") or 0)
        spd_kmh = dist_km / time_s * 3600 if time_s else 0
        lap_rows.append([i, dist_km, gain, loss, time_s,
                        spd_kmh, int(avg_p), int(avg_h), int(avg_cad)])

    # CSV schreiben
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("product,start,end,TSS,NP,IF,avgP,work_kJ,maxHR,avgHR\n")
        if recs:
            fst = (recs[0]["ts"] + timedelta(hours=2)).isoformat()
            fend = (recs[-1]["ts"] + timedelta(hours=2)).isoformat()
        else:
            fst = fend = ""
        f.write(
            f"{product},{fst},{fend},{tss},{int(np_val)},{if_val:.2f},{avg_pow:.1f},{work_kj:.2f},{max_hr},{avg_hr:.1f}\n\n"
        )
        f.write("lap,dist_km,gain_m,loss_m,time_s,spd_kmh,avgP,avgHR,avgCad\n")
        for r in lap_rows:
            f.write(",".join(map(str, r)) + "\n")
        f.write("\nidx,dist_km,spd_kmh,pow,hr,alt\n")
        for j, r in enumerate(recs, 1):
            f.write(
                f"{j},{r['dist']:.2f},{r['spd']:.1f},{int(r['pow'])},{int(r['hr'])},{int(r['alt'])}\n")
    print(f"[+] {basename} erstellt")


if __name__ == "__main__":
    files = [
        os.path.join(FIT_DIR, fn)
        for fn in os.listdir(FIT_DIR)
        if os.path.isfile(os.path.join(FIT_DIR, fn)) and fn.lower().endswith(".fit")
    ]
    for p in sorted(files):
        process_fit(p)
