from __future__ import annotations

import shutil
from pathlib import Path

SOURCE = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations"
)
TEMPLATES = Path(
    r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg\portable_package_files"
)
DEST = Path(
    r"C:\Users\uugur\OneDrive\Desktop"
    r"\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu"
)
ZIP_PATH = DEST.with_suffix(".zip")

if DEST.exists():
    raise RuntimeError(f"Destination already exists: {DEST}")
if ZIP_PATH.exists():
    raise RuntimeError(f"Archive already exists: {ZIP_PATH}")

shutil.copytree(SOURCE, DEST)
for template in TEMPLATES.iterdir():
    if template.is_file():
        shutil.copy2(template, DEST / template.name)

shutil.make_archive(
    str(ZIP_PATH.with_suffix("")),
    "zip",
    root_dir=DEST.parent,
    base_dir=DEST.name,
)

files = [p for p in DEST.rglob("*") if p.is_file()]
size = sum(p.stat().st_size for p in files)
print(
    {
        "folder": str(DEST),
        "zip": str(ZIP_PATH),
        "files": len(files),
        "size_mb": round(size / 1024 / 1024, 2),
    }
)
