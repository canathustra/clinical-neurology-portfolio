from pathlib import Path

path = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations\kostimulasyon\animasyon-0-akim-yayilimi.html"
)
text = path.read_text(encoding="utf-8")
old = (
    'if(d.medianActivation>0){line(ac,[[stimX,laneA+12],[stimX+18,medianY-4]],'
    '"#ff9aa2",2,[4,4]);label(ac,`median ko-stimülasyon %${d.medianActivation}`,'
    'stimX+24,medianY+7,"#ff9aa2",9)}'
)
new = (
    'if(d.medianActivation>0){line(ac,[[stimX,laneA+12],[stimX+18,medianY-4]],'
    '"#ff9aa2",2,[4,4])}'
)
if text.count(old) != 1:
    raise RuntimeError(f"Expected one overlap label block, got {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print({"costim_label_overlap_fixed": True})
