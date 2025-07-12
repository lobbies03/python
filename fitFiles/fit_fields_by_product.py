#!/usr/bin/env python3
# Filename: fit_fields_by_product.py
import os
import json
from fitparse import FitFile

# Basis-Ordner und Ausgabeordner
dir_path = '/Users/mh/Downloads/expTpFitFiles'
fields_dir = os.path.join(dir_path, 'field_lists')
if not os.path.exists(fields_dir):
    os.makedirs(fields_dir)

# Mapping: Produkt -> message_type -> Liste von Feldern in Reihenfolge ihres ersten Auftretens
fields_by_product = {}

# Alle FIT-Dateien durchlaufen (case-insensitive .fit)
for fname in sorted(os.listdir(dir_path)):
    if not fname.lower().endswith('.fit'):
        continue
    fit_path = os.path.join(dir_path, fname)
    fit = FitFile(fit_path)

    # Hersteller bestimmen
    manufacturer = None
    for msg in fit.get_messages('file_id'):
        for f in msg:
            if f.name == 'manufacturer' and f.value:
                manufacturer = str(f.value).lower()
                break
        if manufacturer:
            break

    # Produkt-Key je Hersteller
    product = 'unknown'
    for msg in fit.get_messages('file_id'):
        for f in msg:
            if manufacturer == '1' and f.name == 'garmin_product' and f.value:
                product = str(f.value).replace(' ', '_')
                break
            elif manufacturer in ('294', '355') and f.name == 'product_name' and f.value:
                product = str(f.value).replace(' ', '_')
                break
        if product != 'unknown':
            break

    # Initialisiere Struktur für Produkt
    prod_map = fields_by_product.setdefault(product, {})

    # Nachrichten in der Reihenfolge ihres Auftretens durchgehen
    for msg in fit.get_messages():
        mtype = msg.name
        field_list = prod_map.setdefault(mtype, [])
        for f in msg:
            if f.name not in field_list:
                field_list.append(f.name)

# JSON-Dateien schreiben mit Anzeige-Flag show=1
for product, types in fields_by_product.items():
    safe = product.replace(' ', '_').replace('/', '_')
    out_data = {mtype: [{'name': name, 'show': 1} for name in fields]
                for mtype, fields in types.items()}
    out_path = os.path.join(fields_dir, f"{safe}_fields.json")
    with open(out_path, 'w', encoding='utf-8') as jf:
        json.dump(out_data, jf, ensure_ascii=False, indent=2)
    print(f"Geschrieben: {out_path}")
