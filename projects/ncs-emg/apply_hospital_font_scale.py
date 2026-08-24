from __future__ import annotations

import json
import shutil
from pathlib import Path


PACKAGE = Path(r"C:\Users\uugur\OneDrive\Desktop\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu")
WORKSPACE = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg")
BACKUP = WORKSPACE / "backup_hospital_package_before_font_scale_2026-07-30"
MANIFEST = PACKAGE / "nonfizyolojik_69_sayfa_manifest.json"
SCALE = 1.15
INVERSE_PERCENT = 100 / SCALE


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = [Path(item["file"]) for item in data["sequence"]]

    if BACKUP.exists():
        raise SystemExit(f"Backup already exists: {BACKUP}")

    for relative in files:
        source = PACKAGE / relative
        destination = BACKUP / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    changed = 0
    for relative in files:
        page = PACKAGE / relative
        html = page.read_text(encoding="utf-8")
        marker = '<style id="nonphys-font-scale">'
        if marker in html:
            raise SystemExit(f"Font scale already present: {relative}")
        block = f"""<style id="nonphys-font-scale">
/* Presentation legibility: uniformly enlarge the fixed-pixel slide UI while
   preserving the full-screen 16:9 composition in Chrome and Edge. */
body > .app, body > .slide {{
  zoom: {SCALE} !important;
  width: {INVERSE_PERCENT:.8f}vw !important;
  height: {INVERSE_PERCENT:.8f}vh !important;
}}
</style>
"""
        closing_head = html.lower().find("</head>")
        if closing_head < 0:
            raise SystemExit(f"Missing </head>: {relative}")
        html = html[:closing_head] + block + html[closing_head:]
        page.write_text(html, encoding="utf-8")
        changed += 1

    print(json.dumps({
        "changed": changed,
        "scale": SCALE,
        "backup": str(BACKUP),
        "package": str(PACKAGE),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
