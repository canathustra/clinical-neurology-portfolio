from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations"
)
MANIFEST = ROOT / "nonfizyolojik_69_sayfa_manifest.json"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
rows = []
for item in manifest["sequence"]:
    rel = item["file"]
    text = (ROOT / rel).read_text(encoding="utf-8")
    lower = text.lower()
    flags = []
    if re.search(r"(?<![a-zçğıöşü])şekil(?=\s|\d|[.:])", lower) or re.search(
        r"\bfig(?:ure)?\.?\s*\d", lower
    ):
        flags.append("figure-reference")
    if any(
        marker in lower
        for marker in (
            "pmid",
            "pmcid",
            "pubmed",
            "jnnp",
            "aanem",
            "2018 uzun torasik",
            "ve ark.",
        )
    ):
        flags.append("external-literature")
    if "http://" in lower or "https://" in lower:
        flags.append("external-url")
    if re.search(
        r'<(?:span|div)[^>]*class="[^"]*\b(?:chip|booktag)\b[^"]*"[^>]*>'
        r"\s*</(?:span|div)>",
        text,
        re.I,
    ):
        flags.append("empty-visible-label")
    if "<b></b>" in text or re.search(r"<button[^>]*>[^<]*·\s*</button>", text, re.I):
        flags.append("broken-label")
    if flags:
        rows.append({"number": item["number"], "file": rel, "flags": flags})

print(
    json.dumps(
        {
            "pages": len(manifest["sequence"]),
            "flagged_pages": len(rows),
            "rows": rows,
        },
        ensure_ascii=False,
        indent=2,
    )
)
