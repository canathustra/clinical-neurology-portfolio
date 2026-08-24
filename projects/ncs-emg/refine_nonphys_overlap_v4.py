from __future__ import annotations

import importlib.util
import json
import re
import shutil
from pathlib import Path


WORK = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg")
V3_PATH = WORK / "rebuild_nonphys_v3.py"
spec = importlib.util.spec_from_file_location("nonphys_v3", V3_PATH)
v3 = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(v3)

C = v3.C
S = v3.S


REFINED = {
    "impedans-gurultu/animasyon-1-diferansiyel-amp.html": S(
        "Ortak gürültü ne zaman gerçekten iptal edilir?",
        "G1, G2 ve G1−G2 aynı zaman ekseninde izlenir; bu sayfa CMRR'nin kayıt karşılığını gösterir.",
        "cmr_three_trace",
        "fig_8_4_differential.png",
        "Şekil 8.4 — diferansiyel yükseltme: çıkış G1−G2",
        "Preston & Shapiro, Bölüm 8, s. 82",
        "https://pubmed.ncbi.nlm.nih.gov/31654663/",
        [
            C("common", "Ortak 50/60 Hz gürültüsü", 0, 100, 1, 70, "%"),
            C("mismatch", "Girişler arası uyumsuzluk", 0, 100, 1, 0, "%"),
        ],
        [
            ["Eşleşmiş giriş", [70, 0]],
            ["Orta uyumsuzluk", [70, 25]],
            ["Kötü eşleşme", [70, 65]],
        ],
        "Ortak mod reddi, gürültü iki girişte aynı voltaj olarak görülürse çalışır; eşleşmeyen girişlerde 50/60 Hz çıkışa sızar.",
    ),
    "impedans-gurultu/animasyon-2-gurultu-azaltma.html": S(
        "Gürültü kaynağını deneme-yanılma değil, örüntüyle bul",
        "Sürekli şebeke gürültüsü ile aralıklı kablo temas kusuru aynı kayıt hatası değildir.",
        "noise_fault_bench",
        "fig_8_6_frayed_cable.png",
        "Şekil 8.6 — yıpranmış kabloda aralıklı temas kusuru",
        "Preston & Shapiro, Bölüm 8, s. 83; Box 8.3",
        "",
        [
            C("contact", "Elektrot temas bozukluğu", 0, 100, 1, 15, "%"),
            C("cable", "Kablo temas kusuru", 0, 100, 1, 0, "%"),
        ],
        [
            ["Temiz kayıt", [0, 0]],
            ["Yüksek empedans", [75, 0]],
            ["Yıpranmış kablo", [15, 85]],
        ],
        "Düzenli 50/60 Hz önce empedans ve ortak mod zincirini; ani kesilme ve sıçramalar ise kablo/konnektör temasını düşündürür.",
    ),
    "filtreler/animasyon-1-gecirgen-bant.html": S(
        "Aynı filtreyi motor ve duysal kayda uygulamak aynı hata değildir",
        "Bu sayfa frekans spektrumunu tekrarlamaz; klinik kayıt türüne uygun preset seçimini sınar.",
        "recording_preset",
        "fig_8_7_passband.png",
        "Şekil 8.7 — geçirgen bant ve kademeli filtre eğimleri",
        "Preston & Shapiro, Bölüm 8, s. 83–84",
        "",
        [
            C("signal", "Kayıt türü: 0 motor / 1 duysal", 0, 1, 1, 1, ""),
            C("preset", "Preset: 0 motor / 1 duysal", 0, 1, 1, 1, ""),
        ],
        [
            ["Motor + motor preset", [0, 0]],
            ["Duysal + duysal preset", [1, 1]],
            ["Duysal + yanlış motor preset", [1, 0]],
        ],
        "Normal değer karşılaştırması, aynı çalışma türü ve aynı filtre preset'i ile yapılmalıdır.",
    ),
    "stimulus-artefakti/animasyon-2-artefakt-azaltma.html": S(
        "Artefaktın büyüklüğü kadar amplifikatörün toparlanma süresi de önemlidir",
        "Ölü ölçüm penceresi gerçek DSAP başlangıcını örttüğünde amplitüd ve latans birlikte bozulur.",
        "artifact_recovery",
        "fig_8_11_stimulus_measurement.png",
        "Şekil 8.11 — stimulus artefaktı gerçek yanıt ölçümünü örtebilir",
        "Preston & Shapiro, Bölüm 8, s. 84–85; Box 8.4",
        "",
        [
            C("artifact", "Stimulus artefaktı", 0, 10, 0.1, 7, "mV"),
            C("recovery", "Toparlanma süresi", 0, 4, 0.1, 2.2, "ms"),
        ],
        [
            ["Kontrollü kayıt", [1.5, 0.5]],
            ["Büyük ama kısa", [8, 0.7]],
            ["Uzun saturasyon", [8, 3.2]],
        ],
        "Yanıtı kurtaran müdahale yalnız artefakt pikini küçültmek değil, amplifikatörün yanıt öncesinde bazale dönmesini sağlamaktır.",
    ),
    "katot-polarite/animasyon-1-polarite-tersligi.html": S(
        "Tek bir ters polarite segment hızını nasıl yalancı değiştirir?",
        "Mekanizma sayfasından farklı olarak burada distal ve proksimal onsetler üzerinden gerçek ölçüm hatası hesaplanır.",
        "polarity_cv_case",
        "fig_8_13_walking_anode.png",
        "Şekil 8.13 — anot/katot yönü mesafe ve latans ölçümünü değiştirir",
        "Preston & Shapiro, Bölüm 8, s. 85–87",
        "https://pubmed.ncbi.nlm.nih.gov/3224657/",
        [
            C("distal", "Distal polarite: 0 doğru / 1 ters", 0, 1, 1, 0, ""),
            C("proximal", "Proksimal polarite: 0 doğru / 1 ters", 0, 1, 1, 1, ""),
        ],
        [
            ["İki nokta doğru", [0, 0]],
            ["Yalnız proksimal ters", [0, 1]],
            ["İki nokta ters", [1, 1]],
        ],
        "Polarite hatası yalnız distal latansı değil, iki uyarım noktası arasındaki latans farkını ve hesaplanan ileti hızını da bozabilir.",
    ),
    "supramaksimal/animasyon-1-uyari-egrisi.html": S(
        "Platoyu görmek yetmez: supramaksimal düzeyi nasıl kanıtlarsın?",
        "Kademeli dalga ailesinden sonra bu sayfa amplitüd–akım eğrisi, tekrar değişkenliği ve plato üstü güvenlik payını gösterir.",
        "plateau_protocol",
        "fig_8_17_supramaximal.png",
        "Şekil 8.17 — amplitüd platosu ve plato üzerinde ek akım",
        "Preston & Shapiro, Bölüm 8, s. 87",
        "https://pubmed.ncbi.nlm.nih.gov/27413732/",
        [
            C("current", "Uyarım akımı", 6, 18, 0.1, 11, "mA"),
            C("variability", "Tekrarlar arası değişkenlik", 0, 12, 1, 3, "%"),
        ],
        [
            ["Plato öncesi", [9, 3]],
            ["İlk plato", [11, 3]],
            ["Plato + %25", [14, 3]],
        ],
        "Supramaksimal uyarım, tek yüksek akım değeriyle değil; tekrarlanabilir amplitüd platosu ve plato üzerinde yaklaşık %25 ek akımla doğrulanır.",
    ),
    "kostimulasyon/animasyon-1-tanisal-hatalar.html": S(
        "Ko-stimülasyonun yeri, yalancı tanının yönünü belirler",
        "Distal ve proksimal hedef/komşu kas kanalları birlikte izlenerek üç farklı hata örüntüsü ayrılır.",
        "costim_four_channel",
        "fig_8_20_block_patterns.png",
        "Şekil 8.20 — distal/proksimal amplitüd örüntüleri ve ileti bloğu tuzakları",
        "Preston & Shapiro, Bölüm 8, s. 88–90",
        "",
        [
            C("distal", "Distal ko-stimülasyon", 0, 100, 1, 0, "%"),
            C("proximal", "Proksimal ko-stimülasyon", 0, 100, 1, 0, "%"),
        ],
        [
            ["Seçici uyarım", [0, 0]],
            ["Yalnız distal", [80, 0]],
            ["Yalnız proksimal", [0, 80]],
        ],
        "Komşu kas kanalı kaydedilmeden amplitüd farkının akson kaybı mı, ileti bloğu mu, yoksa ko-stimülasyon mu olduğu güvenle söylenemez.",
    ),
    "kostimulasyon/animasyon-2-optimal-yerlesim.html": S(
        "En düşük eşik noktasını bulmak ko-stimülasyonu önler",
        "Bu sayfa ko-stimülasyonu tekrar göstermiyor; stimülatör konumu ve gerekli akım arasındaki optimizasyonu öğretiyor.",
        "stim_threshold_map",
        "fig_8_19_costimulation.png",
        "Şekil 8.19 — yüksek akım ve komşu sinir katkısı",
        "Preston & Shapiro, Bölüm 8, s. 88–90; Box 8.5",
        "",
        [
            C("offset", "Stimülatörün hedeften sapması", -20, 20, 1, 0, "mm"),
            C("current", "Uyarım akımı", 20, 80, 1, 35, "mA"),
        ],
        [
            ["Seçici pencere", [0, 42]],
            ["Hedef üzerinde düşük akım", [0, 32]],
            ["Sapmış + yüksek akım", [16, 65]],
        ],
        "Hedef sinir üzerindeki en düşük eşik noktası bulunmalı; kötü konumu daha yüksek akımla telafi etmek ko-stimülasyon riskini büyütür.",
    ),
    "motor-elektrot-yerlesimi/animasyon-2-g2-tendon-potansiyeli.html": S(
        "Sağ ve solda farklı G2 konumu yalancı amplitüd asimetrisi üretir",
        "G1−G2 mekanizmasından sonra bu sayfa karşılaştırmalı çalışmadaki klinik sonucu gösterir.",
        "g2_side_asymmetry",
        "fig_8_24_g1_g2.png",
        "Şekil 8.24 — tendon G2 katkısı nihai BKAP morfolojisini değiştirir",
        "Preston & Shapiro, Bölüm 8, s. 90–92",
        "https://pubmed.ncbi.nlm.nih.gov/31794957/",
        [
            C("left", "Sol G2 katkısı", 0, 100, 1, 25, "%"),
            C("right", "Sağ G2 katkısı", 0, 100, 1, 75, "%"),
        ],
        [
            ["Sağ G2 yüksek", [25, 75]],
            ["Simetrik G2", [25, 25]],
            ["Sol G2 yüksek", [75, 25]],
        ],
        "Yan karşılaştırmasında yalnız G1 motor noktası değil, G2'nin anatomik konumu ve elektriksel katkısı da simetrik olmalıdır.",
    ),
    "antidromik-ortodromik/animasyon-1-antidromik-vs-ortodromik.html": S(
        "Antidromik mi ortodromik mi? Seçim yalnız amplitüd seçimi değildir",
        "İki tekniğin sinyal-gürültü oranı, motor kontaminasyon riski ve latans karşılaştırması aynı ekranda değerlendirilir.",
        "technique_choice",
        "fig_8_26_anti_ortho.png",
        "Şekil 8.26 — aynı mesafede antidromik ve ortodromik kayıt",
        "Preston & Shapiro, Bölüm 8, s. 92–93",
        "https://pubmed.ncbi.nlm.nih.gov/2369294/",
        [
            C("depth", "Doku/ödem etkisi", 0, 100, 1, 10, "%"),
            C("motor", "Motor kontaminasyon riski", 0, 100, 1, 20, "%"),
        ],
        [
            ["Rutin karşılaştırma", [10, 20]],
            ["Derin/ödemli doku", [80, 20]],
            ["Yüksek motor risk", [10, 90]],
        ],
        "Antidromik kayıt genellikle daha büyük yanıt verir; ancak geç motor bileşen riski varsa ortodromik doğrulama tanısal değer kazanır.",
    ),
    "elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html": S(
        "Derinlik onseti, peak latansı ve amplitüdü aynı yönde değiştirmez",
        "Doku filtresi mekanizmasından sonra burada hangi ölçütün ne kadar güvenilir kaldığı sınanır.",
        "depth_metric_overlay",
        "fig_8_28_depth_edema.png",
        "Şekil 8.28 — doku mesafesi amplitüdü azaltır ve dalgayı genişletir",
        "Preston & Shapiro, Bölüm 8, s. 93–94",
        "https://pubmed.ncbi.nlm.nih.gov/10627934/",
        [
            C("depth", "Ek doku mesafesi", 0, 20, 0.5, 15, "mm"),
            C("metric", "İmleç: 0 onset / 1 peak", 0, 1, 1, 0, ""),
        ],
        [
            ["Derin + onset", [15, 0]],
            ["Derin + peak", [15, 1]],
            ["Yüzeyel referans", [0, 0]],
        ],
        "Derinlik amplitüd ve peak latansı belirgin değiştirirken onset daha az etkilenebilir; hangi latansın ölçüldüğü açıkça belirtilmelidir.",
    ),
    "aktif-referans-mesafesi/animasyon-1-g1-g2-mesafesi.html": S(
        "G1–G2 çok yakınsa aynı potansiyel iki elektrotta birden görülür ve iptal olur",
        "Bu sayfa G2'nin anatomik yerinden farklı olarak interelektrot mesafesinin zamansal iptalini gösterir.",
        "g1g2_distance_cancel",
        "fig_8_31_g1_g2_distance.png",
        "Şekil 8.31 — interelektrot mesafesi dalga biçimi ve amplitüdü değiştirir",
        "Preston & Shapiro, Bölüm 8, s. 94–95",
        "https://pubmed.ncbi.nlm.nih.gov/2311573/",
        [
            C("distance", "G1–G2 mesafesi", 1, 5, 0.1, 3.5, "cm"),
            C("velocity", "Duyusal iletim hızı", 40, 70, 1, 55, "m/s"),
        ],
        [
            ["Çok yakın 1 cm", [1, 55]],
            ["Önerilen 3.5 cm", [3.5, 55]],
            ["Yavaş iletim 3.5 cm", [3.5, 42]],
        ],
        "Duysal çalışmalarda G1–G2 yaklaşık 3–4 cm tutulur; daha kısa mesafe aynı potansiyelin iki girişte örtüşüp iptal olmasına yol açar.",
    ),
}


