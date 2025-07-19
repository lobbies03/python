#!/usr/bin/env python3
import os
import glob
import pandas as pd
from fitparse import FitFile
from datetime import timedelta

# Pfad zu deinen FIT-Files
FIT_DIR = "/Users/mh/Downloads/expTpFitFiles"

# Threshold-Power-Konstanten
FTP_BIKE = 230  # W
FTP_RUN = 323  # W
# Threshold-Herzfrequenz
HR_THRESH_BIKE = 164  # bpm
HR_THRESH_RUN = 174  # bpm

for fit_path in glob.glob(os.path.join(FIT_DIR, "*.fit")):
    csv_path = os.path.splitext(fit_path)[0] + ".csv"
    # nur erstellen, wenn noch nicht vorhanden
    if os.path.exists(csv_path):
        print(f"[→] übersprungen (existiert): {os.path.basename(csv_path)}")
        continue

    fit = FitFile(fit_path)

    # Produktname aus file_id
    fid = next(fit.get_messages("file_id"), None)
    fd = {m.name: m.value for m in fid} if fid else {}
    product_name = fd.get("product_name", "")

    # alle record-Daten sammeln
    recs = []
    for r in fit.get_messages("record"):
        ts = r.get_value("timestamp")
        recs.append({
            "ts":   ts,
            "dist": (r.get_value("distance") or 0) / 1000.0,
            "spd":  (r.get_value("speed") or 0) * 3.6,
            "pow":  r.get_value("power") or 0,
            "hr":   r.get_value("heart_rate") or 0,
            "alt":  r.get_value("altitude") or 0,
        })
    recs.sort(key=lambda x: x["ts"])

    # START & END aus record-Timestamps (+2h verschoben)
    if recs:
        rec_start = recs[0]["ts"] + timedelta(hours=2)
        rec_end = recs[-1]["ts"] + timedelta(hours=2)
        start_iso = rec_start.isoformat()
        end_iso = rec_end.isoformat()
    else:
        start_iso = end_iso = ""

    # Session-Felder für Sportart & elapsed time
    sess = next(fit.get_messages("session"), None)
    sd = {m.name: m.value for m in sess} if sess else {}
    sport = sd.get("sport", "").lower()
    elapsed_sec = int(sd.get("total_timer_time", 0) or 0)

    # FTP und HR-Threshold nach Sportart wählen
    if 'run' in sport:
        ftp = FTP_RUN
        hr_thresh = HR_THRESH_RUN
    else:
        ftp = FTP_BIKE
        hr_thresh = HR_THRESH_BIKE

    # Create DataFrame for record stream
    df_recs = pd.DataFrame(recs) if recs else pd.DataFrame(
        columns=["pow", "hr"])

    # Durchschnittliche Power & HR aus Records
    avg_power = df_recs["pow"].mean() if not df_recs.empty else 0.0
    work_kJ = df_recs["pow"].sum() / 1000  # W·s to kJ
    max_hr = df_recs["hr"].max() if not df_recs.empty else 0
    avg_hr = df_recs["hr"].mean() if not df_recs.empty else 0.0

    # NP, IF & PW:HR (%) anhand HR-Threshold
    if not df_recs.empty:
        rolling = df_recs["pow"].rolling(window=30, min_periods=1).mean()
        np_val = (rolling.pow(4).mean()) ** 0.25
        if_val = np_val / ftp if ftp else 0.0
        pw_hr = round(avg_hr / hr_thresh * 100, 2) if hr_thresh else 0.0
    else:
        np_val = if_val = pw_hr = 0.0

    # TSS aus NP & IF
    tss_calc = (elapsed_sec * np_val * if_val) / \
        (ftp * 3600) * 100 if ftp and elapsed_sec else 0
    tss = round(tss_calc)

    # Lap-Block
    lap_rows = []
    lap_no = 1
    for lap in fit.get_messages("lap"):
        st = lap.get_value("start_time")
        en = lap.get_value("timestamp")
        d = lap.get_value("total_distance") or 0
        t = int(lap.get_value("total_elapsed_time") or 0)
        seg = [r for r in recs if st <= r["ts"] <= en]
        if seg:
            avg_p = sum(r["pow"] for r in seg) / len(seg)
            avg_hr_l = sum(r["hr"] for r in seg) / len(seg)
            asc = sum(max(0, seg[i+1]["alt"] - seg[i]["alt"])
                      for i in range(len(seg)-1))
        else:
            avg_p = avg_hr_l = asc = 0
        lap_rows.append([
            lap_no,
            f"{d/1000:.2f}",
            int(asc),
            t,
            f"{(d/t*3.6) if t else 0:.1f}",
            int(avg_p),
            int(avg_hr_l),
        ])
        lap_no += 1

    # Record-Block
    rec_rows = []
    rec_start_ts = recs[0]["ts"] if recs else None
    for idx, r in enumerate(recs, start=1):
        secs = int((r["ts"] - rec_start_ts).total_seconds()
                   ) if rec_start_ts else 0
        rec_rows.append([
            idx,
            f"{r['dist']:.2f}",
            f"{r['spd']:.1f}",
            int(r["pow"]),
            int(r["hr"]),
        ])

    # CSV schreiben inklusive erweiterter Summary
    with open(csv_path, "w") as f:
        f.write(
            "PRODUCT_NAME,START,END,TSS,NP_W,IF,PW_HR,AVG_POWER_W,WORK_kJ,MAX_HR,AVG_HR\n")
        f.write(f"{product_name},{start_iso},{end_iso},{tss},{int(np_val)},{if_val:.2f},{pw_hr},{avg_power:.1f},{work_kJ:.2f},{max_hr},{avg_hr:.1f}\n\n")
        f.write(
            "lap_index,distance_km,elev_m,time_s,speed_kmh,avg_power_W,avg_hr_bpm\n")
        for row in lap_rows:
            f.write(",".join(map(str, row)) + "\n")
        f.write("\n")
        f.write("rec_index,distance_km,speed_kmh,avg_power_W,heart_rate_bpm\n")
        for row in rec_rows:
            f.write(",".join(map(str, row)) + "\n")

    print(f"[+] erstellt: {os.path.basename(csv_path)}")
