import json
import re
from pathlib import Path
from urllib.parse import unquote

root = Path(r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\10_Projects\presentations\artifacts_of_ncs_emg\animations")
manifest = json.loads((root / "nonfizyolojik_69_sayfa_manifest.json").read_text(encoding="utf-8"))
chain = [row["file"] for row in manifest["sequence"]]
previous_before_section = "proksimal-distal/animasyon-1-segment-hizi.html"
errors = []


def nav_href(text: str, key: str):
    for match in re.finditer(
        r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        text,
        flags=re.I | re.S,
    ):
        visible_label = re.sub(r"<[^>]+>", " ", match.group(2))
        visible_label = re.sub(r"\s+", " ", visible_label).strip()
        if re.search(rf"\b{re.escape(key)}\b", visible_label, flags=re.I):
            return match.group(1)
    return None


for i, rel in enumerate(chain):
    path = root / rel
    text = path.read_text(encoding="utf-8")
    expected_prev = previous_before_section if i == 0 else chain[i - 1]
    expected_next = "index.html" if i == len(chain) - 1 else chain[i + 1]
    for key, expected in (("F1", expected_prev), ("F3", expected_next)):
        href = nav_href(text, key)
        if href is None:
            errors.append({"file": rel, "key": key, "problem": "missing"})
            continue
        actual = (path.parent / unquote(href.split("#", 1)[0])).resolve()
        wanted = (root / expected).resolve()
        if actual != wanted:
            errors.append(
                {"file": rel, "key": key, "href": href, "expected": expected}
            )

predecessor = root / previous_before_section
pred_f3 = nav_href(predecessor.read_text(encoding="utf-8"), "F3")
if pred_f3 is None or (predecessor.parent / pred_f3).resolve() != (root / chain[0]).resolve():
    errors.append({"file": previous_before_section, "key": "F3", "href": pred_f3, "expected": chain[0]})

report = {"links_checked": len(chain) * 2 + 1, "errors": errors}
(root / "nonfizyolojik_gezinme_qa.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
if errors:
    raise SystemExit(1)
