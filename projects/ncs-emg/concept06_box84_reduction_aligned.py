from pathlib import Path
import shutil


LIVE = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\presentations"
    r"\artifacts_of_ncs_emg\animations"
)
WORK = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg")
target = LIVE / "stimulus-artefakti" / "animasyon-2-artefakt-azaltma.html"
figure_target = LIVE / "figures" / "source-v3" / "box_8_4_reduce_stimulus_artifact.png"

html = r"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Box 8.4 — Stimulus Artefaktını Sistematik Azaltma</title>
<style>
:root{
  --bg:#eef1f4;--panel:#fff;--head:#e7edf3;--line:#d7dee5;--line2:#c3ceda;
  --ink:#16232c;--muted:#5c6b78;--cyan:#0f7a95;--green:#2f7d52;
  --amber:#d89a38;--red:#bd4250;--scope:#061a13;
}
*{box-sizing:border-box}
html,body{width:100%;height:100%;margin:0;background:#ccd4da;color:var(--ink);
  font-family:"Segoe UI",Inter,Arial,sans-serif}
body{display:grid;place-items:center;padding:14px}
.app{width:min(100vw - 28px,1500px);aspect-ratio:16/9;max-height:calc(100vh - 28px);
  background:var(--bg);border:1px solid #c7d0d8;border-radius:6px;
  box-shadow:0 24px 60px rgba(20,33,43,.25);display:grid;
  grid-template-rows:40px 50px 1fr 56px;overflow:hidden}
