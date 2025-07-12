#!/usr/bin/env python3
import os
import csv
from fitparse import FitFile
from datetime import datetime
from zoneinfo import ZoneInfo

# Pfade
DIR = '/Users/mh/Downloads/fitFiles'
OUT_SUMMARY = os.path.join(DIR, 'workout_summary.csv')
OUT_LAPS = os.path.join(DIR, 'laps.csv')
OUT_RECORDS = os.path.join(DIR, 'records.csv')

# Zeitzonen
UTC = ZoneInfo('UTC')
LOCAL = ZoneInfo('Europe/Berlin')

# Kopfdaten für CSV-Dateien
SUMMARY_FIELDS = [
    'start_time', 'sport', 'total_timer_time_s', 'total_distance_m', 'work_kJ',
    'avg_power_W', 'normalized_power_W', 'IF', 'TSS', 'avg_hr_bpm', 'max_hr_bpm',
    'elevation_gain_m', 'num_laps'
]
LAP_FIELDS = [
    'lap_index', 'start_time', 'lap_duration_s', 'lap_distance_m',
    'avg_power_W', 'max_power_W', 'normalized_power_W', 'work_kJ',
    'avg_hr_bpm', 'max_hr_bpm', 'avg_cadence_rpm', 'avg_speed_ms', 'IF', 'lap_TSS',
    'lactate_mmol', 'avg_grade_%',
    'avg_pace_s_km', 'Effort_Pace_s_km', 'avg_run_power_W',
    'vertical_osc_mm', 'stance_time_ms', 'step_length_m',
    'stroke_type', 'stroke_rate_spm', 'swolf', 'pace_100m_s'
]
RECORD_FIELDS = [
    'timestamp', 'lap_index', 'distance_m', 'elapsed_time_s',
    'Powermeter_Power_W', 'Trainer_Power_W', 'run_power_W', 'heart_rate_bpm',
    'cadence_rpm', 'speed_ms', 'altitude_m', 'grade_%', 'position_lat', 'position_long',
    'Effort_Pace_s_km', 'Form_Power_W', 'vertical_osc_mm', 'stance_time_ms', 'lactate_mmol'
]

# Helper: schreibe Header falls Datei nicht existiert


def ensure_header(path, fields):
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(fields)


# Setup CSVs
ensure_header(OUT_SUMMARY, SUMMARY_FIELDS)
ensure_header(OUT_LAPS, LAP_FIELDS)
ensure_header(OUT_RECORDS, RECORD_FIELDS)

# Verarbeite FIT-Dateien
for fname in sorted(f for f in os.listdir(DIR) if f.lower().endswith('.fit')):
    fit = FitFile(os.path.join(DIR, fname))
    # Session erste
    session = next(fit.get_messages('session'), None)
    if not session:
        continue
    sdata = {f.name: f.value for f in session}
    # Zeit
    st = sdata.get('start_time')
    st_loc = st.replace(tzinfo=UTC).astimezone(LOCAL)
    start_iso = st_loc.strftime('%Y-%m-%dT%H:%M:%SZ')
    sport = sdata.get('sport', '')
    # Werte summary
    summary_row = [
        start_iso,
        sport,
        sdata.get('total_timer_time', 'N/A'),
        sdata.get('total_distance', 'N/A'),
        round(sdata.get('total_calories', 0) / 1000, 3),
        sdata.get('avg_power', 'N/A'),
        sdata.get('normalized_power', 'N/A'),
        sdata.get('intensity_factor', 'N/A'),
        sdata.get('training_stress_score', 'N/A'),
        sdata.get('avg_heart_rate', 'N/A'),
        sdata.get('max_heart_rate', 'N/A'),
        sdata.get('total_ascent', 'N/A'),
        sdata.get('num_laps', 'N/A')
    ]
    with open(OUT_SUMMARY, 'a', newline='') as f:
        csv.writer(f, delimiter=';').writerow(summary_row)

    # Laps
    for lap in fit.get_messages('lap'):
        l = {f.name: f.value for f in lap}
        row = [
            l.get('message_index', 'N/A'),
            l.get('start_time', 'N/A'),
            l.get('total_timer_time', 'N/A'),
            l.get('total_distance', 'N/A'),
            l.get('avg_power', 'N/A'),
            l.get('max_power', 'N/A'),
            l.get('normalized_power', 'N/A'),
            round(l.get('total_calories', 0) / 1000, 3),
            l.get('avg_heart_rate', 'N/A'),
            l.get('max_heart_rate', 'N/A'),
            l.get('avg_running_cadence', 'N/A'),
            l.get('avg_speed', 'N/A'),
            l.get('intensity_factor', 'N/A'),
            l.get('lap_trigger', 'N/A'),  # placeholder for lap_TSS
            l.get('avg_stance_time_percent', 'N/A'),
            l.get('avg_grade', 'N/A'),
            l.get('avg_pace', 'N/A'),
            l.get('developer_Effort Pace', 'N/A'),
            l.get('avg_power', 'N/A'),
            l.get('avg_vertical_oscillation', 'N/A'),
            l.get('avg_stance_time', 'N/A'),
            l.get('avg_step_length', 'N/A'),
            l.get('stroke_type', 'N/A'),
            l.get('avg_running_cadence', 'N/A'),
            l.get('swolf', 'N/A'),
            l.get('timestamp', 'N/A')
        ]
        with open(OUT_LAPS, 'a', newline='') as f:
            csv.writer(f, delimiter=';').writerow(row)

    # Records
    for rec in fit.get_messages('record'):
        r = {f.name: f.value for f in rec}
        row = [r.get(f, '') for f in RECORD_FIELDS]
        with open(OUT_RECORDS, 'a', newline='') as f:
            csv.writer(f, delimiter=';').writerow(row)
