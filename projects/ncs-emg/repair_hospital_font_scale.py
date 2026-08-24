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

    repaired = 0
    for relative in files:
        source = BACKUP / relative
        page = PACKAGE / relative
        if not source.exists():
            raise SystemExit(f"Missing backup file: {relative}")
        shutil.copy2(source, page)
        html = page.read_text(encoding="utf-8")
        closing_head = html.rfind("</head>")
        if closing_head < 0:
            raise SystemExit(f"Missing exact </head>: {relative}")
        html = html[:closing_head] + block + html[closing_head:]
        page.write_text(html, encoding="utf-8")
        repaired += 1

    malformed = []
    for relative in files:
        html = (PACKAGE / relative).read_text(encoding="utf-8")
        if html.count('<style id="nonphys-font-scale">') != 1 or "<</" in html or "<</head>" in html:
            malformed.append(str(relative))
    if malformed:
        raise SystemExit(f"Malformed pages after repair: {malformed}")

    print(json.dumps({
        "repaired": repaired,
        "scale": SCALE,
        "malformed": malformed,
        "package": str(PACKAGE),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
