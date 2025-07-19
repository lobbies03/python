#!/usr/bin/env python3
import zlib
from pathlib import Path

# Pfade anpassen
allFiles  = Path('/Users/mh/Documents/Coding/python/allFiles/python')
repoFiles = Path('/Users/mh/Documents/Coding/python/myGitRepo/python')

def calc_crc(path: Path) -> int:
    """Berechnet CRC32 einer Datei."""
    return zlib.crc32(path.read_bytes()) & 0xFFFFFFFF

# CRCs für alle Dateien in allFiles (nur Top-Level)
crc_a = {
    p.name: calc_crc(p)
    for p in allFiles.iterdir()
    if p.is_file()
}

# Vergleichen: für jede Datei in allFiles alle Dateien mit gleichem Namen in repoFiles rekursiv prüfen
equal = []
for name, crc_val in crc_a.items():
    for p in repoFiles.rglob(name):
        if p.is_file() and calc_crc(p) == crc_val:
            equal.append((name, p.relative_to(repoFiles)))
            break  # erstes match reicht

# Ausgabe
print(f"Identische Dateien (CRC32) in allFiles & repoFiles ({len(equal)}):\n")
for name, repo_path in equal:
    print(f"{name}  –  repoFiles/{repo_path}")