EXTRA_SCRIPT = r"""
function drawCmrThree(W,H,v){
  const common=v[0]/100,mis=v[1]/100,x=22,w=W-44,hh=(H-112)/3;
  const n=t=>common*.42*Math.sin(2*Math.PI*(7*t+phase));
  scope(x,52,w,hh,t=>n(t)+.52*snap(t,1,.62,1,0),"#ffc05c","G1 · hedef sinyal + ortak gürültü");
  scope(x,60+hh,w,hh,t=>n(t)*(1-mis*.72),"#75b8ff","G2 · ortak gürültü");
  scope(x,68+2*hh,w,hh,t=>.52*snap(t,1,.62,1,0)+n(t)*mis*.72,"#79e3ac","ÇIKIŞ · G1 − G2");
  const residual=Math.round(common*mis*72);
  readout.innerHTML=`<strong>KALAN 50/60 Hz ${residual}%</strong>Giriş eşleşme hatası ${Math.round(mis*100)}%`;
  note.textContent=residual<8?"G1 ve G2 ortak gürültüyü benzer gördü; çıkarma sonrası hedef potansiyel korunuyor.":"Ortak gürültü iki girişte eşit değil; çıkışta artık ortak mod değil, diferansiyel hata olarak büyütülüyor.";
}
function drawNoiseFault(W,H,v){
  const contact=v[0]/100,cable=v[1]/100,x=22,w=W-44,hh=(H-105)/2;
  const dropout=t=>cable*(gauss(t,.22,.008)-.8*gauss(t,.225,.018)+1.2*gauss(t,.71,.006)-gauss(t,.72,.02));
  scope(x,55,w,hh,t=>.55*snap(t,1,.55,1,.05)+contact*.46*Math.sin(2*Math.PI*(7*t+phase))+dropout(t),"#79e3ac","CANLI KAYIT");
  scope(x,63+hh,w,hh,t=>.55*snap(t,1,.55,1,.05),"#ffc05c","AYNI YANIT · teknik hata giderildi",[7,5]);
  const dx=cable>.45?"KABLO / KONNEKTÖR":contact>.45?"EMPEDANS / ORTAK MOD":"KAYIT UYGUN";
  readout.innerHTML=`<strong>${dx}</strong>${cable>.45?"Aralıklı sıçrama ve kesilme":contact>.45?"Düzenli 50/60 Hz bileşeni":"Stabil bazal ve yanıt"}`;
  note.textContent=cable>.45?"Ani, keskin ve pozisyona bağlı geçiciler yıpranmış kablo veya gevşek bağlantıyı düşündürür.":contact>.45?"Sürekli periyodik gürültüde elektrot empedansı, deri teması, toprak ve ortak mod eşleşmesi kontrol edilir.":"Bazal stabil; teknik müdahale gerektiren belirgin örüntü yok.";
}
function drawRecordingPreset(W,H,v){
  const sensory=v[0]>.5,chosenSens=v[1]>.5,x=22,w=W-44,hh=(H-105)/2;
  const raw=t=>sensory?snap(t,1,.38,.78,.18):cmap(t,1,.31,1.15,0);
  const factor=sensory?(chosenSens?1:.72):(chosenSens?.88:1);
  const wide=sensory&&!chosenSens?1.35:(!sensory&&chosenSens?1.12:1);
  scope(x,55,w,hh,t=>raw(t),"#ffc05c",`${sensory?"DUYSAL":"MOTOR"} HAM REFERANS`,[7,5]);
  scope(x,63+hh,w,hh,t=>factor*(sensory?snap(t,1,.38,wide,.18):cmap(t,1,.31,wide,0)),"#79e3ac",`${chosenSens?"20 Hz–2 kHz DUYSAL":"10 Hz–10 kHz MOTOR"} PRESET`);
  const ok=sensory===chosenSens;
  readout.innerHTML=`<strong>${ok?"UYGUN PRESET":"UYUMSUZ PRESET"}</strong>${sensory?"DSAP":"BKAP"} · amplitüd ${Math.round(factor*100)}%`;
  note.textContent=ok?"Kayıt türü ile preset eşleşiyor; normal değer karşılaştırması teknik olarak tutarlı.":"Yanlış preset hedef sinyalin frekans içeriğini değiştiriyor; oluşan amplitüd/süre farkı patoloji değildir.";
}
function drawArtifactRecovery(W,H,v){
  const art=v[0]/10,rec=v[1],x=22,y=62,w=W-44,h=H-95,on=.36;
  grid(x,y,w,h);const pts=[];for(let i=0;i<=700;i++){const t=i/700;const ms=t*10;let z=art*(2.1*gauss(t,.055,.005)-1.25*gauss(t,.073,.014));if(ms<rec)z+=art*.42*Math.exp(-ms/Math.max(.15,rec));z+=.48*snap(t,1,on,1,0);pts.push([x+w*t,clamp(y+h/2-z*h*.34,y+2,y+h-2)])}line(pts,"#79e3ac",2);
  const deadX=x+w*rec/10;ctx.fillStyle="rgba(180,59,71,.18)";ctx.fillRect(x,y,deadX-x,h);ctx.strokeStyle="#ff6876";ctx.setLineDash([5,4]);ctx.beginPath();ctx.moveTo(deadX,y);ctx.lineTo(deadX,y+h);ctx.stroke();ctx.setLineDash([]);text("amplifikatör toparlanma penceresi",x+10,y+22,"#ff9aa3",11);
  const hidden=rec>3.1;
  readout.innerHTML=`<strong>${hidden?"ONSET ÖRTÜLDÜ":"YANIT ÖLÇÜLEBİLİR"}</strong>Toparlanma ${rec.toFixed(1)} ms · gerçek onset 3.6 ms`;
  note.textContent=hidden?"Bazal yanıt başlamadan dönmedi; latans ve amplitüd imleçleri artefakt kuyruğuna yerleşebilir.":"Artefakt sonrası bazal gerçek yanıt başlamadan önce toparlandı; ölçüm penceresi korunuyor.";
}
function drawPolarityCv(W,H,v){
  const d=v[0]>.5,p=v[1]>.5,dl=3.2+(d?.35:0),pl=6.7+(p?.35:0),x=22,w=W-44,hh=(H-110)/2,cv=200/(pl-dl);
  scope(x,55,w,hh,t=>cmap(t,1,.18+dl*.022,1,0),"#79e3ac",`DİSTAL · ${dl.toFixed(2)} ms · ${d?"TERS":"DOĞRU"} POLARİTE`);
  scope(x,63+hh,w,hh,t=>cmap(t,1,.18+pl*.022,1,0),"#75b8ff",`PROKSİMAL · ${pl.toFixed(2)} ms · ${p?"TERS":"DOĞRU"} POLARİTE`);
  readout.innerHTML=`<strong>${cv.toFixed(1)} m/s</strong>20 cm / ${(pl-dl).toFixed(2)} ms`;
  note.textContent=d===p?"İki noktadaki gecikme benzer olduğu için segment hızı görece korunabilir; fakat mutlak latans ve katot mesafesi yine hatalıdır.":"Yalnız bir uyarım noktasında yaklaşık 0.35 ms ek gecikme latans farkını değiştirerek segment hızını yalancı bozar.";
}
function drawPlateauProtocol(W,H,v){
  const cur=v[0],vari=v[1]/100,x=55,y=62,w=W-105,h=H-210,amp=interpTable(cur)[0];
  grid(x,y,w,h,12,5);const pts=[];for(let i=0;i<=120;i++){const c=6+12*i/120,a=interpTable(c)[0];pts.push([x+w*(c-6)/12,y+h-a/12*h*.84])}line(pts,"#79e3ac",3);
  ctx.fillStyle="rgba(47,125,82,.17)";ctx.fillRect(x+w*5/12,y,w*3/12,h);text("PLATO BÖLGESİ",x+w*6.5/12,y+22,"#79e3ac",11,"center",800);
  const mx=x+w*(cur-6)/12,my=y+h-amp/12*h*.84;ctx.fillStyle="#ffc05c";ctx.beginPath();ctx.arc(mx,my,7,0,Math.PI*2);ctx.fill();
  scope(22,H-128,W-44,96,t=>(amp/10.5)*(1+vari*pseudo(t*3))*cmap(t,1,.29,1,0),"#ffc05c","SEÇİLEN AKIMDA TEKRAR KAYDI");
  const status=cur<11?"REKRUTMAN SÜRÜYOR":cur<13.75?"PLATO GÖRÜLDÜ":"SUPRAMAKSİMAL DOĞRULANDI";
  readout.innerHTML=`<strong>${status}</strong>${cur.toFixed(1)} mA · ${amp.toFixed(1)} mV · tekrar değişkenliği ${Math.round(vari*100)}%`;
  note.textContent=cur<11?"Bir sonraki akım artışında amplitüd hâlâ büyüyor; bu nokta supramaksimal değildir.":cur<13.75?"İlk plato görüldü; yaklaşık %25 ek akım ve tekrar kaydıyla kararlılık doğrulanmalı.":"Plato üzerinde ek akım amplitüdü büyütmedi ve tekrarlar kararlı: teknik supramaksimal uyarım kanıtlandı.";
}
function drawCostimFour(W,H,v){
  const d=v[0]/100,p=v[1]/100,x=22,w=W-44,hh=(H-135)/4,base=.62;
  const rows=[["DİSTAL APB",base+d*.38,"#79e3ac"],["DİSTAL ADM",d*.72,"#75b8ff"],["PROKSİMAL APB",base+p*.38,"#79e3ac"],["PROKSİMAL ADM",p*.72,"#75b8ff"]];
  rows.forEach((r,i)=>scope(x,48+i*(hh+6),w,hh,t=>r[1]*cmap(t,1,.28+(i>1?.05:0),1,0),r[2],r[0]));
  const apparent=(base+p*.38)/(base+d*.38)*100;
  const dx=d>.25&&p<.25?"YALANCI PROKSİMAL DÜŞÜŞ":p>.25&&d<.25?"GERÇEK BLOK GİZLENEBİLİR":d>.25&&p>.25?"İKİ NOKTADA KO-STİM":"SEÇİCİ KAYIT";
  readout.innerHTML=`<strong>${dx}</strong>Proksimal/distal APB ${apparent.toFixed(0)}%`;
  note.textContent=(d>.25||p>.25)?"ADM kanalındaki eşzamanlı yanıt komşu ulnar katkısını kanıtlıyor; yalnız APB amplitüd oranıyla tanı konmamalı.":"Hedef APB yanıtları karşılaştırılabilir ve komşu ADM kanalları sessiz.";
}
function drawThresholdMap(W,H,v){
  const off=v[0],cur=v[1],targetThr=28+Math.abs(off)*.75,adjThr=52-Math.max(0,off)*.7,tar=clamp((cur-targetThr)/18,0,1),adj=clamp((cur-adjThr)/18,0,1);
  const cx=W*.45,px=cx+off*12;line([[55,112],[W-55,112]],"#d9b15f",8);line([[55,165],[W-55,165]],"#75b8ff",8);text("HEDEF MEDİAN",70,95,"#ffc05c",12);text("KOMŞU ULNAR",70,192,"#75b8ff",12);
  ctx.fillStyle="#eef6f4";ctx.beginPath();ctx.arc(px,55,18,0,Math.PI*2);ctx.fill();line([[px,73],[px,112]],"#ff6876",3);text(`${off>0?"+":""}${off} mm`,px,30,"#fff",12,"center",800);
  scope(22,220,W-44,(H-250)/2,t=>tar*cmap(t,1,.3,1,0),"#79e3ac",`APB · eşik ${targetThr.toFixed(0)} mA`);
  scope(22,228+(H-250)/2,W-44,(H-250)/2,t=>adj*cmap(t,1,.34,1,0),"#75b8ff",`ADM · eşik ${adjThr.toFixed(0)} mA`);
  const safe=tar>.75&&adj<.15;
  readout.innerHTML=`<strong>${safe?"SEÇİCİ PENCERE":"OPTİMAL DEĞİL"}</strong>APB ${Math.round(tar*100)}% · ADM ${Math.round(adj*100)}%`;
  note.textContent=Math.abs(off)>10?"Hedeften sapma median eşiğini yükseltti; daha fazla akım komşu ulnar siniri de devreye sokuyor.":cur<targetThr?"Konum uygun olabilir, fakat hedef sinir eşiğine henüz ulaşılmadı.":safe?"Hedef sinirde yüksek yanıt, komşu kasta sessizlik ve düşük gerekli akım birlikte seçiciliği destekliyor.":"Akım komşu sinir eşiğine yaklaştı; konumu yeniden ara.";
}
function drawG2Asymmetry(W,H,v){
  const l=v[0]/100,r=v[1]/100,x=22,w=W-44,hh=(H-110)/2;
  const wave=(t,g)=>cmap(t,1,.27,1,0)-g*(.55*gauss(t,.34,.05)-.42*gauss(t,.45,.07));
  scope(x,55,w,hh,t=>wave(t,l),"#79e3ac",`SOL BKAP · G2 katkısı ${Math.round(l*100)}%`);
  scope(x,63+hh,w,hh,t=>wave(t,r),"#75b8ff",`SAĞ BKAP · G2 katkısı ${Math.round(r*100)}%`);
  const la=10+4*l,ra=10+4*r,diff=Math.abs(la-ra)/Math.max(la,ra)*100;
  readout.innerHTML=`<strong>YALANCI ASİMETRİ ${diff.toFixed(0)}%</strong>Sol ${la.toFixed(1)} mV · sağ ${ra.toFixed(1)} mV`;
  note.textContent=diff<8?"G2 katkıları simetrik; yan amplitüd karşılaştırması kayıt geometrisi açısından tutarlı.":"G1 yanıtları aynı olmasına rağmen farklı G2 katkısı nihai G1−G2 amplitüdlerini ayırdı; bu akson kaybı değildir.";
}
function drawTechniqueChoice(W,H,v){
  const depth=v[0]/100,motor=v[1]/100,x=22,w=W-44,hh=(H-110)/2,antiAmp=1-.35*depth,orthoAmp=.58*(1-.22*depth);
  scope(x,55,w,hh,t=>antiAmp*snap(t,1,.3,1,.15)+motor*.48*cmap(t,1,.62,1.1,0),"#79e3ac","ANTİDROMİK · yüksek amplitüd + motor kontaminasyon olasılığı");
  scope(x,63+hh,w,hh,t=>orthoAmp*snap(t,1,.3,1.08,.10),"#75b8ff","ORTODROMİK · düşük amplitüd + motor bileşenden uzak");
  const choose=motor>.55?"ORTODROMİK DOĞRULAMA":depth>.65?"ANTİDROMİK SNR AVANTAJI":"İKİ TEKNİK TUTARLI";
  readout.innerHTML=`<strong>${choose}</strong>Antidromik/ortodromik amplitüd oranı ${(antiAmp/orthoAmp).toFixed(1)}×`;
  note.textContent=motor>.55?"Geç motor bileşen antidromik kaydı belirsizleştiriyor; ortodromik kayıt duysal yanıtın varlığını doğrulayabilir.":depth>.65?"Doku atenüasyonu küçük ortodromik yanıtı daha kırılgan yapıyor; antidromik kayıt daha yüksek SNR sağlar.":"Aynı mesafede yön değişse de temel iletim süresi değişmez; amplitüd farkı teknik geometriden kaynaklanır.";
}
function drawDepthMetric(W,H,v){
  const depth=v[0],peak=v[1]>.5,att=Math.exp(-depth/16),wide=1+depth/25,on=.34-depth*.0013,x=22,y=62,w=W-44,h=H-95;
  grid(x,y,w,h);const ref=[],cur=[];for(let i=0;i<=700;i++){const t=i/700;ref.push([x+w*t,y+h/2-snap(t,1,.34,1,.15)*h*.32]);cur.push([x+w*t,y+h/2-att*snap(t,1,on,wide,.15)*h*.32])}line(ref,"#ffc05c",2,[7,5]);line(cur,"#79e3ac",2);
  const cursorT=peak?on:on-.025,xx=x+w*cursorT;ctx.strokeStyle=peak?"#75b8ff":"#48d7e8";ctx.setLineDash([6,4]);ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke();ctx.setLineDash([]);text(peak?"PEAK İMLECİ":"ONSET İMLECİ",xx+6,y+22,peak?"#75b8ff":"#48d7e8",11);
  const onsetMs=2.2-depth*.006,peakMs=2.6+depth*.026;
  readout.innerHTML=`<strong>${peak?peakMs.toFixed(2):onsetMs.toFixed(2)} ms</strong>${peak?"Peak":"Onset"} · amplitüd ${Math.round(38*att)} µV`;
  note.textContent=depth>10?"Derinlik yanıtı küçültüp genişletti: peak sağa kayarken onset yalnız hafif sola kaydı. Aynı latans ölçütü kullanılmadan karşılaştırma yapılamaz.":"Yüzeyel kayıtta amplitüd, onset ve peak referans morfolojiye yakındır.";
}
function drawG1G2Distance(W,H,v){
  const dist=v[0],vel=v[1],delay=(dist/vel)*10,shift=.05+delay*.055,x=22,w=W-44,hh=(H-112)/3,cancel=clamp(1-dist/4.2,0,1);
  scope(x,52,w,hh,t=>snap(t,1,.33,1,.12),"#ffc05c","G1 POTANSİYELİ");
  scope(x,60+hh,w,hh,t=>.82*snap(t,1,.33+shift,1,.12),"#75b8ff",`G2 POTANSİYELİ · ${delay.toFixed(2)} ms sonra`);
  scope(x,68+2*hh,w,hh,t=>snap(t,1,.33,1,.12)-.82*snap(t,1,.33+shift,1,.12),"#79e3ac","KAYIT · G1 − G2");
  readout.innerHTML=`<strong>İPTAL ${Math.round(cancel*100)}%</strong>G1–G2 ${dist.toFixed(1)} cm · zaman farkı ${delay.toFixed(2)} ms`;
  note.textContent=dist<2?"G1 ve G2 aynı potansiyeli zamansal olarak örtüşen biçimde gördü; çıkarma gerçek DSAP'ın bir bölümünü iptal etti.":"3–4 cm aralık zamansal ayrımı artırdı; G2 katkısı hedef yanıtla daha az örtüşüyor.";
}
"""


