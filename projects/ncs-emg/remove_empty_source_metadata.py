from pathlib import Path

root = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations\impedans-gurultu"
)
for name in ("animasyon-0-gurultu-haritasi.html", "animasyon-3-ohm-empedans.html"):
    path = root / name
    text = path.read_text(encoding="utf-8")
    old = ', "pubmed": ""'
    if text.count(old) != 1:
        raise RuntimeError(f"{name}: expected one empty source metadata field")
    path.write_text(text.replace(old, "", 1), encoding="utf-8")
print({"empty_external_source_metadata_removed": 2})
