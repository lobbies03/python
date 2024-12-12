from pathlib import Path

p = Path(".")
paths = [p for p in p.iterdir() if p.is_dir()]
print(paths)