SWITCH_INSERT = (
    'case"caliper":drawCaliper(W,H,v);break;'
    'case"cmr_three_trace":drawCmrThree(W,H,v);break;'
    'case"noise_fault_bench":drawNoiseFault(W,H,v);break;'
    'case"recording_preset":drawRecordingPreset(W,H,v);break;'
    'case"artifact_recovery":drawArtifactRecovery(W,H,v);break;'
    'case"polarity_cv_case":drawPolarityCv(W,H,v);break;'
    'case"plateau_protocol":drawPlateauProtocol(W,H,v);break;'
    'case"costim_four_channel":drawCostimFour(W,H,v);break;'
    'case"stim_threshold_map":drawThresholdMap(W,H,v);break;'
    'case"g2_side_asymmetry":drawG2Asymmetry(W,H,v);break;'
    'case"technique_choice":drawTechniqueChoice(W,H,v);break;'
    'case"depth_metric_overlay":drawDepthMetric(W,H,v);break;'
    'case"g1g2_distance_cancel":drawG1G2Distance(W,H,v);break;'
)


def prepare_v4() -> None:
    v3.LABS.update(REFINED)
    v3.LAB_SCRIPT = v3.LAB_SCRIPT.replace(
        "function draw(now){", EXTRA_SCRIPT + "\nfunction draw(now){", 1
    )
    v3.LAB_SCRIPT = v3.LAB_SCRIPT.replace(
        'case"caliper":drawCaliper(W,H,v);break;', SWITCH_INSERT, 1
    )


