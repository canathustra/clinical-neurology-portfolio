from pathlib import Path

ROOT = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations"
)

fixes = {
    "elektronik-ortalama/animasyon-1-ortalama.html": [
        ("N = 10 · </button>", "N = 10 · kitap örneği</button>"),
    ],
    "kostimulasyon/animasyon-0-akim-yayilimi.html": [
        ('id="highBtn">87 mA · </button>', 'id="highBtn">87 mA · ko-stimülasyon</button>'),
    ],
    "stimulus-artefakti/animasyon-3-kablo-induksiyonu.html": [
        ("<div><b></b>Aynı biyolojik yanıt;", "<div><b>Kitap mekanizması</b>Aynı biyolojik yanıt;"),
    ],
    "impedans-gurultu/animasyon-3-ohm-empedans.html": [
        ("<b> - diferansiyel amplifikasyon ve empedans uyumsuzluğu</b>", "<b>Diferansiyel amplifikasyon ve empedans uyumsuzluğu</b>"),
        ('"figure_label": " - diferansiyel amplifikasyon ve empedans uyumsuzluğu"', '"figure_label": "Diferansiyel amplifikasyon ve empedans uyumsuzluğu"'),
    ],
    "impedans-gurultu/animasyon-0-gurultu-haritasi.html": [
        ("<b> - sensitivite değişince görünen 60 Hz</b>", "<b>Sensitivite değişince görünen 60 Hz</b>"),
    ],
    "aktif-referans-mesafesi/animasyon-1-g1-g2-mesafesi.html": [
        ('alt=": G1-G2', 'alt="G1-G2'),
    ],
    "elektrot-sinir-mesafesi/animasyon-0-derinlik-filtresi.html": [
        ('alt=": median', 'alt="Median'),
    ],
    "elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html": [
        ('alt=": yüzey', 'alt="Yüzey'),
    ],
    "elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html": [
        ('alt=": elektrotlar', 'alt="Elektrotlar'),
    ],
    "elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html": [
        ('alt=": sinir', 'alt="Sinir'),
    ],
    "sweep-sensitivite/animasyon-1-sensitivite.html": [
        ('alt=": aynı', 'alt="Aynı'),
    ],
    "sweep-sensitivite/animasyon-2-sweep-hizi.html": [
        ('alt=": aynı', 'alt="Aynı'),
    ],
}

count = 0
for rel, replacements in fixes.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if text.count(old) != 1:
            raise RuntimeError(f"{rel}: expected exactly one match for {old!r}")
        text = text.replace(old, new, 1)
        count += 1
    path.write_text(text, encoding="utf-8")

print({"labels_polished": count, "files": len(fixes)})
