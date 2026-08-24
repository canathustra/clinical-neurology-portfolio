from pathlib import Path

ROOT = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations"
)

fixes = {
    "kostimulasyon/animasyon-0-akim-yayilimi.html": [
        (
            'label(ac,"MEDİAN KOMŞU · yalnız bilek alanında ko-stimüle olabilir",w*.07,medianY-9,"#8bc6da",9.5);',
            'label(ac,"MEDİAN KOMŞU · yalnız bilek alanında ko-stimüle olabilir",w*.43,medianY+4,"#8bc6da",9.5);',
        ),
    ],
    "sweep-sensitivite/animasyon-2-sweep-hizi.html": [
        (
            'y=Math.max(35,Math.min(335,base-signal(t)*27))',
            'y=Math.max(35,Math.min(335,base-signal(t)*9.2))',
        ),
        ('<span class="chip"></span>', '<span class="chip">Kitap kaydı</span>'),
    ],
    "sweep-sensitivite/animasyon-1-sensitivite.html": [
        ('<span class="chip"></span>', '<span class="chip">Kitap kaydı</span>'),
    ],
    "elektronik-ortalama/animasyon-1-ortalama.html": [
        (
            "Kaynak: Preston &amp; Shapiro, ; Lovelace ve ark., JNNP 1973, PMID 4359163.",
            "Kaynak: Preston &amp; Shapiro, Bölüm 8.",
        ),
    ],
    "stimulus-artefakti/animasyon-0-mekanizma.html": [
        (
            "Kaynak: Preston &amp; Shapiro, ; McLean ve ark., 1996, PMID 8976313.",
            "Kaynak: Preston &amp; Shapiro, Bölüm 8.",
        ),
    ],
    "stimulus-artefakti/animasyon-2-artefakt-azaltma.html": [
        (
            "Kaynak: Preston &amp; Shapiro, Box 8.4; McLean ve ark., PMID 8976313.",
            "Kaynak: Preston &amp; Shapiro, Box 8.4.",
        ),
    ],
    "impedans-gurultu/animasyon-0-gurultu-haritasi.html": [
        (
            '"figure_label": " - sensitivite değişince görünen 60 Hz"',
            '"figure_label": "Sensitivite değişince görünen 60 Hz"',
        ),
        (
            "<br>Kaynak mekanizma: kullanıcı tarafından sağlanan ders kitabı",
            "",
        ),
    ],
}

changes = 0
for rel, replacements in fixes.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if text.count(old) != 1:
            raise RuntimeError(f"{rel}: expected one match for {old!r}, got {text.count(old)}")
        text = text.replace(old, new, 1)
        changes += 1
    path.write_text(text, encoding="utf-8")

print({"visual_and_scope_fixes": changes, "files": len(fixes)})
