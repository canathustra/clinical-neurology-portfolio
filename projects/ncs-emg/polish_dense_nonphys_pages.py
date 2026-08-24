from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations"
)
BACKUP = Path(
    r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg"
    r"\backup_before_portable_polish_2026-07-30"
)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


manifest = json.loads(
    (ROOT / "nonfizyolojik_69_sayfa_manifest.json").read_text(encoding="utf-8")
)
if BACKUP.exists():
    raise RuntimeError(f"Backup already exists: {BACKUP}")

for item in manifest["sequence"]:
    src = ROOT / item["file"]
    dst = BACKUP / item["file"]
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
for rel in ("index.html", "nonfizyolojik_69_sayfa_manifest.json"):
    dst = BACKUP / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / rel, dst)


replacements: dict[str, list[tuple[str, str]]] = {
    "kostimulasyon/onleme-yontemleri.html": [
        (
            "Akım yavaşça artırılır — ilk küçük <b>submaksimal</b> yanıt alınana kadar.",
            "Akımı, ilk küçük <b>submaksimal</b> yanıt görülene dek yavaş artır.",
        ),
        (
            "Akım <b>sabit tutulup</b>, stimülatör hafifçe <b>medial/lateral</b> kaydırılır.",
            "Akımı <b>sabit tut</b>; stimülatörü hafifçe <b>mediale ve laterale</b> kaydır.",
        ),
        (
            "En yüksek amplitüdü veren konum, sinire <b>en yakın</b> konumdur — sonra akım supramaksimale çıkarılır.",
            "En yüksek amplitüdlü konum sinire <b>en yakındır</b>; burada akımı supramaksimale çıkar.",
        ),
        (
            "Bu teknik, gereken akımı <b>şaşırtıcı derecede azaltır</b>.",
            "Doğru konum, supramaksimal yanıt için gereken akımı <b>belirgin azaltır</b>.",
        ),
        (
            "Dalga formu <b>aniden değişebilir</b> (örn. median'ın kubbe şekli, ulnar katılınca <b>bifid</b> olur).",
            "Dalga biçimindeki <b>ani değişim</b> ko-stimülasyonu gösterir: median kubbe, ulnar katılınca <b>bifid</b> olabilir.",
        ),
        (
            "Kas seğirmesi değişir: median → tenar + ilk 2 lumbrikal; ulnar → <b>yaygın el fleksiyonu</b>.",
            "Twitch: median → tenar + ilk 2 lumbrikal; ulnar → <b>yaygın el fleksiyonu</b>.",
        ),
        (
            "Popliteal fossada: peroneal → dorsifleksiyon/eversiyon; tibial → <b>plantar fleksiyon/inversiyon</b>.",
            "Popliteal fossa: peroneal → dorsifleksiyon/eversiyon; tibial → <b>plantar fleksiyon/inversiyon</b>.",
        ),
        (
            'Normal bireylerde ko-stimülasyon genellikle <span class="num">&gt;50 mA</span> (<span class="num">0.2 ms</span> süre) civarında başlar.',
            'Normal bireylerde 0,2 ms uyarıyla ko-stimülasyon çoğunlukla <span class="num">&gt;50 mA</span> düzeyinde başlar.',
        ),
        (
            "Bu eşiğin üzerinde, ko-stimülasyon olasılığına karşı <b>daha dikkatli</b> olunmalı.",
            "Bu düzeyin üzerinde <b>ko-stimülasyon olasılığını</b> özellikle denetle.",
        ),
    ],
    "ekstremite-morfoloji/index.html": [
        (
            "Birden fazla noktanın uyarıldığı bir çalışmada (genelde <b>motor</b> çalışmalar) ekstremite, <b>tüm uyarım noktaları boyunca aynı pozisyonda</b> kalmalıdır.",
            "Birden fazla uyarım noktasında—özellikle <b>motor</b> çalışmada—ekstremite <b>tüm kayıt boyunca aynı pozisyonda</b> tutulur.",
        ),
        (
            "Pozisyon uyarımlar arasında değişirse, hafifçe <b>farklı yanıtlar</b> elde edilebilir.",
            "Uyarımlar arasında pozisyon değişirse yanıtlar hafifçe <b>farklılaşabilir</b>.",
        ),
        (
            "Pozisyon değişince cilt (ve üzerindeki elektrotlar), altındaki kas veya sinire göre <b>hafifçe kayabilir</b>.",
            "Pozisyon değişince cilt ve elektrotlar, alttaki kas veya sinire göre <b>kayabilir</b>.",
        ),
        (
            "Karın-tendon montajında tendonun elektriksel olarak <b>sessiz</b> olduğu varsayılır — ama <b>ulnar ve tibial</b> sinirde bu doğru değildir (bkz. G2 Yerleşimi).",
            "Belly–tendon montajı tendonu <b>sessiz</b> varsayar; <b>ulnar ve tibial</b> sinirde G2 elektriksel olarak aktif olabilir.",
        ),
        (
            'Bu "tendon potansiyeli", uzak alandan hacim iletilen bir sinyaldir ve ekstremite pozisyonu değiştikçe <b>şekli ve latansı değişebilir</b>.',
            'Hacim iletilen bu “tendon potansiyelinin” <b>şekli ve latansı</b> ekstremite pozisyonuyla değişebilir.',
        ),
        (
            "<b>Senaryo 1:</b> Ulnar motor çalışma — bilek, dirsek-altı, dirsek-üstü hepsi kol <b>aynı (bükülü) pozisyondayken</b> uyarılır.",
            "<b>Senaryo 1:</b> Bilek, dirsek-altı ve dirsek-üstü; kol <b>her kayıtta bükülü</b>.",
        ),
        (
            "<b>Senaryo 2:</b> Bilek kol <b>düzken</b> uyarılır; sonra dirsek <b>bükülüp</b> dirsek-altı ve dirsek-üstü uyarılır.",
            "<b>Senaryo 2:</b> Bilek kol <b>düzken</b>; dirsek-altı ve dirsek-üstü kol <b>bükülüyken</b> uyarılır.",
        ),
        (
            "Senaryo 2'de, özellikle <b>dirsek-altı ve dirsek-üstünde</b>, hafifçe farklı amplitüd ve İH elde edilir.",
            "Senaryo 2, özellikle <b>dirsek-altı/üstü amplitüdünü ve İH’yi</b> hafifçe değiştirir.",
        ),
    ],
    "ekstremite-mesafe/animasyon-2-kaliper.html": [
        (
            '<span id="sourceFigureNo">Şekil 10.17A</span>',
            '<span id="sourceFigureNo">Erb–aksilla segmenti</span>',
        ),
        ('figureNo:"Şekil 10.17A"', 'figureNo:"Erb–aksilla segmenti"'),
        ('figureNo:"Şekil 10.13D"', 'figureNo:"Radyal sinir–spiral oluk"'),
        (
            'caption:"<b>Kitap bağlantısı:</b> Median ve ulnar sinirlerin aksilla–Erb noktası arasındaki yüzey mesafesi çoğu kez gerçek sinir uzunluğunu doğru yansıtmaz."',
            'caption:"<b>Kitap kuralı:</b> Aksilla–Erb yüzey mesafesi gerçek sinir uzunluğunu güvenilir biçimde yansıtmayabilir."',
        ),
        (
            'evidence:"<b>Klinik dayanak:</b> Proksimal çalışmaların mesafeleri kaliperle ölçülür; 2018 uzun torasik sinir yöntem çalışması da aksiller–supraklaviküler mesafeyi kaliperle ölçmüştür."',
            'evidence:"<b>Kitap sonucu:</b> Obstetrik kaliper, yüzey mezurasına göre gerçek sinir uzunluğunu daha doğru yaklaştırır."',
        ),
        (
            'caption:"<b>Kitap bağlantısı:</b> Proksimal radyal motor çalışmalarda yüzey mesafeleri güvenilmez olabilir; spiral oluk altı ve üstü mesafeleri kaliperle ölçülür."',
            'caption:"<b>Kitap kuralı:</b> Humerus çevresinde spiralleşen radyal sinirde yüzey mesafesi güvenilir olmayabilir."',
        ),
        (
            'evidence:"<b>Uzmanlık düzeyi nüans:</b> Radyal aksilla–dirsek çalışmasında yöntemler eşdeğer değildir. Kaliper yüzey hatasını azaltabilir; segment protokolü ve laboratuvar normali yine korunmalıdır."',
            'evidence:"<b>Kitap sonucu:</b> Spiral oluk altı–üstü gibi eğrisel segmentlerde mesafeyi kaliperle yaklaşıkla."',
        ),
    ],
}

edits = 0
for rel, pairs in replacements.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        text = replace_once(text, old, new, f"{rel}: {old[:45]}")
        edits += 1
    path.write_text(text, encoding="utf-8")

print(
    json.dumps(
        {
            "backup": str(BACKUP),
            "pages_polished": len(replacements),
            "exact_edits": edits,
        },
        ensure_ascii=False,
        indent=2,
    )
)
