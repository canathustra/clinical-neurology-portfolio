from __future__ import annotations

import json
import shutil
from pathlib import Path

PACKAGE = Path(
    r"C:\Users\uugur\OneDrive\Desktop"
    r"\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu"
)
BACKUP = Path(
    r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg"
    r"\backup_hospital_package_before_fullscreen_2026-07-30"
)

manifest = json.loads(
    (PACKAGE / "nonfizyolojik_69_sayfa_manifest.json").read_text(encoding="utf-8")
)

if BACKUP.exists():
    raise RuntimeError(f"Backup already exists: {BACKUP}")

for item in manifest["sequence"]:
    source = PACKAGE / item["file"]
    destination = BACKUP / item["file"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

override = """
<style id="nonphys-fullscreen-override">
html,body{
  width:100%;
  height:100%;
  margin:0 !important;
  padding:0 !important;
  overflow:hidden !important;
}
body{
  display:block !important;
}
body > .app,
body > .slide{
  box-sizing:border-box !important;
  width:100vw !important;
  height:100vh !important;
  min-width:0 !important;
  min-height:0 !important;
  max-width:none !important;
  max-height:none !important;
  margin:0 !important;
  border:0 !important;
  border-radius:0 !important;
  box-shadow:none !important;
  aspect-ratio:auto !important;
}
</style>
"""

changed = []
for item in manifest["sequence"]:
    path = PACKAGE / item["file"]
    text = path.read_text(encoding="utf-8")
    if 'id="nonphys-fullscreen-override"' in text:
        raise RuntimeError(f"Fullscreen override already present: {item['file']}")
    if text.count("</head>") != 1:
        raise RuntimeError(f"Expected one </head>: {item['file']}")
    text = text.replace("</head>", f"{override}</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(item["file"])

print(
    json.dumps(
        {
            "package": str(PACKAGE),
            "backup": str(BACKUP),
            "pages_resized": len(changed),
        },
        ensure_ascii=False,
        indent=2,
    )
)
