from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


LIVE = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations"
)
BACKUP = Path(
    r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg"
    r"\backup_before_book_audit_2026-07-30"
)


def read(rel: str) -> str:
    return (LIVE / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    (LIVE / rel).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.I | re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text


manifest = json.loads(
    (LIVE / "nonfizyolojik_69_sayfa_manifest.json").read_text(encoding="utf-8")
)

if not BACKUP.exists():
    for item in manifest["sequence"]:
        src = LIVE / item["file"]
        dst = BACKUP / item["file"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    for rel in ("index.html", "nonfizyolojik_69_sayfa_manifest.json"):
        dst = BACKUP / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(LIVE / rel, dst)


# 1) Electronic averaging: the displayed response must be exactly flat until
# the marked physiologic onset.
rel = "elektronik-ortalama/animasyon-1-ortalama.html"
s = read(rel)
s = replace_once(
    s,
    "function dsap(t){return AMP*(.92*gauss(t,PEAK,.22)-.62*gauss(t,4.02,.31)+.16*gauss(t,4.72,.55))}",
    """function dsap(t){
  if(t<=ONSET)return 0;
  const gate=1-Math.exp(-Math.pow((t-ONSET)/.045,2));
  return AMP*gate*(.92*gauss(t,PEAK,.22)-.62*gauss(t,4.02,.31)+.16*gauss(t,4.72,.55));
}""",
    "averaging causal onset",
)
write(rel, s)


# 2) Limb-position morphology: the onset cursor now marks the first departure
# from baseline, not the early tail of an ungated Gaussian.
rel = "ekstremite-morfoloji/animasyon-1-pozisyon-tutarliligi.html"
s = read(rel)
s = replace_once(
    s,
    """function cmap(t,p){
  const q=t-p.lat;
  const bifid=p.shoulder;
  return p.amp*(.68*gauss(q,.48,.27)+bifid*gauss(q,1.10,.36)-.34*gauss(q,1.82,.46)+.16*gauss(q,2.75,.62)-.055*gauss(q,4.1,.8));
}""",
    """function cmap(t,p){
  if(t<=p.lat)return 0;
  const q=t-p.lat,bifid=p.shoulder;
  const gate=1-Math.exp(-Math.pow(q/.075,2));
  return p.amp*gate*(.68*gauss(q,.48,.27)+bifid*gauss(q,1.10,.36)-.34*gauss(q,1.82,.46)+.16*gauss(q,2.75,.62)-.055*gauss(q,4.1,.8));
}""",
    "position morphology causal onset",
)
s = replace_once(
    s,
    "teachingModel:true,playing};",
    'teachingModel:true,causalOnset:true,stimulationsAreSeparate:true,playing};',
    "position state",
)
write(rel, s)


# 3) Sensitivity and sweep speed must use the same stored physiologic CMAP.
# The signal is gated at 2.9 ms and has its negative peak at 4.7 ms, matching
# the values shown alongside the book figure.
canonical_signal = """function signal(t){
  const g=(m,s)=>Math.exp(-.5*Math.pow((t-m)/s,2));
  const stimulus=.22*Math.exp(-.5*Math.pow((t-.16)/.018,2))-.13*Math.exp(-.5*Math.pow((t-.21)/.028,2));
  if(t<=2.90)return stimulus;
  const gate=1-Math.exp(-Math.pow((t-2.90)/.055,2));
  const foot=.060*g(3.08,.12);
  const main=7.8*g(4.70,.63);
  const after=-5.2*g(6.28,.78);
  const late=.62*g(8.35,.96);
  const noise=.010*Math.sin(t*17.3)+.006*Math.sin(t*37.7);
  return stimulus+gate*(foot+main+after+late)+noise;
}"""

rel = "sweep-sensitivite/animasyon-1-sensitivite.html"
s = read(rel)
s = regex_once(
    s,
    r"function signal\(t\)\{.*?\n\}",
    canonical_signal,
    "sensitivity canonical signal",
)
s = replace_once(
    s,
    "responseUnchanged:true,playing};",
    "responseUnchanged:true,causalOnset:true,playing};",
    "sensitivity state",
)
write(rel, s)

rel = "sweep-sensitivite/animasyon-2-sweep-hizi.html"
s = read(rel)
s = regex_once(
    s,
    r"function signal\(t\)\{.*?\}",
    canonical_signal,
    "sweep canonical signal",
)
s = replace_once(
    s,
    "responseUnchanged:true,playing};",
    "responseUnchanged:true,causalOnset:true,playing};",
    "sweep state",
)
write(rel, s)


# 4) Co-stimulation: wrist and below-elbow are two separate acquisitions.
# Two independent lanes prevent a pulse from appearing to travel from one
# stimulation site through the other before reaching FDI.
rel = "kostimulasyon/animasyon-0-akim-yayilimi.html"
s = read(rel)
start = s.index("function drawAnatomy(now){")
end = s.index("function drawScope(now){", start)
new_anatomy = """function drawAnatomy(now){
  const {w,h}=fit(anatomy,anatomyWrap);ac.clearRect(0,0,w,h);ac.fillStyle="#101d24";ac.fillRect(0,0,w,h);
  const d=DATA[level],stimX=w*.24,targetX=w*.88,laneA=h*.34,laneB=h*.73,medianY=h*.535;
  label(ac,"A · BİLEK UYARIMI → FDI KAYDI",w*.07,laneA-22,"#e0bd78",11);
  label(ac,"B · DİRSEK-ALTI UYARIMI → AYNI FDI KAYDI",w*.07,laneB-22,"#9cc9ff",11);
  line(ac,[[w*.07,laneA],[w*.93,laneA]],"#b58b43",7);
  line(ac,[[w*.07,laneB],[w*.93,laneB]],"#b58b43",7);
  line(ac,[[w*.07,medianY],[w*.42,medianY]],"#476979",5);
  label(ac,"MEDİAN KOMŞU · yalnız bilek alanında ko-stimüle olabilir",w*.07,medianY-9,"#8bc6da",9.5);
  ac.save();ac.beginPath();ac.arc(stimX,laneA,d.field,0,Math.PI*2);
  ac.fillStyle=level==="high"?"rgba(235,90,101,.20)":level==="risk"?"rgba(255,200,87,.16)":"rgba(94,234,141,.13)";
  ac.fill();ac.strokeStyle=level==="high"?"#eb5a65":level==="risk"?"#ffc857":"#5eea8d";ac.lineWidth=2;ac.stroke();ac.restore();
  dot(ac,stimX,laneA,10,"#111820","#ffc857");label(ac,`BİLEK · ${d.current} mA`,stimX,laneA+25,"#ffc857",10,"center");
  dot(ac,stimX,laneB,9,"#111820","#64a7ff");label(ac,"DİRSEK ALTI · 37 mA",stimX,laneB+25,"#8fc2ff",10,"center");
  for(const [lane,color] of [[laneA,"#5eea8d"],[laneB,"#36c9d7"]]){
    dot(ac,targetX,lane,8,color);label(ac,"FDI · G1",targetX,lane-15,color,10,"center");
    line(ac,[[stimX+17,lane-10],[targetX-20,lane-10]],color,2,[6,4]);
    ac.fillStyle=color;ac.beginPath();ac.moveTo(targetX-20,lane-15);ac.lineTo(targetX-10,lane-10);ac.lineTo(targetX-20,lane-5);ac.closePath();ac.fill();
  }
  if(d.medianActivation>0){line(ac,[[stimX,laneA+12],[stimX+18,medianY-4]],"#ff9aa2",2,[4,4]);label(ac,`median ko-stimülasyon %${d.medianActivation}`,stimX+24,medianY+7,"#ff9aa2",9)}
  if(stimStart>=0){
    const e=(now-stimStart)/1000;
    if(e<.42){const a=1-e/.42;for(const lane of [laneA,laneB]){ac.beginPath();ac.arc(stimX,lane,17+25*(1-a),0,Math.PI*2);ac.strokeStyle=`rgba(255,200,87,${a})`;ac.lineWidth=4;ac.stroke()}}
    if(e>2.0)stimStart=-1;
  }
}
"""
s = s[:start] + new_anatomy + s[end:]
s = s.replace(">Uyarıları göster<", ">İki ayrı uyarımı göster<")
s = replace_once(
    s,
    'propagationDirection:"distal_to_FDI_only"',
    'propagationDirection:"two_independent_stimulations_to_FDI"',
    "costim propagation state",
)
s = replace_once(
    s,
    '<div class="caveat"><b>Sınır:</b> “50 mA” evrensel eşik değildir; anatomi, stimülatör konumu, pulse süresi ve impedansa bağlıdır. Ani morfoloji değişimi + komşu twitch/kanal yanıtı daha değerlidir.</div>',
    '<div class="caveat"><b>Kitap ölçütü:</b> Normal bireylerde 0,2 ms uyarıyla 50 mA üzeri akımlar komşu sinir ko-stimülasyonu olasılığını belirgin artırır.</div>',
    "costim caveat",
)
write(rel, s)


# 5) Remove literature digressions and rewrite them as concise Chapter 8
# takeaways. This keeps the animation pages at book scope.
book_note_replacements = {
    "motor-elektrot-yerlesimi/animasyon-1-g1-konumu.html": (
        r'<div class="warning"><b>Resident notu:</b>.*?</div>',
        '<div class="warning"><b>Kitap kuralı:</b> İlk pozitif sapma görülürse G1 motor nokta dışında kabul edilir; pozitiflik kaybolana kadar G1 yeniden konumlandırılır.</div>',
    ),
    "motor-elektrot-yerlesimi/animasyon-2-g2-tendon-potansiyeli.html": (
        r'<div class="warning"><b>Resident notu:</b>.*?</div>',
        '<div class="warning"><b>Kitap kuralı:</b> Ulnar ve tibial çalışmalarda tendon G2 elektriksel olarak aktif olabilir. Sağ–sol ve seri kayıtlarda G2 aynı anatomik yere konmalıdır.</div>',
    ),
    "antidromik-ortodromik/animasyon-1-antidromik-vs-ortodromik.html": (
        r'<div class="warning"><b>Resident notu:</b>.*?</div>',
        '<div class="warning"><b>Kitap sonucu:</b> Aynı sinir segmenti ve mesafede latans ile iletim hızı aynıdır; antidromik amplitüd çoğunlukla daha yüksektir.</div>',
    ),
    "antidromik-ortodromik/animasyon-2-sahte-dsap.html": (
        r'<div class="warning"><b>Resident notu:</b>.*?</div>',
        '<div class="warning"><b>Kitap uyarısı:</b> Erken ve keskin yanıt DSAP’tır. DSAP yoksa daha geç ve geniş hacim-iletilen motor bileşen duysal yanıt sanılmamalıdır.</div>',
    ),
    "elektrot-sinir-mesafesi/animasyon-0-derinlik-filtresi.html": (
        r'<p class="source-note"><b>Resident notu:</b>.*?</p>',
        '<p class="source-note"><b>Kitap kuralı:</b> Akım ve mesafe sabitken elektrot çifti medial–laterale taşınır; en yüksek amplitüd sinire en yakın kayıt yerini gösterir.</p>',
    ),
    "elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html": (
        r'<p class="source-note"><b>Resident notu:</b>.*?</p>',
        '<p class="source-note"><b>Kitap sonucu:</b> Artan doku mesafesi amplitüdü azaltır, süreyi uzatır, onseti hafif kısaltabilir ve peak latansını hafif uzatabilir.</p>',
    ),
    "elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html": (
        r'<p class="source-note"><b>Resident notu:</b>.*?</p>',
        '<p class="source-note"><b>Kitap kaydı:</b> Sinir üzerinde 38 µV; 0,5 cm lateralde 31 µV; 1 cm lateralde 12 µV. Akım ve kayıt mesafesi değişmez.</p>',
    ),
    "elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html": (
        r'<p class="source-note"><b>Resident notu:</b>.*?</p>',
        '<p class="source-note"><b>Kitap sonucu:</b> Elektrot sinirden uzaklaştıkça onset sola kayabilir; aynı mesafeyle hesaplanan iletim hızı yalancı yüksek görünür.</p>',
    ),
    "aktif-referans-mesafesi/animasyon-1-g1-g2-mesafesi.html": (
        r'<p class="source-note"><b>Resident notu:</b>.*?</p>',
        '<p class="source-note"><b>Kitap kaydı:</b> G1–G2 aralığı 1,0 / 2,5 / 4,0 cm olduğunda amplitüd 14 / 25 / 28 µV’tur; önerilen aralık 3–4 cm’dir.</p>',
    ),
}

for rel, (pattern, replacement) in book_note_replacements.items():
    s = regex_once(read(rel), pattern, replacement, f"book note {rel}")
    write(rel, s)


# Exact book wording for the two supramaximal animation notes.
rel = "supramaksimal/animasyon-0-akson-rekrutmani.html"
s = read(rel)
s = replace_once(
    s,
    '<div class="caveat">Amplitüd platosu tüm motor aksonların rekrüte edildiğini gösterir. Onsetin hafif kısalması yeni motor ünite katkısından ayrı olarak uyarımın etkinleşme fiziğini de yansıtabilir.</div>',
    '<div class="caveat">Kitap sonucu: akım arttıkça amplitüd yükselir ve latans kısalır; amplitüd platosu ek %25 akımla değişmiyorsa supramaksimal uyarım doğrulanır.</div>',
    "supramax recruitment caveat",
)
write(rel, s)

rel = "supramaksimal/animasyon-1-uyari-egrisi.html"
s = read(rel)
s = replace_once(
    s,
    '<div class="caveat">Ek pay tek bir biyolojik sabit değildir: AANEM terminolojisi yaklaşık %20; klinik yöntemler yaklaşık %20–33 kullanabilir. Bu animasyon  11→14 mA örneğini izler.</div>',
    '<div class="caveat">Kitap protokolü: amplitüd artık artmadığında akımı yaklaşık %25 yükselt; amplitüd yine değişmiyorsa supramaksimal uyarımı doğrula.</div>',
    "supramax protocol caveat",
)
write(rel, s)


# Co-stimulation diagnostic note: only the checks explicitly emphasized in
# Chapter 8 are retained.
rel = "kostimulasyon/animasyon-1-tanisal-hatalar.html"
s = read(rel)
s = replace_once(
    s,
    '<div class="warning"><b>Güvenlik kontrolü:</b> Blok kararı yalnız amplitüd oranına dayanmaz. Supramaksimal uyarım, morfoloji/alan/süre, komşu kas aktivasyonu ve anatomik varyantlar birlikte denetlenir.</div>',
    '<div class="warning"><b>Kitap kontrolü:</b> Blok örüntüsünde distal ko-stimülasyonu düşün; dalga biçimini, kas twitchini ve eşzamanlı komşu kas kaydını kontrol et.</div>',
    "costim diagnostic note",
)
write(rel, s)


# Remove all external-literature links from the non-physiologic sequence.
# The visible teaching statements now come only from the local Chapter 8 text.
for item in manifest["sequence"]:
    rel = item["file"]
    s = read(rel)
    s = re.sub(
        r"<br\s*/?>\s*<a\b[^>]*https?://[^>]*>.*?</a>",
        "",
        s,
        flags=re.I | re.S,
    )
    s = re.sub(
        r"<a\b[^>]*https?://[^>]*>.*?</a>",
        "",
        s,
        flags=re.I | re.S,
    )
    write(rel, s)

# Remove the now-unused machine-readable PubMed URL from the impedance page as
# well; it is not visible after the source-link cleanup but is still outside
# the requested Chapter 8 scope.
rel = "impedans-gurultu/animasyon-3-ohm-empedans.html"
s = read(rel)
s = replace_once(
    s,
    '"pubmed": "https://pubmed.ncbi.nlm.nih.gov/31654663/"',
    '"pubmed": ""',
    "impedance metadata source removal",
)
write(rel, s)


# Repair labels left visually empty after the earlier request to remove figure
# numbers. These are text-only edits and do not touch working mechanisms.
label_fixes = {
    "aktif-referans-mesafesi/animasyon-1-g1-g2-mesafesi.html": [
        ("<div><b></b> · Aynı depolarize segment", "<div>Aynı depolarize segment")
    ],
    "antidromik-ortodromik/animasyon-1-antidromik-vs-ortodromik.html": [
        ("<div><b></b> · Aynı median sinir", "<div>Aynı median sinir")
    ],
    "antidromik-ortodromik/animasyon-2-sahte-dsap.html": [
        ("<div><b></b> · Median bilek", "<div>Median bilek")
    ],
    "elektrot-sinir-mesafesi/animasyon-0-derinlik-filtresi.html": [
        ("<span><b></b> · Median", "<span>Median")
    ],
    "elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html": [
        ("<span><b></b> · Alt", "<span>Alt")
    ],
    "elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html": [
        ("<div><b></b> · Median", "<div>Median")
    ],
    "elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html": [
        ("<div><b></b> · Aynı median", "<div>Aynı median")
    ],
    "kostimulasyon/animasyon-1-tanisal-hatalar.html": [
        ("<div><b></b> · Aynı teknik", "<div>Aynı teknik")
    ],
    "motor-elektrot-yerlesimi/animasyon-1-g1-konumu.html": [
        ("<div><b></b> · Sinir", "<div>Sinir")
    ],
    "motor-elektrot-yerlesimi/animasyon-2-g2-tendon-potansiyeli.html": [
        ("<div><b></b> · Ulnar", "<div>Ulnar"),
        ("<span> · G1 + (−G2)</span>", "<span>Kitap mekanizması · G1 + (−G2)</span>"),
        ("<span> · 8,3 / 7,2 / 5,6 mV</span>", "<span>Kitap kayıtları · 8,3 / 7,2 / 5,6 mV</span>"),
    ],
    "stimulus-artefakti/animasyon-1-anot-rotasyon.html": [
        ('<div class="booktag"> · yüzeyel', '<div class="booktag">Kitap örneği · yüzeyel')
    ],
    "katot-polarite/animasyon-0-depolarizasyon-anodal-blok.html": [
        ("<b> · kitap sırası</b>", "<b>Kitap mekanizması</b>")
    ],
    "katot-polarite/animasyon-1-polarite-tersligi.html": [
        ("<b> · median duysal</b>", "<b>Kitap kaydı · median duysal</b>")
    ],
    "supramaksimal/animasyon-0-akson-rekrutmani.html": [
        ("<span> · amplitüd ve onsetin gerçek basamakları</span>", "<span>Kitap kaydı · amplitüd ve latans basamakları</span>"),
        ("<b> · gerçek değerler</b>", "<b>Kitap kaydı</b>"),
    ],
    "supramaksimal/animasyon-1-uyari-egrisi.html": [
        ("<b> · kitap protokolü</b>", "<b>Kitap protokolü</b>")
    ],
    "supramaksimal/animasyon-2-amplitud-farki.html": [
        ("<b> · ulnar motor</b>", "<b>Kitap kaydı · ulnar motor</b>")
    ],
    "kostimulasyon/animasyon-0-akim-yayilimi.html": [
        ("<b> · gerçek kayıt</b>", "<b>Kitap kaydı · ulnar motor</b>")
    ],
    "ekstremite-mesafe/animasyon-1-dirsek-pozisyonu.html": [
        ('<span class="chip"> · 9 → 10 cm</span>', '<span class="chip">9 → 10 cm</span>')
    ],
}

for rel, fixes in label_fixes.items():
    s = read(rel)
    for old, new in fixes:
        s = replace_once(s, old, new, f"label fix {rel}: {old}")
    write(rel, s)


# No external source links should remain in the section.
remaining_urls = []
for item in manifest["sequence"]:
    s = read(item["file"])
    if re.search(r"https?://", s):
        remaining_urls.append(item["file"])

if remaining_urls:
    raise RuntimeError(f"External URLs remain: {remaining_urls}")

print(
    json.dumps(
        {
            "backup": str(BACKUP),
            "causal_onset_fixes": 4,
            "costimulation_geometry_fixed": True,
            "book_scope_notes_rewritten": len(book_note_replacements) + 4,
            "empty_labels_repaired": sum(len(v) for v in label_fixes.values()),
            "external_urls_remaining": 0,
        },
        ensure_ascii=False,
        indent=2,
    )
)