.titlebar{display:flex;align-items:center;justify-content:space-between;padding:0 18px;
  background:linear-gradient(180deg,#fff,#eef1f4);border-bottom:1px solid var(--line);
  font-size:16px;color:#45525c}
.tb-left{display:flex;align-items:center;gap:10px;font-weight:600}.dot{width:10px;height:10px;border-radius:50%;
  background:var(--green);box-shadow:0 0 6px rgba(47,125,82,.5)}
.tb-right{display:flex;gap:18px;font-weight:800;letter-spacing:.12em;color:#7c8894;font-size:15px}.tb-right b{color:var(--cyan)}
.toolbar{display:flex;align-items:center;gap:24px;padding:0 18px;background:var(--head);border-bottom:1px solid var(--line)}
.tf{display:flex;align-items:baseline;gap:9px}.tf label{font-size:13px;color:var(--muted);font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.tf strong{font-size:15px;color:var(--ink);font-weight:800}.toolbar .claim{margin-left:auto;color:var(--green);font-size:12px;font-weight:900}
.workspace{min-height:0;padding:12px;display:grid;grid-template-columns:410px minmax(0,1fr);gap:12px}
.panel{min-width:0;min-height:0;background:#fff;border:1px solid var(--line);display:flex;flex-direction:column;overflow:hidden}
.panel-head{height:38px;flex:none;display:flex;align-items:center;justify-content:space-between;gap:8px;padding:0 12px;
  background:var(--head);border-bottom:1px solid var(--line);font-size:13px;font-weight:800;
  letter-spacing:.04em;text-transform:uppercase;color:#465762}
.head-actions{display:flex;gap:5px}.head-actions button{min-height:25px;padding:0 8px;font-size:10.5px}
.checklist{flex:1;min-height:0;padding:8px;display:grid;grid-template-rows:repeat(8,1fr);gap:5px}
.item{display:flex;align-items:center;gap:8px;padding:6px 8px;background:#f3f6f8;border:1px solid var(--line);
  cursor:pointer;user-select:none;min-height:0}
.item:hover{border-color:var(--cyan)}.item input{width:17px;height:17px;accent-color:var(--green);flex:none}
.item .num{width:20px;height:20px;display:grid;place-items:center;border-radius:50%;background:#dfe7ed;color:#43525d;
  font-size:11px;font-weight:900;flex:none}.item .txt{font-size:12.2px;font-weight:650;line-height:1.22}
.item .txt b{color:#075f74}.item.on{background:#e9f5ee;border-color:#b8ddc6}.item.on .num{background:var(--green);color:#fff}
.right{min-width:0;min-height:0;display:grid;grid-template-rows:1fr 50px}
.stage{min-height:0;display:grid;grid-template-columns:minmax(0,1fr) 250px}
.scope{position:relative;min-width:0;min-height:0;background:var(--scope)}
canvas{display:block;width:100%;height:100%}
.scope-meta{position:absolute;left:12px;right:12px;top:9px;display:flex;justify-content:space-between;
  color:#a7c0b7;font-size:11px;font-weight:800;letter-spacing:.04em;pointer-events:none}
.scope-meta b{color:#e9f7f1;font-size:13px}.legend{position:absolute;right:12px;bottom:8px;display:flex;gap:12px;color:#9cb2aa;font-size:10px}
.legend span::before{content:"";display:inline-block;width:20px;margin-right:5px;vertical-align:middle;border-top:2px solid #64eda0}
.legend .true::before{border-color:#d89a38;border-style:dashed}
.inspector{min-height:0;padding:8px;background:#fff;border-left:1px solid var(--line);display:grid;gap:7px;align-content:start;overflow:auto}
.note{padding:8px;background:#f3f6f8;border:1px solid var(--line);font-size:11.5px;line-height:1.3;font-weight:600}.note b{color:var(--cyan)}
.meters{display:grid;gap:6px}.meter-row{display:grid;grid-template-columns:1fr 42px;gap:5px;align-items:center}
.meter-row label{grid-column:1/-1;font-size:10.5px;color:var(--muted);font-weight:800}
.track{height:8px;background:#e1e7eb;border-radius:5px;overflow:hidden}.fill{height:100%;background:var(--red);transition:width .22s}
.meter-row output{font-size:11px;font-weight:900;text-align:right}.book{display:grid;grid-template-columns:78px 1fr;gap:7px;align-items:center;
  padding:6px;border:1px solid var(--line)}.book img{width:78px;height:54px;object-fit:contain}.book b{font-size:10.5px;line-height:1.18}
.book span{display:block;margin-top:2px;font-size:9.5px;line-height:1.18;color:var(--muted)}
.source{font-size:9.5px;line-height:1.2;color:#687784}
.statusbar{display:flex;align-items:center;gap:10px;padding:0 14px;background:var(--head);border-top:1px solid var(--line)}
.statusbar span{font-size:11px;color:var(--muted);font-weight:800;text-transform:uppercase}.statusbar b{font-size:14px}
.progress{flex:1;height:12px;border-radius:7px;background:linear-gradient(90deg,#e6f7ec,#fbf0de 55%,#fbe6e7);
  border:1px solid var(--line2);overflow:hidden}.progress-fill{height:100%;background:rgba(189,66,80,.34);width:100%;transition:width .22s}
button{appearance:none;border:1px solid var(--line2);background:#fff;color:var(--ink);border-radius:4px;
  min-height:30px;padding:0 10px;font:800 11.5px "Segoe UI",Arial,sans-serif;cursor:pointer}
button:hover,button:focus-visible{border-color:var(--cyan);outline:none}
.bottom-bar{height:56px;display:flex;align-items:stretch;gap:1px;background:#d5dde4;border-top:1px solid #d5dde4}
.fkey{flex:1;background:var(--head);color:var(--ink);text-decoration:none;display:flex;align-items:center;
  justify-content:center;gap:9px;font:800 13px/1 "Segoe UI",Arial,sans-serif}
.fkey span{color:var(--cyan);font-size:15px}.fkey:hover{background:#dce8f0}
@media(max-width:980px){body{padding:0}.app{width:100vw;min-height:100vh;max-height:none;aspect-ratio:auto;border-radius:0}
  .workspace{grid-template-columns:1fr}.panel:first-child{display:none}.stage{grid-template-columns:1fr}.inspector{display:none}}
</style>
</head>
<body>
<div class="app">
  <div class="titlebar">
    <div class="tb-left"><span class="dot"></span>EDX Öğrenim İstasyonu — Bölüm 8 Oturumu</div>
    <div class="tb-right"><b>EDX</b><span>SİM</span></div>
  </div>
  <div class="toolbar">
    <div class="tf"><label>Konu</label><strong>Stimulus Artefaktını Azaltma</strong></div>
    <div class="tf"><label>Kaynak</label><strong>Box 8.4 — kitap sırası</strong></div>
    <div class="claim">Aynı DSAP · yalnız teknik kirlenme azalır</div>
  </div>

  <div class="workspace">
    <section class="panel">
      <div class="panel-head"><span>Box 8.4 kontrol listesi</span>
        <div class="head-actions"><button id="allBtn" type="button">Tümünü uygula</button><button id="resetBtn" type="button">Sıfırla</button></div></div>
      <div class="checklist" id="checklist">
        <label class="item" data-fix="ground"><input type="checkbox"><span class="num">1</span><span class="txt">Toprağı stimülatör ile kayıt elektrotları <b>arasına</b> yerleştir.</span></label>
        <label class="item" data-fix="impedance"><input type="checkbox"><span class="num">2</span><span class="txt">Kayıt elektrotları arasındaki <b>empedans uyumsuzluğunu</b> azalt.</span></label>
        <label class="item" data-fix="coax"><input type="checkbox"><span class="num">3</span><span class="txt"><b>Koaksiyel</b> kayıt kablosu kullan.</span></label>
        <label class="item" data-fix="position"><input type="checkbox"><span class="num">4</span><span class="txt">Stimülatörü sinirin üzerinde <b>optimal</b> konumlandır.</span></label>
        <label class="item" data-fix="intensity"><input type="checkbox"><span class="num">5</span><span class="txt">Supramaksimal yanıtı koruyarak uyarı <b>şiddetini azalt</b>.</span></label>
        <label class="item" data-fix="anode"><input type="checkbox"><span class="num">6</span><span class="txt">Katodu sabit tutup <b>anodu döndür</b>.</span></label>
        <label class="item" data-fix="distance"><input type="checkbox"><span class="num">7</span><span class="txt">Stimülatör–kayıt elektrotları <b>mesafesini artır</b>.</span></label>
        <label class="item" data-fix="cables"><input type="checkbox"><span class="num">8</span><span class="txt">Stimülatör ve kayıt kablolarını <b>çakıştırma</b>.</span></label>
      </div>
    </section>

    <section class="panel right">
      <div class="stage">
        <div class="scope">
          <canvas id="scopeCanvas"></canvas>
          <div class="scope-meta"><span>MEDİAN DSAP · 20 µV/div · 1 ms/div</span><b id="scopeReadout">Başlangıç örtülü</b></div>
          <div class="legend"><span>kaydedilen iz</span><span class="true">gerçek DSAP</span></div>
        </div>
        <aside class="inspector">
          <div class="note" id="stepNote"><b>Başlangıç:</b> Kısa mesafe ve üç kirlenme yolu birlikte DSAP başlangıcını örter.</div>
          <div class="meters">
            <div class="meter-row"><label>Hacim iletilen alan</label><div class="track"><div class="fill" id="volumeFill"></div></div><output id="volumeOut">100%</output></div>
            <div class="meter-row"><label>Diferansiyel/empedans artığı</label><div class="track"><div class="fill" id="diffFill"></div></div><output id="diffOut">100%</output></div>
            <div class="meter-row"><label>Kablo indüksiyonu</label><div class="track"><div class="fill" id="indFill"></div></div><output id="indOut">100%</output></div>
            <div class="meter-row"><label>DSAP–kuyruk ayrımı</label><div class="track"><div class="fill" id="marginFill"></div></div><output id="marginOut">dar</output></div>
          </div>
          <div class="book"><img src="../figures/source-v3/box_8_4_reduce_stimulus_artifact.png" alt="Box 8.4 stimulus artefaktını azaltma yöntemleri">
            <div><b>Box 8.4 — sekiz yöntem aynı klinik hedefe gider</b><span>Anot ve kablo mekanizmaları sonraki sayfalarda ayrıntılıdır.</span></div></div>
          <div class="source">Kaynak: Preston &amp; Shapiro, Box 8.4; McLean ve ark., PMID 8976313.</div>
        </aside>
      </div>
      <div class="statusbar"><span>Artefakt kuyruğu</span><div class="progress"><div class="progress-fill" id="progressFill"></div></div>
        <b id="scoreOut">8/8 eksik</b></div>
    </section>
  </div>

  <nav class="bottom-bar" aria-label="Standart sunum gezinmesi">
    <a class="fkey" href="azaltma-yontemleri.html"><span>F1</span><b>Önceki</b></a>
    <a class="fkey" href="../index.html"><span>F2</span><b>İçindekiler</b></a>
    <a class="fkey" href="anot-dondurme.html"><span>F3</span><b>Sonraki</b></a>
  </nav>
</div>

<script>
const canvas=document.getElementById("scopeCanvas"),ctx=canvas.getContext("2d"),wrap=canvas.parentElement;
const checklist=document.getElementById("checklist"),allBtn=document.getElementById("allBtn"),resetBtn=document.getElementById("resetBtn");
const stepNote=document.getElementById("stepNote"),scoreOut=document.getElementById("scoreOut"),progressFill=document.getElementById("progressFill");
const scopeReadout=document.getElementById("scopeReadout"),fills={volume:volumeFill,diff:diffFill,ind:indFill,margin:marginFill};
const outs={volume:volumeOut,diff:diffOut,ind:indOut,margin:marginOut};
let W=0,H=0,dpr=Math.min(2,devicePixelRatio||1),checked=new Set(),lastFix="";
const notes={
  ground:"<b>1 · Toprak:</b> Stimülatör ile kayıt elektrotları arasındaki toprak, hacim iletilen akımın kayıt girişlerine ulaşan bölümünü azaltır.",
  impedance:"<b>2 · Empedans:</b> G1–G2 empedansları yaklaştıkça ortak artefaktın diferansiyel çıkışta kalan kısmı küçülür.",
  coax:"<b>3 · Koaksiyel kablo:</b> Aktif ve referans iletkenleri birbirine yakın tutar; dış alanın oluşturduğu indüksiyon azalır.",
  position:"<b>4 · Optimal konum:</b> Sinirin üzerinde doğru yerleşim, aynı supramaksimal yanıt için daha az akım gerektirir.",
  intensity:"<b>5 · Şiddet:</b> Yalnız supramaksimal yanıt korunarak azaltılır; submaksimal uyarı teknik çözüm değildir.",
  anode:"<b>6 · Anot rotasyonu:</b> Katot sabit kalır; artefakt geometrisi değişir. Ayrıntılı mekanizma sonraki animasyondadır.",
  distance:"<b>7 · Mesafe:</b> DSAP daha geç gelir; artefakt kuyruğuyla arasındaki ölçüm penceresi genişler.",
  cables:"<b>8 · Kablo ayrımı:</b> Stimülatör ve kayıt kabloları çakışmadığında elektromanyetik kuplaj belirgin azalır."
};
function levels(){
  let volume=100,diff=100,ind=100,current=1,geometry=1,distance=7;
  if(checked.has("ground"))volume*=.62;
  if(checked.has("impedance"))diff*=.35;
  if(checked.has("coax"))ind*=.45;
  if(checked.has("position"))current*=.82;
  if(checked.has("intensity"))current*=.68;
  if(checked.has("anode"))geometry*=.35;
  if(checked.has("distance"))distance=14;
  if(checked.has("cables"))ind*=.25;
  volume*=current;diff*=geometry;ind*=current;
  return{volume,diff,ind,distance,latency:distance/7}
}
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function gauss(t,m,s){const z=(t-m)/s;return Math.exp(-.5*z*z)}
function dsap(t,lat){const u=t-lat;if(u<0)return 0;return 38*(.38*gauss(u,.25,.14)-.78*gauss(u,.70,.24)+.20*gauss(u,1.35,.42))}
function artifact(t,L){
  if(t<0)return 0;const shock=-92*Math.exp(-t/.035)+34*Math.exp(-t/.13);
  const vol=-.23*L.volume*Math.exp(-t/1.20),dif=-.17*L.diff*Math.exp(-t/1.75);
  const ind=.14*L.ind*Math.sin(2*Math.PI*1.7*t+1.1)*Math.exp(-t/1.55);
  return shock+vol+dif+ind
}
function resize(){
  const r=wrap.getBoundingClientRect();W=Math.max(650,Math.round(r.width));H=Math.max(380,Math.round(r.height));
  canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw()
}
new ResizeObserver(resize).observe(wrap);
function line(points,color,width=2,dash=[]){
  ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();
  points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.restore()
}
function txt(s,x,y,color,size=10,weight=700,align="left"){
  ctx.save();ctx.fillStyle=color;ctx.font=`${weight} ${size}px "Segoe UI",Arial,sans-serif`;ctx.textAlign=align;ctx.fillText(s,x,y);ctx.restore()
}
function draw(){
  if(!W||!H)return;const L=levels();ctx.clearRect(0,0,W,H);ctx.fillStyle="#061a13";ctx.fillRect(0,0,W,H);
  const l=28,r=W-18,t=42,b=H-30,mid=(t+b)/2,msX=ms=>l+(r-l)*ms/7,uvY=uv=>mid-uv*(b-t)/155;
  ctx.strokeStyle="#143126";ctx.lineWidth=1;
  for(let i=0;i<=14;i++){const x=l+(r-l)*i/14;ctx.beginPath();ctx.moveTo(x,t);ctx.lineTo(x,b);ctx.stroke()}
  for(let i=0;i<=6;i++){const y=t+(b-t)*i/6;ctx.beginPath();ctx.moveTo(l,y);ctx.lineTo(r,y);ctx.stroke()}
  line([[l,mid],[r,mid]],"#2a4a3b",1);line([[msX(0),t],[msX(0),b]],"#45d5e6",1,[4,4]);txt("t=0",msX(0)+5,t+11,"#69e2ee",10,800);
  const truePts=[],recordedPts=[];for(let i=0;i<=700;i++){const ms=7*i/700,d=dsap(ms,L.latency);
    truePts.push([msX(ms),uvY(d)]);recordedPts.push([msX(ms),uvY(d+artifact(ms,L))])}
  line(truePts,"#d89a38",2,[6,4]);line(recordedPts,"#64eda0",2.5);
  line([[msX(L.latency),t+10],[msX(L.latency),b-8]],"#d89a38",1,[4,4]);txt("gerçek DSAP başlangıcı",msX(L.latency)+5,b-7,"#d89a38",9,800);
  for(let ms=0;ms<=7;ms++)txt(`${ms}`,msX(ms),b+16,"#799087",9,600,ms===0?"left":ms===7?"right":"center")
}
function update(){
  const L=levels(),done=checked.size,remaining=8-done,tail=clamp((L.volume+L.diff+L.ind)/3,0,100);
  fills.volume.style.width=`${L.volume}%`;fills.diff.style.width=`${L.diff}%`;fills.ind.style.width=`${L.ind}%`;
  const margin=L.distance===14?82:24;fills.margin.style.width=`${margin}%`;fills.margin.style.background="var(--green)";
  outs.volume.textContent=`${L.volume.toFixed(0)}%`;outs.diff.textContent=`${L.diff.toFixed(0)}%`;outs.ind.textContent=`${L.ind.toFixed(0)}%`;
  outs.margin.textContent=L.distance===14?"geniş":"dar";scoreOut.textContent=`${remaining}/8 eksik`;progressFill.style.width=`${tail}%`;
  const clean=tail<20&&L.distance===14;scopeReadout.textContent=clean?"DSAP başlangıcı net":tail<45?"Kuyruk azalıyor":"Başlangıç örtülü";
  stepNote.innerHTML=lastFix?notes[lastFix]:"<b>Başlangıç:</b> Kısa mesafe ve üç kirlenme yolu birlikte DSAP başlangıcını örter.";
  draw()
}
checklist.addEventListener("change",e=>{const item=e.target.closest(".item");if(!item)return;lastFix=item.dataset.fix;
  if(e.target.checked){checked.add(lastFix);item.classList.add("on")}else{checked.delete(lastFix);item.classList.remove("on")}update()});
allBtn.addEventListener("click",()=>{checked=new Set([...document.querySelectorAll(".item")].map(x=>x.dataset.fix));lastFix="cables";
  document.querySelectorAll(".item").forEach(x=>{x.classList.add("on");x.querySelector("input").checked=true});update()});
resetBtn.addEventListener("click",()=>{checked.clear();lastFix="";document.querySelectorAll(".item").forEach(x=>{x.classList.remove("on");x.querySelector("input").checked=false});update()});
document.addEventListener("keydown",e=>{if(["INPUT","SELECT","TEXTAREA"].includes(document.activeElement?.tagName))return;
  const k=e.key.toUpperCase(),a=k==="F1"?document.querySelector(".fkey:nth-child(1)"):k==="F2"?document.querySelector(".fkey:nth-child(2)"):k==="F3"?document.querySelector(".fkey:nth-child(3)"):null;
  if(a){e.preventDefault();location.href=a.href}});
resize();update();
</script>
</body>
</html>
"""

target.write_text(html, encoding="utf-8")
figure_target.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(WORK / "box_8_4_reduce_stimulus_artifact.png", figure_target)
print(target)
print(figure_target)
