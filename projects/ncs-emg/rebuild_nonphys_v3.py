from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\10_Projects\presentations\artifacts_of_ncs_emg"
)
LIVE = ROOT / "animations"
BACKUP = ROOT / "animations_ncs_emg_codex_backup_20260729_before_nonphys_rebuild"
V2_BACKUP = ROOT / "animations_ncs_emg_codex_backup_20260729_before_white_free_lab_v3"
WORK = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg")
FIGURES = WORK / "textbook_figures_v3"
STAGING = Path(
    r"C:\Users\uugur\.codex\visualizations\2026\07\28\019faae7-0429-7922-9e1b-f4bb10c72700"
)
ASSET_DIR = LIVE / "figures" / "source-v3"


def load_v2():
    path = WORK / "rebuild_nonphys_deck.py"
    spec = importlib.util.spec_from_file_location("nonphys_v2", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


V2 = load_v2()
CHAIN = V2.build_chain()
EXPLANATIONS = set(V2.EXPLANATIONS)
EXISTING = set(V2.EXISTING_ANIMS)


def C(id_, label, min_, max_, step, value, unit):
    return [id_, label, min_, max_, step, value, unit]


def S(title, subtitle, kind, figure, figure_label, source, pubmed, controls, presets, rule):
    return {
        "title": title,
        "subtitle": subtitle,
        "kind": kind,
        "figure": figure,
        "figure_label": figure_label,
        "source": source,
        "pubmed": pubmed,
        "controls": controls,
        "presets": presets,
        "rule": rule,
    }


LABS = {
    "impedans-gurultu/animasyon-0-gurultu-haritasi.html": S(
        "Doymuş kayıt ekranını 50/60 Hz olarak tanıma laboratuvarı",
        "Bu laboratuvarın tek sorusu: anlaşılmaz dik çizgilerin altında hangi sinyal var?",
        "noise_recognition",
        "fig_8_5_impedance_noise.png",
        "Şekil 8.5 - sensitivite değişince görünen 60 Hz",
        "Preston & Shapiro, Bölüm 8, s. 82",
        "",
        [C("sens", "Sensitivite", 20, 10000, 20, 20, "µV/div"), C("noise", "Ortak şebeke gürültüsü", 0, 100, 1, 78, "%")],
        [["20 µV/div - doygun", [20, 78]], ["1 mV/div", [1000, 78]], ["10 mV/div - 60 Hz görünür", [10000, 78]]],
        "Tekrarlayan dik çizgilerde sensitiviteyi geçici olarak düşürmek, doygunluğun altındaki 50/60 Hz kaynağını gösterebilir.",
    ),
    "impedans-gurultu/animasyon-3-ohm-empedans.html": S(
        "G1 ve G2 empedans eşleşmesi laboratuvarı",
        "Aynı indüklenen akım, iki farklı empedansta iki farklı giriş voltajına dönüşür.",
        "impedance",
        "fig_8_4_differential.png",
        "Şekil 8.4 - diferansiyel amplifikasyon ve empedans uyumsuzluğu",
        "Preston & Shapiro, Bölüm 8, s. 82-83",
        "https://pubmed.ncbi.nlm.nih.gov/31654663/",
        [C("r1", "G1 empedansı", 1, 50, 1, 5, "kΩ"), C("r2", "G2 empedansı", 1, 50, 1, 5, "kΩ")],
        [["Eşleşmiş", [5, 5]], ["Orta uyumsuzluk", [5, 15]], ["Belirgin uyumsuzluk", [5, 35]]],
        "Düşük empedans tek başına yeterli değildir; G1 ve G2'nin birbirine yakın empedanslarda olması ortak mod reddini korur.",
    ),
    "filtreler/animasyon-0-filtre-spektrumu.html": S(
        "Sinyalin hangi frekans bileşenleri ekranda kalır?",
        "Passband laboratuvarı gürültü azaltma ile hedef yanıtı koruma arasındaki sınırı gösterir.",
        "filter_spectrum",
        "fig_8_8_filter_stack.png",
        "Şekil 8.8 - yüksek kesim filtresi ve DSAP görünürlüğü",
        "Preston & Shapiro, Bölüm 8, s. 83-84",
        "",
        [C("lff", "Alçak kesim", 1, 100, 1, 20, "Hz"), C("hff", "Yüksek kesim", 500, 20000, 100, 2000, "Hz")],
        [["Duysal 20 Hz-2 kHz", [20, 2000]], ["Motor 10 Hz-10 kHz", [10, 10000]], ["Aşırı dar 100 Hz-0.5 kHz", [100, 500]]],
        "Filtre ayarı yalnız gürültüyü değil, kaydedilen potansiyelin frekans içeriğini ve morfolojisini de belirler.",
    ),
    "filtreler/animasyon-2-filtre-odunlesimi.html": S(
        "Filtre değişikliğinin amplitüd ve süre bedeli",
        "Gerçek referans kayıtla kalibre edilmiş DSAP morfoloji laboratuvarı.",
        "filter_tradeoff",
        "fig_8_9_filter_tradeoff.png",
        "Şekil 8.9 - 2 kHz'de 30 µV, 0.5 kHz'de 16 µV",
        "Preston & Shapiro, Bölüm 8, s. 84",
        "",
        [C("lff", "Alçak kesim", 1, 100, 1, 20, "Hz"), C("hff", "Yüksek kesim", 500, 5000, 100, 2000, "Hz")],
        [["Standart 20 Hz-2 kHz", [20, 2000]], ["HFF 0.5 kHz", [20, 500]], ["LFF 2 Hz", [2, 2000]]],
        "Filtre değiştirildikten sonra amplitüd veya süre değişimi patoloji olarak yorumlanmamalıdır.",
    ),
    "stimulus-artefakti/animasyon-3-kablo-induksiyonu.html": S(
        "Kayıt kablosuna indüklenen stimulus artefaktı",
        "Koaksiyel kablo ve fiziksel kablo ayrımının gerçek kayıt üzerindeki etkisi.",
        "cable",
        "fig_8_12_cables.png",
        "Şekil 8.12 - koaksiyel kablo ve ayrı serbest iletkenler",
        "Preston & Shapiro, Bölüm 8, s. 85",
        "",
        [C("spacing", "Kablolar arası mesafe", 0, 30, 1, 20, "cm"), C("shield", "Koaksiyel kalkan", 0, 100, 1, 100, "%")],
        [["Koaksiyel + ayrık", [25, 100]], ["Yakın koaksiyel", [4, 100]], ["Üst üste serbest teller", [0, 0]]],
        "Stimülatör ve kayıt kabloları ayrılmalı; G1-G2 iletkenleri birbirine yakın ve tercihen koaksiyel olmalıdır.",
    ),
    "katot-polarite/animasyon-0-depolarizasyon-anodal-blok.html": S(
        "Katot, gerçek başlangıç noktası ve anodal blok",
        "Ölçüm mesafesinin neden stimülatör gövdesinden değil katottan başladığını gösterir.",
        "polarity_mechanism",
        "fig_8_14_15_cathode_anode.png",
        "Şekil 8.14-8.15 - katodal depolarizasyon ve teorik anodal blok",
        "Preston & Shapiro, Bölüm 8, s. 86",
        "https://pubmed.ncbi.nlm.nih.gov/3224657/",
        [C("reverse", "Polarite yönü", 0, 1, 1, 0, ""), C("block", "Anodal blok olasılığı", 0, 100, 1, 0, "%")],
        [["Katot G1'e bakıyor", [0, 0]], ["Ters polarite", [1, 0]], ["Ters + anodal blok modeli", [1, 80]]],
        "Her uyarım noktasında katot yönü ve ölçümün katot-G1 arasında yapıldığı doğrulanmalıdır.",
    ),
    "supramaksimal/animasyon-0-akson-rekrutmani.html": S(
        "Akım arttıkça BKAP rekrutmanı ve latans nasıl değişir?",
        "Şekil 8.17'nin gerçek sayılarıyla kalibre edilmiş kademeli uyarım laboratuvarı.",
        "supramax_waterfall",
        "fig_8_17_supramaximal.png",
        "Şekil 8.17 - 6, 7.2, 9, 11 ve 14 mA kayıtları",
        "Preston & Shapiro, Bölüm 8, s. 87",
        "https://pubmed.ncbi.nlm.nih.gov/27413732/",
        [C("current", "Uyarım akımı", 6, 14, 0.1, 9, "mA"), C("depth", "Sinir derinliği", 0, 100, 1, 20, "%")],
        [["Submaksimal 6 mA", [6, 20]], ["Plato 11 mA", [11, 20]], ["Plato + yaklaşık %25", [14, 20]]],
        "Supramaksimal uyarım cihaz çıkışıyla değil, amplitüd platosu ve plato üstünde ek akımla doğrulanır.",
    ),
    "kostimulasyon/animasyon-0-akim-yayilimi.html": S(
        "Ko-stimülasyonu çift kanal ve twitch ile yakalama",
        "Hedef APB ve komşu ADM eşzamanlı kaydı, basit bir akım çemberinden daha güvenilirdir.",
        "costim_dual",
        "fig_8_19_costimulation.png",
        "Şekil 8.19 - aşırı akımda komşu median-ulnar katkısı",
        "Preston & Shapiro, Bölüm 8, s. 88-90; Box 8.5",
        "",
        [C("current", "Uyarım akımı", 10, 80, 1, 35, "mA"), C("offset", "Stimülatör lateral-medial sapması", -20, 20, 1, 0, "mm")],
        [["Hedef üzerinde 35 mA", [35, 0]], ["Yüksek akım 60 mA", [60, 0]], ["Sapmış + yüksek akım", [60, 15]]],
        "Ani morfoloji veya twitch değişiminde ko-stimülasyon düşünülmeli ve komşu kas ikinci kanalda kaydedilmelidir.",
    ),
    "motor-elektrot-yerlesimi/animasyon-0-belly-tendon-montaj.html": S(
        "BKAP aslında G1 eksi G2'dir",
        "Elektriksel olarak aktif tendon elektrodunun nihai dalga biçimine katkısı.",
        "belly_tendon",
        "fig_8_24_g1_g2.png",
        "Şekil 8.24 - ulnar BKAP'ta G1 ve tendon G2 katkısı",
        "Preston & Shapiro, Bölüm 8, s. 90-92",
        "https://pubmed.ncbi.nlm.nih.gov/8455652/",
        [C("g1", "G1 kas potansiyeli", 40, 120, 1, 100, "%"), C("g2", "G2 tendon potansiyeli", 0, 100, 1, 70, "%")],
        [["Median - küçük G2", [100, 15]], ["Ulnar - belirgin G2", [100, 70]], ["Asimetrik G2 yerleşimi", [100, 100]]],
        "Karşılaştırmalı motor çalışmalarda G2 konumu, G1 kadar standart tutulmalıdır.",
    ),
    "antidromik-ortodromik/animasyon-2-sahte-dsap.html": S(
        "Antidromik kayıtta motor uzak-alan potansiyeli sahte DSAP olabilir",
        "Gerçek erken DSAP ile daha geç hacim iletilen motor bileşeni ayrı ayrı kontrol edilir.",
        "false_snap",
        "fig_8_26_anti_ortho.png",
        "Şekil 8.26 - antidromik DSAP ve geç motor bileşen",
        "Preston & Shapiro, Bölüm 8, s. 92-93",
        "https://pubmed.ncbi.nlm.nih.gov/2369294/",
        [C("snap", "Gerçek DSAP amplitüdü", 0, 40, 1, 22, "µV"), C("motor", "Geç motor uzak-alan bileşeni", 0, 100, 1, 70, "%")],
        [["Normal DSAP + motor", [22, 70]], ["Küçük DSAP", [6, 70]], ["DSAP yok - yalnız motor", [0, 70]]],
        "Antidromik kayıtta erken DSAP gösterilmeden geç motor bileşen duysal yanıt olarak raporlanmamalıdır.",
    ),
    "elektrot-sinir-mesafesi/animasyon-0-derinlik-filtresi.html": S(
        "Doku mesafesi yüksek frekans filtresi gibi davranır",
        "Derinlik arttıkça yalnız amplitüd değil; süre, onset ve peak ilişkisi de değişir.",
        "tissue_filter",
        "fig_8_28_depth_edema.png",
        "Şekil 8.28 - ödemde atenüasyon ve temporal yayılma",
        "Preston & Shapiro, Bölüm 8, s. 93-94",
        "https://pubmed.ncbi.nlm.nih.gov/10627934/",
        [C("depth", "Ek doku mesafesi", 0, 20, 0.5, 0, "mm"), C("edema", "Ödem dağılımı", 0, 100, 1, 0, "%")],
        [["Yüzeyel sinir", [0, 0]], ["Orta derinlik", [8, 20]], ["Belirgin ödem", [18, 100]]],
        "Belirgin ödemde düşük veya kayıp duysal yanıt tek başına akson kaybı kanıtı değildir.",
    ),
    "elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html": S(
        "Sabit akımla medial-lateral elektrot arama",
        "En yüksek amplitüdün bulunduğu konum, güvenilir yan karşılaştırmasının başlangıcıdır.",
        "electrode_search",
        "fig_8_27_electrode_search.png",
        "Şekil 8.27 - sinir üzerinde 38 µV, 0.5 cm lateralde 31 µV, 1 cm lateralde 12 µV",
        "Preston & Shapiro, Bölüm 8, s. 93-94",
        "https://pubmed.ncbi.nlm.nih.gov/9052817/",
        [C("offset", "Elektrotun sinire göre konumu", -10, 10, 0.5, 0, "mm"), C("current", "Sabit uyarım akımı", 20, 80, 1, 50, "%")],
        [["Sinir üzerinde", [0, 50]], ["5 mm lateral", [5, 50]], ["10 mm lateral", [10, 50]]],
        "Yan karşılaştırmasından önce her iki tarafta da bağımsız elektrot araması yapılmalıdır.",
    ),
    "elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html": S(
        "Elektrot sapması onseti sola kaydırıp yalancı hızlı İH üretebilir",
        "Aynı gerçek sinir iletisinde ölçüm geometrisinin İH hesabını nasıl bozduğu.",
        "false_speed",
        "fig_8_29_false_speed.png",
        "Şekil 8.29 - sinir dışından kayıtta onsetin sola kayması",
        "Preston & Shapiro, Bölüm 8, s. 94",
        "https://pubmed.ncbi.nlm.nih.gov/9052817/",
        [C("offset", "Medial-lateral sapma", 0, 15, 0.5, 0, "mm"), C("distance", "Uyarı-kayıt mesafesi", 8, 20, 0.5, 14, "cm")],
        [["Sinir üzerinde", [0, 14]], ["5 mm sapma", [5, 14]], ["10 mm sapma", [10, 14]]],
        "Şüpheli yüksek İH veya düşük amplitüd birlikteyse elektrot-sinir geometrisi doğrulanmalıdır.",
    ),
    "ekstremite-mesafe/animasyon-2-kaliper.html": S(
        "Düz cetvel yerine sinir yolunu izleyen kontur ölçümü",
        "Radyal spiral ve Erb-aksilla gibi kıvrımlı segmentlerde mesafe hatasını gösterir.",
        "caliper",
        "fig_8_32_elbow_distance.png",
        "Şekil 8.32 - yüzey konturu ve gerçek sinir yolu",
        "Preston & Shapiro, Bölüm 8, s. 94-96",
        "https://pubmed.ncbi.nlm.nih.gov/7870113/",
        [C("curve", "Sinir yolu kıvrımı", 0, 100, 1, 55, "%"), C("segment", "Segment uzunluğu", 10, 30, 0.5, 20, "cm")],
        [["Düz segment", [0, 20]], ["Radyal spiral", [55, 20]], ["Erb-aksilla konturu", [90, 25]]],
        "Kıvrımlı proksimal segmentlerde ölçüm aracı sinirin anatomik yolunu izlemelidir.",
    ),
}


LAB_CSS = r"""
:root{--bg:#eef1f4;--paper:#fff;--panel:#f7f9fb;--panel-head:#e7edf3;--line:#d5dde4;--line2:#becbd5;--ink:#16232c;--muted:#5d6b76;--dim:#8b98a2;--cyan:#0f7a95;--blue:#2f6fbd;--amber:#c97a2a;--green:#2f7d52;--red:#b43b47;--scope:#03110c;--grid:#16362a;--trace:#79e3ac}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#ccd4da;color:var(--ink);font-family:"Segoe UI",Inter,Arial,sans-serif}body{display:grid;place-items:center;padding:14px}
button,input{font:inherit}.app{position:relative;width:min(calc(100vw - 28px),1500px);aspect-ratio:16/9;max-height:calc(100vh - 28px);overflow:hidden;background:var(--bg);border:1px solid #c7d0d8;border-radius:6px;box-shadow:0 24px 60px rgba(20,33,43,.24);display:grid;grid-template-rows:50px 38px minmax(0,1fr) 104px 56px}
.titlebar{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:0 18px;background:linear-gradient(180deg,#fff,#eef1f4);border-bottom:1px solid var(--line)}.title-left{min-width:0;display:flex;align-items:center;gap:10px}.status-dot{width:9px;height:9px;border-radius:50%;background:var(--green);box-shadow:0 0 5px rgba(47,125,82,.45);flex:none}.title-left h1{margin:0;font-size:20px;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.lab-badge{flex:none;border:1px solid #9bb5bf;background:#eaf5f8;color:#155a6c;padding:6px 9px;font-size:12px;font-weight:800;letter-spacing:.07em}
.topicbar{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:0 18px;background:var(--panel-head);border-bottom:1px solid var(--line);font-size:13px}.subtitle{min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#3f4d57;font-weight:650}.topicbar .mode{color:var(--muted);white-space:nowrap}.topicbar .mode b{color:var(--cyan)}
.workspace{min-height:0;display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:12px;padding:12px}.scope-panel,.source-panel{min-width:0;min-height:0;border:1px solid var(--line);background:var(--paper);overflow:hidden}.scope-panel{position:relative;background:var(--scope)}#labCanvas{position:absolute;inset:0;width:100%;height:100%}.scope-head{position:absolute;z-index:2;left:14px;right:14px;top:10px;display:flex;justify-content:space-between;pointer-events:none;color:#b8d1c8;font:12px/1.2 Consolas,monospace;letter-spacing:.04em}.scope-head b{color:#e8fff4}.scope-readout{position:absolute;z-index:2;right:14px;top:36px;max-width:390px;text-align:right;background:rgba(3,17,12,.86);border-right:3px solid var(--amber);padding:8px 10px;color:#dceae5;font-size:13px}.scope-readout strong{display:block;color:#fff;font-size:17px;margin-bottom:3px}.scope-note{position:absolute;z-index:2;left:14px;bottom:12px;max-width:650px;background:rgba(3,17,12,.88);border-left:3px solid var(--cyan);padding:7px 10px;color:#d8e8e2;font-size:13px}
.source-panel{display:grid;grid-template-rows:34px minmax(0,1fr) auto}.source-head{display:flex;align-items:center;padding:0 12px;background:var(--panel-head);border-bottom:1px solid var(--line);font-size:12px;font-weight:850;letter-spacing:.06em;text-transform:uppercase;color:#4b5963}.source-figure{min-height:0;display:grid;place-items:center;padding:8px;background:#fff}.source-figure img{display:block;max-width:100%;max-height:100%;object-fit:contain}.source-meta{padding:9px 11px;border-top:1px solid var(--line);font-size:11px;line-height:1.35;color:var(--muted)}.source-meta b{display:block;color:var(--ink);margin-bottom:4px}.source-meta a{color:var(--cyan);text-decoration:none}
.controls{display:grid;grid-template-columns:1fr 1fr 1.25fr;gap:20px;align-items:center;padding:10px 18px;background:#fff;border-top:1px solid var(--line)}.control{min-width:0}.control label{display:flex;justify-content:space-between;gap:10px;font-size:12px;color:var(--muted);font-weight:750;margin-bottom:7px}.control output{color:var(--ink);font-weight:850}.control input{width:100%;accent-color:var(--cyan)}.preset-wrap label{display:block;font-size:12px;color:var(--muted);font-weight:750;margin-bottom:7px}.presets{display:flex;gap:6px;flex-wrap:wrap}.preset{border:1px solid #aebbc5;background:#f2f5f7;color:#24323b;padding:7px 9px;font-size:11px;font-weight:750;cursor:pointer}.preset:hover,.preset:focus-visible,.preset.active{border-color:var(--cyan);background:#e5f2f5;outline:none}
.bottom-bar{display:flex;align-items:stretch;gap:1px;background:var(--line);border-top:1px solid var(--line)}.fkey{flex:1;background:var(--panel-head);color:var(--ink);text-decoration:none;display:flex;align-items:center;justify-content:center;gap:9px;font-size:13px;font-weight:800}.fkey span{color:var(--cyan);font-size:15px}.fkey:hover,.fkey:focus-visible{background:#dce8f0;outline:none}
@media(max-width:1000px){body{padding:0}.app{width:100vw;height:100vh;max-height:none;aspect-ratio:auto;border-radius:0;grid-template-rows:48px 34px minmax(0,1fr) 154px 52px}.workspace{grid-template-columns:1fr}.source-panel{display:none}.controls{grid-template-columns:1fr 1fr}.preset-wrap{grid-column:1/-1}.title-left h1{font-size:17px}}
"""


NAV_CSS = r"""
/* standard-nav-v3 */
.bottom-bar{flex:none;height:56px;display:flex!important;align-items:stretch!important;gap:1px!important;background:#d5dde4!important;border-top:1px solid #d5dde4!important}.bottom-bar .fkey{flex:1!important;background:#e7edf3!important;color:#16232c!important;text-decoration:none!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:9px!important;padding:0 12px!important;font:800 13px/1 "Segoe UI",Arial,sans-serif!important}.bottom-bar .fkey span{color:#0f7a95!important;font-size:15px!important}.bottom-bar .fkey b{color:#16232c!important;font-size:13px!important}.bottom-bar .fkey:hover,.bottom-bar .fkey:focus-visible{background:#dce8f0!important;outline:none!important}
"""


LAB_SCRIPT = r"""
const spec=__SPEC__;
const canvas=document.getElementById("labCanvas"),ctx=canvas.getContext("2d");
const inputs=[...document.querySelectorAll(".control input")],outputs=[...document.querySelectorAll(".control output")],presets=[...document.querySelectorAll(".preset")];
const readout=document.getElementById("readout"),note=document.getElementById("scopeNote");
let phase=0;
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function gauss(x,m,s){const z=(x-m)/s;return Math.exp(-.5*z*z)}
function pseudo(x){return .46*Math.sin(x*37.3)+.28*Math.sin(x*71.1+1.4)+.17*Math.sin(x*113.7+.2)+.09*Math.sin(x*181.4+2.1)}
function fmt(v,d=0){return Number(v).toFixed(d)}
function vals(){return inputs.map(el=>Number(el.value))}
function resize(){const r=canvas.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);canvas.width=Math.max(1,Math.round(r.width*d));canvas.height=Math.max(1,Math.round(r.height*d));ctx.setTransform(d,0,0,d,0,0)}
addEventListener("resize",resize);resize();
function text(s,x,y,color="#d9e9e3",size=13,align="left",weight=600){ctx.fillStyle=color;ctx.font=`${weight} ${size}px Segoe UI`;ctx.textAlign=align;ctx.fillText(s,x,y);ctx.textAlign="left"}
function line(points,color="#79e3ac",width=2,dash=[]){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.restore()}
function grid(x,y,w,h,divX=10,divY=6){ctx.save();ctx.fillStyle="#03110c";ctx.fillRect(x,y,w,h);ctx.strokeStyle="#16362a";ctx.lineWidth=1;for(let i=0;i<=divX;i++){const xx=x+w*i/divX;ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke()}for(let i=0;i<=divY;i++){const yy=y+h*i/divY;ctx.beginPath();ctx.moveTo(x,yy);ctx.lineTo(x+w,yy);ctx.stroke()}ctx.strokeStyle="#2f6a52";ctx.beginPath();ctx.moveTo(x,y+h/2);ctx.lineTo(x+w,y+h/2);ctx.stroke();ctx.restore()}
function scope(x,y,w,h,fn,color="#79e3ac",label="",dash=[]){grid(x,y,w,h);const pts=[];for(let i=0;i<=700;i++){const t=i/700;const raw=fn(t);const yy=clamp(y+h/2-raw*h*.36,y+2,y+h-2);pts.push([x+w*t,yy])}line(pts,color,2,dash);if(label)text(label,x+10,y+18,"#a8c2b8",12)}
function snap(t,amp=1,on=.31,width=1,artifact=.12){return artifact*(1.8*gauss(t,.055,.004)-1.15*gauss(t,.068,.010)) + amp*(1.05*gauss(t,on,.022*width)-.76*gauss(t,on+.050*width,.032*width)+.23*gauss(t,on+.115*width,.055*width))}
function cmap(t,amp=1,on=.26,width=1,positive=.0){return .15*(1.7*gauss(t,.045,.004)-gauss(t,.058,.012))+positive*gauss(t,on-.025,.018)+amp*(1.15*gauss(t,on,.045*width)-.85*gauss(t,on+.105*width,.065*width)+.16*gauss(t,on+.22*width,.09*width))}
function updateOutputs(){inputs.forEach((el,i)=>{const c=spec.controls[i],step=Number(c[4]);outputs[i].textContent=`${Number(el.value).toFixed(step<1?1:0)} ${c[6]}`.trim()})}
function selectPreset(i){const values=spec.presets[i][1];inputs.forEach((el,j)=>{el.value=values[j];el.dispatchEvent(new Event("input",{bubbles:true}))});presets.forEach((b,j)=>b.classList.toggle("active",i===j))}
inputs.forEach(el=>el.addEventListener("input",()=>{updateOutputs();presets.forEach(b=>b.classList.remove("active"))}));presets.forEach((b,i)=>b.addEventListener("click",()=>selectPreset(i)));updateOutputs();

function drawNoise(W,H,v){
  const sens=v[0],n=v[1]/100,amp=n*1800/sens;
  const x=22,y=48,w=W-44,h=H-78;
  scope(x,y,w,h,t=>amp*Math.sin(2*Math.PI*(8*t+phase))+.08*snap(t,1,.63,1,0),"#79e3ac","RADİAL DSAP · sensitivite taraması");
  const saturated=amp>.95;
  readout.innerHTML=`<strong>${saturated?"AMPLİFİKATÖR DOYGUN":"50/60 Hz SİNÜSÜ GÖRÜNÜR"}</strong>Sensitivite ${sens<1000?sens+" µV/div":fmt(sens/1000,1)+" mV/div"}`;
  note.textContent=saturated?"Dik çizgiler kaynak değildir; büyük sinüs dalgasının ekran sınırında kesilmiş görünümüdür.":"Daha düşük sensitivite, doygun kaydın altında şebeke frekanslı sinüsü açığa çıkardı.";
}
function drawImpedance(W,H,v){
  const r1=v[0],r2=v[1],base=.34,diff=Math.abs(r1-r2)/Math.max(r1,r2),x=22,w=W-44;
  scope(x,48,w,(H-112)/3,t=>base*Math.sin(2*Math.PI*(6*t+phase))+.08*snap(t,1,.68,1,0),"#ffc05c",`G1 girişi · Z=${r1} kΩ`);
  scope(x,56+(H-112)/3,w,(H-112)/3,t=>base*(r2/r1)*Math.sin(2*Math.PI*(6*t+phase))+.08*snap(t,1,.68,1,0),"#75b8ff",`G2 girişi · Z=${r2} kΩ`);
  scope(x,64+2*(H-112)/3,w,(H-112)/3,t=>base*(1-r2/r1)*Math.sin(2*Math.PI*(6*t+phase))+.55*snap(t,1,.68,1,0),"#79e3ac","G1 − G2 · amplifikatör çıkışı");
  readout.innerHTML=`<strong>ΔZ ${Math.abs(r1-r2).toFixed(0)} kΩ</strong>E = I × Z; eşleşme hatası ${Math.round(diff*100)}%`;
  note.textContent=diff<.08?"Ortak gürültü iki girişte benzer voltaj üretir ve çıkarma ile bastırılır.":"Aynı indüklenen akım farklı giriş voltajları oluşturur; kalan 50/60 Hz hedef sinyalle birlikte büyütülür.";
}
function drawFilterSpectrum(W,H,v){
  const lo=v[0],hi=v[1],x=35,y=55,w=W-70,h=155,fx=f=>x+w*(Math.log10(f)-0)/(Math.log10(30000));
  ctx.fillStyle="#071913";ctx.fillRect(x,y,w,h);ctx.strokeStyle="#1f4c3a";for(let i=0;i<6;i++){const yy=y+h*i/5;ctx.beginPath();ctx.moveTo(x,yy);ctx.lineTo(x+w,yy);ctx.stroke()}
  const pts=[];for(let i=0;i<=600;i++){const f=Math.pow(10,Math.log10(30000)*i/600);const hp=1/Math.sqrt(1+Math.pow(lo/f,4)),lp=1/Math.sqrt(1+Math.pow(f/hi,4));pts.push([fx(f),y+h-18-hp*lp*(h-36)])}line(pts,"#79e3ac",3);
  [[2,"bazal"],[50,"şebeke"],[700,"DSAP"],[12000,"HF gürültü"]].forEach(([f,l])=>{const xx=fx(f);ctx.strokeStyle="#43685a";ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke();text(l,xx,y+h-5,"#a8c2b8",11,"center")});
  scope(22,235,W-44,H-265,t=>.10*Math.sin(t*6*Math.PI)*(lo<10?1:.2)+(.65*(hi>=2000?.95:hi/2100))*snap(t,1,.47,hi<1000?1.5:1,0)+.10*(hi>8000?1:.25)*pseudo(t*4+phase),"#79e3ac","FİLTRELENMİŞ DSAP");
  readout.innerHTML=`<strong>${lo} Hz – ${hi>=1000?fmt(hi/1000,1)+" kHz":hi+" Hz"}</strong>Geçirgen bant`;
  note.textContent=hi<800?"Yüksek kesim hedef DSAP'ın hızlı bileşenlerini de bastırıyor.":lo>50?"Alçak kesim, yavaş bileşenleri azaltıp süre ve bazali değiştiriyor.":"Hedef yanıtın çoğu korunurken bant dışı gürültü kademeli zayıflatılıyor.";
}
function drawFilterTradeoff(W,H,v){
  const lo=v[0],hi=v[1],amp=hi<=500?16:16+14*clamp((hi-500)/1500,0,1),width=1+clamp((20-lo)/20,0,1)*.34;
  scope(22,55,W-44,(H-95)/2,t=>snap(t,1,.36,1,.22),"#ffc05c","REFERANS · 20 Hz–2 kHz",[7,5]);
  scope(22,63+(H-95)/2,W-44,(H-95)/2,t=>(amp/30)*snap(t,1,.36,width,.22),"#79e3ac",`SEÇİLEN · ${lo} Hz–${hi/1000} kHz`);
  readout.innerHTML=`<strong>${amp.toFixed(0)} µV</strong>Referans 30 µV · süre katsayısı ×${width.toFixed(2)}`;
  note.textContent=hi<=600?"Şekil 8.9 kalibrasyonu: HFF 2 kHz'den 0.5 kHz'ye düşünce DSAP 30 µV'den 16 µV'ye iner.":lo<5?"Düşük LFF daha fazla yavaş bileşen geçirir; potansiyel süresi uzar.":"Standart filtre referans morfolojisine yakın.";
}
function drawCable(W,H,v){
  const sep=v[0],shield=v[1]/100,ind=clamp((1-sep/30)*(1-.86*shield),0,1);
  text("STİMÜLATÖR KABLOSU",35,65,"#ff8b95",13);line([[35,82],[W-35,82]],"#ff6876",7);
  text("G1 / G2 KAYIT KABLOSU",35,118+sep*2,"#75cfe0",13);line([[35,135+sep*2],[W-35,135+sep*2]],"#48bfd2",shield>.5?10:4);
  if(shield>.5){line([[35,135+sep*2],[W-35,135+sep*2]],"#dbe8e4",2,[6,5]);text("koaksiyel dış kalkan",W*.5,160+sep*2,"#a8c2b8",11,"center")}
  scope(22,205,W-44,H-235,t=>ind*(1.9*gauss(t,.045,.007)-1.2*gauss(t,.075,.035))+.72*snap(t,1,.48,1,0),"#79e3ac","MEDİAN DSAP · stimulus artefaktı + yanıt");
  readout.innerHTML=`<strong>İNDÜKSİYON ${Math.round(ind*100)}%</strong>Kablo aralığı ${sep} cm · kalkan ${Math.round(shield*100)}%`;
  note.textContent=ind>.55?"Serbest teller ve örtüşen güzergâh, stimulus geçicisini kayıt devresine indüklüyor.":"Fiziksel ayrım ve koaksiyel geometri ortak indüksiyonu azaltıyor.";
}
function drawPolarity(W,H,v){
  const rev=v[0]>.5,block=v[1]/100,y=125,x1=65,x2=W-70,cath=rev?W*.34:W*.55,an=rev?W*.55:W*.34;
  line([[x1,y],[x2,y]],"#d9b15f",6);text("G1",x2,y-18,"#75cfe0",15,"center",800);
  [["KATOT",cath,"#1d252a"],["ANOT",an,"#b43b47"]].forEach(([lab,x,c])=>{ctx.fillStyle=c;ctx.beginPath();ctx.arc(x,y-34,18,0,Math.PI*2);ctx.fill();ctx.strokeStyle="#eef6f4";ctx.lineWidth=2;ctx.stroke();text(lab,x,y-65,c==="#1d252a"?"#fff":"#ff9aa3",12,"center",800)});
  const dir=rev?-1:1;ctx.strokeStyle="#48d7e8";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(cath,y);ctx.lineTo(cath+dir*90,y);ctx.stroke();text("depolarizasyon",cath+dir*105,y+5,"#48d7e8",12,dir>0?"left":"right");
  if(block>.05){ctx.fillStyle=`rgba(255,104,118,${.15+.55*block})`;ctx.fillRect(an-14,y-15,28,30);text("hiperpolarizasyon",an,y+42,"#ff9aa3",11,"center")}
  const latency=2.2+(rev?.35:0),amp=1-.85*block;
  scope(22,205,W-44,H-235,t=>amp*snap(t,1,.32+latency/20,1,.24),"#79e3ac","DUYSAL YANIT");
  readout.innerHTML=`<strong>${latency.toFixed(2)} ms</strong>${rev?"Ek 2.5–3.0 cm aktivasyon yolu":"Mesafe katot-G1 arasında"}`;
  note.textContent=block>.6?"Anodal blok yanıtı azaltabilir; kitap bunun pratikte nadir olduğunu vurgular.":rev?"Ters polarite depolarizasyon başlangıcını G1'den uzaklaştırır ve distal latansı yaklaşık 0.3–0.4 ms uzatır.":"Katot G1'e bakıyor; ölçülen ve gerçek aktivasyon mesafesi eşleşir.";
}
function interpTable(cur){
  const rows=[[6,4.5,3.6],[7.2,6.8,3.5],[9,9.3,3.5],[11,10.5,3.2],[14,10.5,3.1]];
  for(let i=0;i<rows.length-1;i++){if(cur<=rows[i+1][0]){const a=rows[i],b=rows[i+1],q=(cur-a[0])/(b[0]-a[0]);return [a[1]+q*(b[1]-a[1]),a[2]+q*(b[2]-a[2])]}}return [10.5,3.1]
}
function drawSupramax(W,H,v){
  const cur=v[0],depth=v[1]/100,[a0,lat]=interpTable(cur),amp=a0*(1-.22*depth),rows=[[6,4.5,3.6],[7.2,6.8,3.5],[9,9.3,3.5],[11,10.5,3.2],[14,10.5,3.1]];
  const hh=(H-75)/5;rows.forEach((r,i)=>{const alpha=1-Math.min(1,Math.abs(cur-r[0])/5)*.55;scope(22,48+i*hh,W-44,hh-6,t=>(r[1]/10.5)*cmap(t,1,.24+(r[2]-3.1)*.025,1,0),"rgba(121,227,172,"+alpha.toFixed(2)+")",`${r[0]} mA · ${r[1]} mV · ${r[2]} ms`)});
  readout.innerHTML=`<strong>${amp.toFixed(1)} mV · ${lat.toFixed(2)} ms</strong>${cur>=14?"Plato + yaklaşık %25 doğrulama":cur>=11?"Amplitüd platosu":"Submaksimal rekrutman"}`;
  note.textContent=cur<11?"Akım arttıkça daha fazla akson katılır; BKAP büyür ve en hızlı liflerin devreye girmesiyle latans kısalır.":"11–14 mA arasında amplitüd değişmiyor: plato gösterildi ve ek akımla supramaksimal düzey doğrulandı.";
}
function drawCostim(W,H,v){
  const cur=v[0],off=Math.abs(v[1]),target=clamp((cur-12)/28,0,1)*Math.exp(-off/28),adj=clamp((cur-45)/25+off/35,0,1);
  scope(22,58,W-44,(H-120)/2,t=>target*cmap(t,1,.28,1,0)+adj*.32*cmap(t,1,.34,.85,0),"#79e3ac","KANAL 1 · APB (median hedef)");
  scope(22,72+(H-120)/2,W-44,(H-120)/2,t=>adj*cmap(t,1,.32,1,0),"#75b8ff","KANAL 2 · ADM (ulnar komşu)");
  const status=adj>.15?"KO-STİMÜLASYON":"SEÇİCİ UYARIM";
  readout.innerHTML=`<strong>${status}</strong>APB ${Math.round(target*100)}% · ADM ${Math.round(adj*100)}%`;
  note.textContent=adj>.15?"ADM kanalında potansiyel ve daha yaygın el fleksiyonu, akım yayılımını doğruluyor; amplitüd artık yalnız median sinire ait değil.":"APB yanıtı artarken ADM sessiz ve twitch thenar ağırlıklı: hedef sinir seçici uyarılıyor.";
}
function drawBelly(W,H,v){
  const g1=v[0]/100,g2=v[1]/100,x=22,w=W-44,hh=(H-105)/3;
  scope(x,55,w,hh,t=>g1*cmap(t,1,.25,1,0),"#ffc05c","G1 · kas karnı");
  scope(x,63+hh,w,hh,t=>g2*(.62*gauss(t,.31,.055)-.45*gauss(t,.43,.075)),"#75b8ff","G2 · tendon / uzak-alan potansiyeli");
  scope(x,71+2*hh,w,hh,t=>g1*cmap(t,1,.25,1,0)-g2*(.62*gauss(t,.31,.055)-.45*gauss(t,.43,.075)),"#79e3ac","EKRAN · G1 − G2");
  readout.innerHTML=`<strong>G1 − G2</strong>Tendon katkısı ${Math.round(g2*100)}%`;
  note.textContent=g2>.55?"Ulnar/tibial montajda pozitif G2 katkısı çıkarıldığında nihai negatif BKAP büyür ve bifid morfoloji oluşabilir.":"Median benzeri küçük G2 katkısında nihai BKAP ağırlıklı olarak G1'i temsil eder.";
}
function drawFalseSnap(W,H,v){
  const sa=v[0]/22,mo=v[1]/100,x=22,y=62,w=W-44,h=H-94;
  scope(x,y,w,h,t=>sa*snap(t,1,.27,1,.18)+mo*.82*cmap(t,1,.58,1.2,0),"#79e3ac","ANTİDROMİK D2 KAYDI");
  const snapX=x+w*.27,motorX=x+w*.58;ctx.strokeStyle="#ffc05c";ctx.setLineDash([5,4]);ctx.beginPath();ctx.moveTo(snapX,y);ctx.lineTo(snapX,y+h);ctx.stroke();ctx.strokeStyle="#75b8ff";ctx.beginPath();ctx.moveTo(motorX,y);ctx.lineTo(motorX,y+h);ctx.stroke();ctx.setLineDash([]);text("DSAP penceresi",snapX+5,y+25,"#ffc05c",11);text("motor uzak-alan",motorX+5,y+25,"#75b8ff",11);
  readout.innerHTML=`<strong>${v[0]>1?v[0].toFixed(0)+" µV DSAP":"DSAP YOK"}</strong>Geç motor bileşen ${Math.round(mo*100)}%`;
  note.textContent=v[0]<1?"Erken duysal bileşen yok; geç hacim iletilen motor potansiyeli DSAP olarak işaretlenmemelidir.":"Erken DSAP, geç motor bileşenden latans ve morfoloji ile ayrılıyor.";
}
function drawTissue(W,H,v){
  const depth=v[0],ed=v[1]/100,att=Math.exp(-depth/13)*(1-.18*ed),wide=1+depth/24+.25*ed,on=.34-depth*.0015;
  text("YÜZEY ELEKTRODU",W*.5,62,"#75cfe0",12,"center",800);ctx.fillStyle="#d9b28e";ctx.fillRect(55,80,W-110,45+depth*3);ctx.fillStyle="rgba(105,162,210,.28)";ctx.fillRect(55,125,W-110,depth*3*ed);line([[70,155+depth*3],[W-70,155+depth*3]],"#d9b15f",7);
  scope(22,215,W-44,H-245,t=>snap(t,1,.34,1,.15),"#ffc05c","YÜZEYEL REFERANS",[7,5]);
  const x=22,y=215,w=W-44,h=H-245,pts=[];grid(x,y,w,h);for(let i=0;i<=700;i++){const t=i/700;pts.push([x+w*t,clamp(y+h/2-att*snap(t,1,on,wide,.15)*h*.36,y+2,y+h-2)])}line(pts,"#79e3ac",2);
  readout.innerHTML=`<strong>${Math.round(38*att)} µV</strong>Süre ×${wide.toFixed(2)} · onset ${on<.34?"hafif erken":"referans"}`;
  note.textContent=depth>12?"Doku hızlı bileşenleri atenüe eder; yanıt küçülür, genişler, onset hafif kısalabilir ve peak uzayabilir.":"Elektrot sinire yakın; yüksek frekanslı DSAP bileşenleri daha az atenüe olur.";
}
function ampFromOffset(mm){const a=Math.abs(mm);if(a<=5)return 38-(7*a/5);return Math.max(2,31-(19*(a-5)/5))}
function drawSearch(W,H,v){
  const off=v[0],cur=v[1]/50,amp=ampFromOffset(off)*cur,cx=W*.5,ex=cx+off*18;
  ctx.fillStyle="#c98f72";ctx.fillRect(45,60,W-90,125);ctx.fillStyle="#ffc05c";ctx.beginPath();ctx.arc(cx,130,19,0,Math.PI*2);ctx.fill();ctx.fillStyle="#20282d";ctx.beginPath();ctx.arc(ex,78,15,0,Math.PI*2);ctx.fill();line([[ex,95],[ex,110]],"#75cfe0",2,[4,3]);text("sinir",cx,165,"#68402e",11,"center",800);text(`offset ${off.toFixed(1)} mm`,ex,52,"#75cfe0",11,"center");
  scope(22,215,W-44,H-245,t=>(amp/38)*snap(t,1,.33-Math.abs(off)*.0015,1+.02*Math.abs(off),.16),"#79e3ac","MEDİAN MİKST YANIT");
  readout.innerHTML=`<strong>${amp.toFixed(0)} µV</strong>Uyarım akımı sabit · konum taraması`;
  note.textContent=Math.abs(off)<1?"Maksimum amplitüd bulundu: elektrot sinir üzerinde.":`Kitap kalibrasyonu: 0 / 5 / 10 mm sapmada yaklaşık 38 / 31 / 12 µV. Bu konum yan karşılaştırması için uygun değildir.`;
}
function drawFalseSpeed(W,H,v){
  const off=v[0],dist=v[1],trueCV=70,trueLat=dist/trueCV*10,shift=.022*off,measLat=trueLat-shift,measCV=dist/measLat*10,amp=ampFromOffset(off);
  scope(22,80,W-44,H-115,t=>(amp/38)*snap(t,1,.36-shift/4,1+.02*off,.16),"#79e3ac","MİKST YANIT · onset imleci");
  const x=22,y=80,w=W-44,h=H-115,tx=x+w*.36,mx=x+w*(.36-shift/4);ctx.strokeStyle="#ffc05c";ctx.setLineDash([6,4]);ctx.beginPath();ctx.moveTo(tx,y);ctx.lineTo(tx,y+h);ctx.stroke();ctx.strokeStyle="#48d7e8";ctx.beginPath();ctx.moveTo(mx,y);ctx.lineTo(mx,y+h);ctx.stroke();ctx.setLineDash([]);text("gerçek onset",tx+5,y+22,"#ffc05c",11);text("ölçülen onset",mx+5,y+40,"#48d7e8",11);
  readout.innerHTML=`<strong>${trueCV.toFixed(0)} → ${measCV.toFixed(0)} m/s</strong>${trueLat.toFixed(2)} ms gerçek · ${measLat.toFixed(2)} ms ölçülen`;
  note.textContent=off>4?"Hacim iletimi onseti sola kaydırdı; sabit mesafe daha kısa süreye bölündüğü için İH yalancı yüksek hesaplandı.":"Elektrot sinir üzerinde; onset ve İH hesabı referans değere yakın.";
}
function drawCaliper(W,H,v){
  const curve=v[0]/100,seg=v[1],x1=65,x2=W-65,y=H*.60,pts=[];let len=0,prev=null;
  for(let i=0;i<=260;i++){const t=i/260,x=x1+(x2-x1)*t,yy=y-curve*150*Math.sin(Math.PI*t)-curve*35*Math.sin(3*Math.PI*t);pts.push([x,yy]);if(prev)len+=Math.hypot(x-prev[0],yy-prev[1]);prev=[x,yy]}
  line([[x1,y],[x2,y]],"#8ea49b",2,[7,5]);line(pts,"#ffc05c",7);for(let i=0;i<9;i++){const p=pts[Math.round(i*260/8)];ctx.fillStyle="#48d7e8";ctx.beginPath();ctx.arc(p[0],p[1],5,0,Math.PI*2);ctx.fill()}
  const ratio=len/(x2-x1),contour=seg*ratio;
  text("DÜZ İKİ NOKTA ÖLÇÜMÜ",W*.27,75,"#9fb4ac",13,"center",800);text(`${seg.toFixed(1)} cm`,W*.27,108,"#fff",26,"center",800);
  text("KONTUR / KALİPER",W*.73,75,"#48d7e8",13,"center",800);text(`${contour.toFixed(1)} cm`,W*.73,108,"#fff",26,"center",800);
  text("sinirin yüzeyde izlenen anatomik yolu",W*.5,y+65,"#a8c2b8",12,"center");
  readout.innerHTML=`<strong>FARK ${(contour-seg).toFixed(1)} cm</strong>Düz ölçüm İH'yi ${Math.round((ratio-1)*100)}% bozabilir`;
  note.textContent=curve>.3?"Düz cetvel eğrisel yolu kısaltır; obstetrik kaliper yüzey konturunu izleyerek gerçek sinir uzunluğuna yaklaşır.":"Düz segmentte iki nokta ve kontur ölçümleri birbirine yakındır.";
}
function draw(now){
  phase=(now/1000)*.12;const r=canvas.getBoundingClientRect(),W=r.width,H=r.height,v=vals();ctx.clearRect(0,0,W,H);ctx.fillStyle="#03110c";ctx.fillRect(0,0,W,H);
  switch(spec.kind){
    case"noise_recognition":drawNoise(W,H,v);break;case"impedance":drawImpedance(W,H,v);break;case"filter_spectrum":drawFilterSpectrum(W,H,v);break;case"filter_tradeoff":drawFilterTradeoff(W,H,v);break;
    case"cable":drawCable(W,H,v);break;case"polarity_mechanism":drawPolarity(W,H,v);break;case"supramax_waterfall":drawSupramax(W,H,v);break;case"costim_dual":drawCostim(W,H,v);break;
    case"belly_tendon":drawBelly(W,H,v);break;case"false_snap":drawFalseSnap(W,H,v);break;case"tissue_filter":drawTissue(W,H,v);break;case"electrode_search":drawSearch(W,H,v);break;
    case"false_speed":drawFalseSpeed(W,H,v);break;case"caliper":drawCaliper(W,H,v);break;
  }requestAnimationFrame(draw)
}
requestAnimationFrame(draw);
"""


def href_from(src_rel: str, dst_rel: str) -> str:
    import os

    return Path(os.path.relpath(Path(dst_rel), Path(src_rel).parent)).as_posix()


def standard_nav(src_rel: str, prev_rel: str, next_rel: str) -> str:
    return f"""<div class="bottom-bar" aria-label="Standart sunum gezinmesi">
<a class="fkey" href="{href_from(src_rel, prev_rel)}"><span>F1</span><b>Önceki</b></a>
<a class="fkey" href="{href_from(src_rel, 'index.html')}"><span>F2</span><b>İçindekiler</b></a>
<a class="fkey" href="{href_from(src_rel, next_rel)}"><span>F3</span><b>Sonraki</b></a>
</div>"""


def keyboard_script() -> str:
    return """<script data-standard-nav-v3>
document.addEventListener("keydown",e=>{if(["INPUT","SELECT","TEXTAREA"].includes(document.activeElement?.tagName))return;const k=e.key.toUpperCase();const a=k==="F1"?document.querySelector(".bottom-bar .fkey:nth-child(1)"):k==="F2"?document.querySelector(".bottom-bar .fkey:nth-child(2)"):k==="F3"?document.querySelector(".bottom-bar .fkey:nth-child(3)"):null;if(a){e.preventDefault();location.href=a.href}});
</script>"""


def patch_standard_nav(text: str, rel: str, prev_rel: str, next_rel: str) -> str:
    text = re.sub(r"\s*/\* standard-nav-v3 \*/.*?</style>", "</style>", text, count=1, flags=re.S)
    text = text.replace("</style>", NAV_CSS + "\n</style>", 1)
    text = re.sub(
        r'<div\s+class=["\']bottom-bar["\'][^>]*>.*?</div>',
        standard_nav(rel, prev_rel, next_rel),
        text,
        count=1,
        flags=re.S | re.I,
    )
    if "Standart sunum gezinmesi" not in text:
        insertion = standard_nav(rel, prev_rel, next_rel)
        if "</main>" in text:
            text = text.replace("</main>", insertion + "\n</main>", 1)
        else:
            text = text.replace("</body>", insertion + "\n</body>", 1)
    text = re.sub(r'<script\s+data-standard-nav-v3>.*?</script>', "", text, flags=re.S)
    text = text.replace("</body>", keyboard_script() + "\n</body>", 1)
    return text


def lab_html(rel: str, spec: dict, prev_rel: str, next_rel: str) -> str:
    import html

    controls = "\n".join(
        f"""<div class="control"><label for="{c[0]}"><span>{html.escape(c[1])}</span><output></output></label>
<input id="{c[0]}" type="range" min="{c[2]}" max="{c[3]}" step="{c[4]}" value="{c[5]}"></div>"""
        for c in spec["controls"]
    )
    presets = "\n".join(
        f'<button class="preset{" active" if i == 0 else ""}" type="button">{html.escape(p[0])}</button>'
        for i, p in enumerate(spec["presets"])
    )
    pubmed = (
        f'<a href="{html.escape(spec["pubmed"])}" target="_blank" rel="noreferrer">PubMed doğrulaması</a>'
        if spec["pubmed"]
        else "Kaynak mekanizma: kullanıcı tarafından sağlanan ders kitabı"
    )
    payload = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    script = LAB_SCRIPT.replace("__SPEC__", payload)
    nav = standard_nav(rel, prev_rel, next_rel)
    return f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(spec['title'])}</title><style>{LAB_CSS}</style></head>
