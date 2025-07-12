#!/usr/bin/env python3
# Filename: parse_all_fit_to_json.py

import os
import json
from fitparse import FitFile

BASE_DIR = '/Users/mh/Downloads/expTpFitFiles'


def fit_to_json(input_path, output_path=None):
    """
    Parse a .fit file and export all message data to a structured JSON file.
    """
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        return

    fit = FitFile(input_path)
    data = {}

    for msg in fit.get_messages():
        mtype = msg.name
        data.setdefault(mtype, [])
        record = {}
        for field in msg:
            record[field.name] = {
                'value': field.value,
                'units': field.units,
                'raw_value': field.raw_value,
                # Robust: nutze developer_data_index oder fallback auf developer_data_id
                'developer_index': getattr(field, 'developer_data_index', None)
                or getattr(field, 'developer_data_id', None)
            }
        data[mtype].append(record)

    if not output_path:
        base = os.path.splitext(input_path)[0]
        output_path = base + '.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    print(f"Exported: {output_path}")


if __name__ == '__main__':
    for fn in sorted(os.listdir(BASE_DIR)):
        if fn.lower().endswith('.fit'):
            in_path = os.path.join(BASE_DIR, fn)
            out_path = os.path.splitext(in_path)[0] + '.json'
            fit_to_json(in_path, out_path)