def update_index_v4() -> None:
    path = v3.LIVE / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\s*<!-- nonphys-status-v3 -->.*?<!-- /nonphys-status-v3 -->\s*",
        "\n",
        text,
        flags=re.S,
    )
    banner = """<!-- nonphys-status-v4 -->
<aside style="position:fixed;right:18px;bottom:18px;z-index:999;max-width:560px;padding:12px 15px;background:#fff;color:#16232c;border:1px solid #c3ceda;border-left:4px solid #2f7d52;box-shadow:0 10px 28px rgba(20,33,43,.18);font:650 13px/1.35 'Segoe UI',Arial,sans-serif">
Nonfizyolojik faktörler: ayrıntılı açıklamalar + <b style="color:#2f7d52">yalnız serbest laboratuvar</b>. Örtüşen eski animasyonlar farklı klinik sorulara göre yeniden tasarlandı; standart F1/F2/F3 akışı korundu.
</aside>
<!-- /nonphys-status-v4 -->"""
    text = re.sub(
        r"\s*<!-- nonphys-status-v4 -->.*?<!-- /nonphys-status-v4 -->\s*",
        "\n",
        text,
        flags=re.S,
    )
    text = text.replace("</body>", banner + "\n</body>", 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    prepare_v4()
    backup = v3.ROOT / "animations_ncs_emg_codex_backup_20260729_before_overlap_refinement_v4"
    if not backup.exists():
        shutil.copytree(v3.LIVE, backup)

    v3.restore_old_pages()
    v3.deploy_assets()
    previous_before = "proksimal-distal/animasyon-1-segment-hizi.html"
    for i, rel in enumerate(v3.CHAIN):
        prev_rel = previous_before if i == 0 else v3.CHAIN[i - 1]
        next_rel = "index.html" if i == len(v3.CHAIN) - 1 else v3.CHAIN[i + 1]
        if rel in v3.LABS:
            (v3.LIVE / rel).write_text(
                v3.lab_html(rel, v3.LABS[rel], prev_rel, next_rel),
                encoding="utf-8",
            )
        elif rel == "stimulus-artefakti/animasyon-0-mekanizma.html":
            v3.patch_stimulus_lab(rel, prev_rel, next_rel)
        else:
            path = v3.LIVE / rel
            text = path.read_text(encoding="utf-8")
            text = v3.patch_standard_nav(text, rel, prev_rel, next_rel)
            path.write_text(text, encoding="utf-8")

    predecessor = v3.LIVE / previous_before
    if predecessor.exists():
        text = predecessor.read_text(encoding="utf-8")
        text = v3.patch_standard_nav(
            text, previous_before, "proksimal-distal/index.html", v3.CHAIN[0]
        )
        predecessor.write_text(text, encoding="utf-8")

    v3.update_index()
    update_index_v4()
    report = v3.validate()
    report["redesigned_older_labs"] = len(REFINED)
    report["distinct_animation_jobs"] = len(
        {
            data["kind"]
            for data in v3.LABS.values()
        }
    ) + (len(v3.EXISTING - set(REFINED)) + 1)
    report["overlap_solution"] = {
        "filters": [
            "frequency spectrum",
            "recording-type preset selection",
            "waveform distortion",
        ],
        "polarity": ["activation mechanism", "paired-site latency/CV error"],
        "supramaximal": [
            "graded recruitment waterfall",
            "plateau proof protocol",
            "false diagnostic amplitude pattern",
        ],
        "costimulation": [
            "dual-channel detection",
            "distal/proximal diagnostic error",
            "minimum-threshold prevention",
        ],
        "motor_recording": [
            "G1−G2 construction",
            "G1 motor point",
            "side-to-side G2 asymmetry",
        ],
        "electrode_geometry": [
            "tissue filtering",
            "onset-vs-peak metric choice",
            "electrode search",
            "false conduction velocity",
            "G1–G2 temporal cancellation",
        ],
    }
    (v3.LIVE / "nonfizyolojik_v4_qa.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (v3.LIVE / "nonfizyolojik_animasyon_gorev_matrisi_v4.json").write_text(
        json.dumps(
            {
                rel: {
                    "title": data["title"],
                    "teaching_job": data["kind"],
                    "source": data["source"],
                    "pubmed": data["pubmed"],
                }
                for rel, data in sorted(v3.LABS.items())
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=True, indent=2))
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
        raise RuntimeError("V4 structural validation failed.")


if __name__ == "__main__":
    main()