<body><main class="app" aria-labelledby="lab-title">
<div class="titlebar"><div class="title-left"><span class="status-dot"></span><h1 id="lab-title">{html.escape(spec['title'])}</h1></div><div class="lab-badge">SERBEST LABORATUVAR</div></div>
<div class="topicbar"><div class="subtitle">{html.escape(spec['subtitle'])}</div><div class="mode"><b>Canlı model</b> · kontroller ilk kareden açık</div></div>
<section class="workspace"><div class="scope-panel"><canvas id="labCanvas" aria-label="{html.escape(spec['title'])} interaktif NCS simülasyonu"></canvas>
<div class="scope-head"><span>NCS/EMG KAYIT EKRANI</span><span>20 µV/div veya 5 mV/div · 1-2 ms/div</span></div>
<div class="scope-readout" id="readout"></div><div class="scope-note" id="scopeNote"></div></div>
<aside class="source-panel"><div class="source-head">Kaynak kayıt ve mekanizma</div><div class="source-figure"><img src="../figures/source-v3/{html.escape(spec['figure'])}" alt="{html.escape(spec['figure_label'])}"></div>
<div class="source-meta"><b>{html.escape(spec['figure_label'])}</b>{html.escape(spec['source'])}<br>{pubmed}</div></aside></section>
<section class="controls">{controls}<div class="preset-wrap"><label>Klinik koşul</label><div class="presets">{presets}</div></div></section>
{nav}</main><script>{script}</script>{keyboard_script()}</body></html>"""


def restore_old_pages() -> None:
    for rel in sorted(EXPLANATIONS | EXISTING):
        src = BACKUP / rel
        dst = LIVE / rel
        if not src.exists():
            raise FileNotFoundError(f"Previous-version page missing: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def deploy_assets() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for src in FIGURES.glob("*.png"):
        shutil.copy2(src, ASSET_DIR / src.name)
    photo = STAGING / "stimulus-artifact-forearm.png"
    if photo.exists():
        shutil.copy2(photo, LIVE / "stimulus-artefakti" / photo.name)


def patch_stimulus_lab(rel: str, prev_rel: str, next_rel: str) -> None:
    src = V2_BACKUP / rel
    if not src.exists():
        src = LIVE / rel
    text = src.read_text(encoding="utf-8")
    text = re.sub(r'<nav\s+class=["\']prototype-nav["\'][^>]*>.*?</nav>', "", text, flags=re.S | re.I)
    overrides = r"""
/* free-lab-white-v3 */
html,body{background:#ccd4da!important;color:#16232c!important}
.app{background:#eef1f4!important;border-color:#c7d0d8!important;box-shadow:0 24px 60px rgba(20,33,43,.24)!important;grid-template-rows:58px minmax(0,1fr) 280px 92px 56px!important}
header{background:linear-gradient(180deg,#fff,#eef1f4)!important;border-bottom:1px solid #d5dde4!important;color:#16232c!important;padding:0 22px!important}
header h1{color:#16232c!important}.sub{color:#5d6b76!important}.header-actions,.prototype-nav,.step-dots,.lab-lock{display:none!important}
.controls{background:#fff!important;border-top:1px solid #d5dde4!important}.control label{color:#5d6b76!important}.control output{color:#16232c!important}
.preset{background:#f2f5f7!important;color:#24323b!important;border-color:#aebbc5!important}.preset.active,.preset:hover{background:#e5f2f5!important;border-color:#0f7a95!important}
.free-badge{margin-left:auto;border:1px solid #9bb5bf;background:#eaf5f8;color:#155a6c;padding:6px 9px;font-size:12px;font-weight:800;letter-spacing:.07em}
"""
    text = text.replace("</style>", overrides + NAV_CSS + "\n</style>", 1)
    text = text.replace("</header>", '<span class="free-badge">SERBEST LABORATUVAR</span></header>', 1)
    text = re.sub(r'<div\s+class=["\']bottom-bar["\'][^>]*>.*?</div>', "", text, flags=re.S | re.I)
    text = text.replace("</main>", standard_nav(rel, prev_rel, next_rel) + "\n</main>", 1)
    unlock = """<script data-free-lab-v3>
window.addEventListener("load",()=>{setTimeout(()=>{if(typeof window.applyStep==="function")window.applyStep(7);document.querySelectorAll(".controls input,.controls button").forEach(el=>{el.disabled=false;el.style.pointerEvents="";el.removeAttribute("aria-disabled")});const msg=document.querySelector("#eventLabel");if(msg)msg.innerHTML="<strong>Serbest laboratuvar:</strong> artefakt yönü, mesafe ve gerçek DSAP amplitüdünü doğrudan ayarlayın.";},0)});
</script>"""
    text = text.replace("</body>", unlock + keyboard_script() + "\n</body>", 1)
    (LIVE / rel).write_text(text, encoding="utf-8")


def update_index() -> None:
    path = LIVE / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\s*<!-- nonphys-status-v2 -->.*?<!-- /nonphys-status-v2 -->\s*", "\n", text, flags=re.S)
    text = re.sub(r"\s*<!-- nonphys-status-v3 -->.*?<!-- /nonphys-status-v3 -->\s*", "\n", text, flags=re.S)
    banner = """<!-- nonphys-status-v3 -->
<aside style="position:fixed;right:18px;bottom:18px;z-index:999;max-width:510px;padding:12px 15px;background:#fff;color:#16232c;border:1px solid #c3ceda;border-left:4px solid #0f7a95;box-shadow:0 10px 28px rgba(20,33,43,.18);font:650 13px/1.35 'Segoe UI',Arial,sans-serif">
Nonfizyolojik faktörler: önceki ayrıntılı açıklamalar + <b style="color:#2f7d52">yalnız serbest laboratuvar</b>. Tüm sayfalarda standart F1/F2/F3 akışı.
</aside>
<!-- /nonphys-status-v3 -->"""
    text = text.replace("</body>", banner + "\n</body>", 1)
    path.write_text(text, encoding="utf-8")


def validate() -> dict:
    missing = [rel for rel in CHAIN if not (LIVE / rel).exists()]
    guided = []
    nonwhite = []
    nav_errors = []
    broken_images = []
    for i, rel in enumerate(CHAIN):
        path = LIVE / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "guided-tour-v2" in text or "Gösterimi başlat" in text or "Önce rehberli" in text:
            guided.append(rel)
        if "background:#ccd4da" not in text and "--bg:#eef1f4" not in text:
            nonwhite.append(rel)
        if text.count('class="fkey"') != 3:
            nav_errors.append({"file": rel, "count": text.count('class="fkey"')})
        for src in re.findall(r'<img\b[^>]*src=["\']([^"\']+)["\']', text, flags=re.I):
            if src.startswith(("http:", "https:", "data:")):
                continue
            if not (path.parent / src).resolve().exists():
                broken_images.append({"file": rel, "src": src})
    restored_mismatch = []
    for rel in EXPLANATIONS:
        old = (BACKUP / rel).read_text(encoding="utf-8")
        cur = (LIVE / rel).read_text(encoding="utf-8")
        old_body = re.sub(r'<div\s+class=["\']bottom-bar["\'][^>]*>.*?</div>', "", old, flags=re.S | re.I)
        cur_body = re.sub(r'<div\s+class=["\']bottom-bar["\'][^>]*>.*?</div>', "", cur, flags=re.S | re.I)
        old_text = re.sub(r"<[^>]+>", " ", old_body)
        cur_text = re.sub(r"<[^>]+>", " ", cur_body)
        for token in re.findall(r"\b[\wğüşöçıİĞÜŞÖÇ]{5,}\b", old_text, flags=re.I):
            if token not in cur_text:
                restored_mismatch.append({"file": rel, "missing_token": token})
                break
    return {
        "pages": len(CHAIN),
        "restored_explanations": len(EXPLANATIONS),
        "restored_existing_labs": len(EXISTING),
        "new_research_labs": len(LABS) + 1,
        "missing_pages": missing,
        "guided_mode_residue": guided,
        "pages_without_white_shell": nonwhite,
        "navigation_errors": nav_errors,
        "broken_images": broken_images,
        "previous_text_mismatches": restored_mismatch,
    }


def main() -> None:
    if not BACKUP.exists() or not LIVE.exists():
        raise FileNotFoundError("Live deck or pre-rebuild backup is unavailable.")
    if len(CHAIN) != 69 or len(EXPLANATIONS) != 34 or len(EXISTING) != 20 or len(LABS) != 14:
        raise RuntimeError("V3 content contract changed unexpectedly.")
    restore_old_pages()
    deploy_assets()
    previous_before = "proksimal-distal/animasyon-1-segment-hizi.html"
    for i, rel in enumerate(CHAIN):
        prev_rel = previous_before if i == 0 else CHAIN[i - 1]
        next_rel = "index.html" if i == len(CHAIN) - 1 else CHAIN[i + 1]
        if rel in LABS:
            (LIVE / rel).write_text(lab_html(rel, LABS[rel], prev_rel, next_rel), encoding="utf-8")
        elif rel == "stimulus-artefakti/animasyon-0-mekanizma.html":
            patch_stimulus_lab(rel, prev_rel, next_rel)
        else:
            path = LIVE / rel
            text = path.read_text(encoding="utf-8")
            text = patch_standard_nav(text, rel, prev_rel, next_rel)
            path.write_text(text, encoding="utf-8")
    predecessor = LIVE / previous_before
    if predecessor.exists():
        text = predecessor.read_text(encoding="utf-8")
        text = patch_standard_nav(text, previous_before, "proksimal-distal/index.html", CHAIN[0])
        predecessor.write_text(text, encoding="utf-8")
    update_index()
    report = validate()
    (LIVE / "nonfizyolojik_v3_qa.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if any(
        report[key]
        for key in (
            "missing_pages",
            "guided_mode_residue",
            "pages_without_white_shell",
            "navigation_errors",
            "broken_images",
            "previous_text_mismatches",
        )
    ):
        raise RuntimeError("V3 structural validation failed.")


if __name__ == "__main__":
    main()
