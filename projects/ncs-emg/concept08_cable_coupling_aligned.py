from pathlib import Path

OUT = Path(r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\10_Projects\presentations\artifacts_of_ncs_emg\animations\stimulus-artefakti\animasyon-3-kablo-induksiyonu.html")

HTML = r'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kablo Kuplajı ve Stimulus Artefaktı — Serbest Laboratuvar</title>
<style>
:root{
  --paper:#f7f8f9;--panel:#fff;--head:#e7edf3;--line:#d5dde4;--ink:#15232d;--muted:#60707d;
  --teal:#0f7a95;--cyan:#36c9d7;--green:#5eea8d;--amber:#ffc857;--red:#eb5a65;--blue:#64a7ff;
  --scope:#06140f;--grid:#143326
}
*{box-sizing:border-box}
html,body{width:100%;height:100%;margin:0;background:#fff;color:var(--ink);font-family:"Segoe UI",Inter,Arial,sans-serif}
body{display:grid;place-items:center;padding:12px}
.app{width:min(calc(100vw - 24px),1500px);aspect-ratio:16/9;max-height:calc(100vh - 24px);background:var(--paper);border:1px solid #c8d1d9;box-shadow:0 18px 48px #23313b24;display:grid;grid-template-rows:42px 48px 1fr 78px 56px;overflow:hidden}
.titlebar,.toolbar{display:flex;align-items:center;padding:0 18px;border-bottom:1px solid var(--line)}
.titlebar{justify-content:space-between;background:linear-gradient(#fff,#f0f3f5);font-size:14px;color:#43515c}
.session{display:flex;align-items:center;gap:9px;font-weight:700}.dot{width:9px;height:9px;border-radius:50%;background:#2f7d52;box-shadow:0 0 7px #2f7d5270}.brand{font-weight:900;letter-spacing:.12em;color:#73808b}.brand b{color:var(--teal)}
.toolbar{gap:20px;background:var(--head)}.label{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:900}.toolbar strong{font-size:15px}.mode{margin-left:auto;color:var(--teal);font-weight:900}
.workspace{min-height:0;padding:10px;display:grid;grid-template-columns:minmax(0,1fr) 326px;gap:10px}
.panel{background:#fff;border:1px solid var(--line);min-width:0;min-height:0;overflow:hidden;display:flex;flex-direction:column}
.panel-head{height:39px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 13px;background:var(--head);border-bottom:1px solid var(--line);font-size:12px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;color:#4a5964}
.state{padding:4px 10px;border-radius:999px;background:#e6f7ec;color:#28744a;border:1px solid #c8e8d3;text-transform:none;letter-spacing:0}.state.warn{background:#fff2dd;color:#965817;border-color:#edd0a2}.state.bad{background:#fde8ea;color:#a6313d;border-color:#f0c3c8}
.lab{flex:1;min-height:0;display:grid;grid-template-rows:44% 56%}
.coupling{position:relative;min-height:0;background:#101d24;border-bottom:4px solid #d5dde4}
#cableCanvas,#scopeCanvas{position:absolute;inset:0;width:100%;height:100%}
.formula{position:absolute;left:12px;bottom:9px;padding:5px 8px;background:#071118e8;border:1px solid #4c626f;color:#d9e7ec;font:800 10px Consolas,monospace}.formula b{color:var(--cyan)}
.scope{position:relative;min-height:0;background:var(--scope)}
.legend{position:absolute;right:12px;top:8px;display:flex;gap:12px;padding:5px 8px;background:#06140fdb;border:1px solid #2b493a;color:#b8c8bf;font-size:11px;font-weight:800}
.key{display:inline-flex;align-items:center;gap:5px}.sw{width:18px;height:3px;background:var(--green)}.sw.true{height:0;border-top:2px dashed var(--amber)}.sw.art{background:var(--cyan)}
.side-body{padding:11px;display:grid;gap:8px;align-content:start;overflow:auto}
.invariant{display:grid;grid-template-columns:1fr auto;gap:4px 9px;padding:9px 10px;border:1px solid #d6e2ea;background:#f2f7fa}.invariant span{font-size:12px;color:var(--muted);font-weight:800}.invariant b{font-size:12px;color:#256744}.lock{font-weight:900}
.meter{padding:9px 10px;border:1px solid var(--line);background:#f5f7f9}.meter-top{display:flex;justify-content:space-between;gap:8px;font-size:12px;font-weight:800;color:var(--muted)}.meter-top b{color:var(--ink);font-variant-numeric:tabular-nums}.track{height:7px;margin-top:6px;background:#dde4e9;border-radius:9px;overflow:hidden}.fill{height:100%;width:0;background:var(--cyan);transition:width .18s}
.readout{display:grid;grid-template-columns:1fr auto;padding:8px 10px;border:1px solid var(--line);font-size:12px}.readout span{color:var(--muted);font-weight:800}.readout b{font-variant-numeric:tabular-nums}
.lesson{padding:9px 10px;border-left:4px solid var(--teal);background:#edf6f8;font-size:12px;line-height:1.35;font-weight:650}.lesson b{color:var(--teal)}
.source{height:92px;border:1px solid var(--line);background:#fff;display:grid;grid-template-columns:112px 1fr;overflow:hidden}.source img{width:100%;height:100%;object-fit:contain;border-right:1px solid var(--line)}.source div{padding:8px;font-size:11px;line-height:1.28;color:var(--muted)}.source b{display:block;color:var(--ink);margin-bottom:3px}
.controls{display:grid;grid-template-columns:230px minmax(190px,1fr) minmax(190px,1fr) auto;align-items:center;gap:14px;padding:9px 16px;background:#fff;border-top:1px solid var(--line)}
.types{display:flex;gap:5px}button{appearance:none;border:1px solid #b8c5cf;background:#f2f5f7;color:var(--ink);font:800 11px "Segoe UI",sans-serif;padding:8px 10px;cursor:pointer;border-radius:3px}button:hover,button:focus-visible{background:#e2edf2;outline:2px solid #8ac4d1;outline-offset:1px}button.active{background:#dceef2;border-color:#62aaba;color:#0b6075}.stim{background:#172b24;color:#dfffea;border-color:#315a48;padding:10px 14px}.stim:hover{background:#234436}
.sliderbox{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:center}.sliderbox span{font-size:11px;color:var(--muted);font-weight:900}.sliderbox output{min-width:50px;text-align:right;font:900 13px "Segoe UI";color:var(--teal);font-variant-numeric:tabular-nums}input[type=range]{width:100%;accent-color:var(--teal)}
.presets{position:absolute;left:12px;top:9px;display:flex;gap:5px}.presets button{background:#101b22e8;color:#dce8ed;border-color:#5b6f7a}.presets button.active{background:#dceef2;color:#0b6075;border-color:#62aaba}
.bottom-bar{height:56px;display:flex!important;align-items:stretch!important;gap:1px!important;background:#d5dde4!important;border-top:1px solid #d5dde4!important}.bottom-bar .fkey{flex:1!important;background:#e7edf3!important;color:#16232c!important;text-decoration:none!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:9px!important;padding:0 12px!important;font:800 13px/1 "Segoe UI",Arial,sans-serif!important}.bottom-bar .fkey span{color:#0f7a95!important;font-size:15px!important}.bottom-bar .fkey b{color:#16232c!important;font-size:13px!important}.bottom-bar .fkey:hover,.bottom-bar .fkey:focus-visible{background:#dce8f0!important;outline:none!important}
@media(max-width:980px){body{padding:0}.app{width:100vw;min-height:100vh;max-height:none;aspect-ratio:auto;grid-template-rows:42px auto minmax(760px,1fr) auto 56px}.toolbar{padding:8px 12px;flex-wrap:wrap}.workspace{grid-template-columns:1fr}.controls{grid-template-columns:1fr}.types{justify-content:center}.source{height:105px}}
</style>
</head>
<body>
<main class="app">
  <div class="titlebar"><div class="session"><span class="dot"></span>EDX Öğrenim İstasyonu — Bölüm 8</div><div class="brand"><b>EDX</b>SİM</div></div>
  <div class="toolbar"><span class="label">Konu</span><strong>Stimulus artefaktı</strong><span class="label">Tek hedef</span><strong>Kablo kuplajı</strong><span class="mode">SERBEST LABORATUVAR</span></div>
  <section class="workspace">
    <div class="panel">
      <div class="panel-head"><span>Uyarıcı kablo → kayıt döngüsü → amplifikatör</span><span id="stateBadge" class="state">Koaksiyel + ayrık</span></div>
      <div class="lab">
        <div class="coupling" id="coupling">
          <canvas id="cableCanvas"></canvas>
          <div class="presets"><button id="cleanBtn" class="active">Koaksiyel + ayrık</button><button id="nearBtn">Yakın koaksiyel</button><button id="worstBtn">Üst üste serbest</button></div>
          <div class="formula"><b>Kapasitif:</b> I ≈ Ck·dV/dt &nbsp;|&nbsp; <b>Manyetik:</b> Vind ≈ M·di/dt</div>
        </div>
        <div class="scope" id="scope"><canvas id="scopeCanvas"></canvas><div class="legend"><span class="key"><i class="sw"></i>Kaydedilen</span><span class="key"><i class="sw art"></i>İndüklenen</span><span class="key"><i class="sw true"></i>Gerçek DSAP</span></div></div>
      </div>
    </div>
    <aside class="panel">
      <div class="panel-head"><span>Neyi sabit tutuyoruz?</span></div>
      <div class="side-body">
        <div class="invariant"><span>Stimulus darbesi</span><b>AYNI</b><span>Elektrot montajı</span><b>AYNI</b><span>Gerçek DSAP</span><b id="trueOut">14 µV · 2,4 ms</b></div>
        <div class="meter"><div class="meter-top"><span>Toplam kablo kuplajı</span><b id="couplingOut">%1</b></div><div class="track"><div id="couplingFill" class="fill"></div></div></div>
        <div class="readout"><span>Artefakt @ onset</span><b id="artifactOut">0,2 µV</b></div>
        <div class="readout"><span>Amplifikatör toparlanması</span><b id="recoveryOut">onsetten önce</b></div>
        <div class="lesson" id="lesson"><b>Klinik hedef:</b> Ayrım ve kısa paralel güzergâh kuplajı azaltır; bükümlü çift loop alanını, koaksiyel kalkan kapasitif pickup'ı küçültür.</div>
        <div class="source"><img src="../figures/source-v3/fig_8_12_cables.png" alt="Şekil 8.12 koaksiyel kablo ve serbest teller"><div><b>Şekil 8.12</b>Aynı biyolojik yanıt; serbest tellerde stimulus geçicisi ve kuyruk belirgin, koaksiyel kabloda baseline daha temiz.</div></div>
      </div>
    </aside>
  </section>
  <div class="controls">
    <div class="types" aria-label="Kayıt kablosu tipi"><button id="freeBtn">Serbest</button><button id="twistedBtn">Bükümlü çift</button><button id="coaxBtn" class="active">Koaksiyel</button></div>
    <label class="sliderbox"><span>Ayrım</span><input id="spacing" type="range" min="0" max="30" step="1" value="25"><output id="spacingOut">25 cm</output></label>
    <label class="sliderbox"><span>Paralel/örtüşen bölüm</span><input id="overlap" type="range" min="0" max="100" step="1" value="15"><output id="overlapOut">%15</output></label>
    <button id="stimBtn" class="stim">Stimulus ver</button>
  </div>
  <nav class="bottom-bar" aria-label="Standart sunum gezinmesi"><a class="fkey" href="kablo-ayrimi.html"><span>F1</span><b>Önceki</b></a><a class="fkey" href="../index.html"><span>F2</span><b>İçindekiler</b></a><a class="fkey" href="../katot-polarite/index.html"><span>F3</span><b>Sonraki</b></a></nav>
</main>
<script>
const cable=document.getElementById("cableCanvas"),cc=cable.getContext("2d"),couplingWrap=document.getElementById("coupling");
const scope=document.getElementById("scopeCanvas"),sc=scope.getContext("2d"),scopeWrap=document.getElementById("scope");
const spacingEl=document.getElementById("spacing"),overlapEl=document.getElementById("overlap");
const spacingOut=document.getElementById("spacingOut"),overlapOut=document.getElementById("overlapOut");
const stateBadge=document.getElementById("stateBadge"),couplingOut=document.getElementById("couplingOut"),couplingFill=document.getElementById("couplingFill");
const artifactOut=document.getElementById("artifactOut"),recoveryOut=document.getElementById("recoveryOut"),lesson=document.getElementById("lesson");
const freeBtn=document.getElementById("freeBtn"),twistedBtn=document.getElementById("twistedBtn"),coaxBtn=document.getElementById("coaxBtn");
const cleanBtn=document.getElementById("cleanBtn"),nearBtn=document.getElementById("nearBtn"),worstBtn=document.getElementById("worstBtn");
let spacing=25,overlap=15,cableType="coax",stimStart=-1,raf=0,dpr=Math.max(1,window.devicePixelRatio||1);
const TRUE_AMP=14,TRUE_LAT=2.4;
function fit(canvas,wrap){const r=wrap.getBoundingClientRect(),w=Math.max(320,Math.round(r.width)),h=Math.max(130,Math.round(r.height));canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);canvas.style.width=w+"px";canvas.style.height=h+"px";canvas.getContext("2d").setTransform(dpr,0,0,dpr,0,0);return{w,h}}
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function couplingValue(){
  const parallel=overlap/100,near=Math.exp(-spacing/8),fringe=.10*Math.exp(-spacing/14);
  const typeFactor=cableType==="free"?1:cableType==="twisted"?.30:.16;
  return clamp((parallel*near+fringe)*typeFactor,0,1);
}
function trueSnap(t){if(t<TRUE_LAT)return 0;const u=t-TRUE_LAT;return -14*Math.exp(-Math.pow((u-.48)/.23,2))+10.7*Math.exp(-Math.pow((u-1.05)/.40,2))-1.5*Math.exp(-Math.pow((u-2.0)/.65,2))}
function induced(t,k){if(t<.22)return 0;const u=t-.22;return k*(-92*Math.exp(-u/.045)+53*Math.exp(-u/.17)+42*Math.exp(-u/1.15)+18*Math.exp(-u/3.6))}
function noise(t){return .34*Math.sin(t*29.1)+.18*Math.sin(t*67.5+.7)+.10*Math.sin(t*107.2)}
function dot(c,x,y,r,fill,stroke="#fff"){c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.fillStyle=fill;c.fill();c.strokeStyle=stroke;c.lineWidth=2;c.stroke()}
function line(c,pts,color,width=2,dash=[]){c.save();c.strokeStyle=color;c.lineWidth=width;c.setLineDash(dash);c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.stroke();c.restore()}
function label(c,text,x,y,color="#dce8ed",size=11,align="left"){c.fillStyle=color;c.font=`800 ${size}px Segoe UI`;c.textAlign=align;c.fillText(text,x,y);c.textAlign="left"}
function drawRecordingCable(c,x1,x2,y,type){
  if(type==="free"){line(c,[[x1,y-8],[x2,y-8]],"#36c9d7",3);line(c,[[x1,y+8],[x2,y+8]],"#64a7ff",3);label(c,"açık loop alanı",x1+250,y-17,"#9fc4d1")}
  else if(type==="twisted"){const p1=[],p2=[];for(let i=0;i<=120;i++){const x=x1+(x2-x1)*i/120,dy=7*Math.sin(i/120*Math.PI*12);p1.push([x,y+dy]);p2.push([x,y-dy])}line(c,p1,"#36c9d7",2.5);line(c,p2,"#64a7ff",2.5);label(c,"küçük etkin loop alanı",x1+250,y-17,"#9fc4d1")}
  else{line(c,[[x1,y],[x2,y]],"#718b99",12);line(c,[[x1,y],[x2,y]],"#d7e4e9",6);line(c,[[x1,y],[x2,y]],"#36c9d7",2);label(c,"kalkan + yakın dönüş yolu",x1+250,y-17,"#9fc4d1")}
}
function drawCables(now){
  const {w,h}=fit(cable,couplingWrap);cc.clearRect(0,0,w,h);cc.fillStyle="#101d24";cc.fillRect(0,0,w,h);
  const left=42,right=w-42,stimY=h*.36,sepPx=28+spacing*(h*.35/30),recY=Math.min(h-44,stimY+sepPx);
  const overlapStart=right-(right-left)*(overlap/100),k=couplingValue();
  label(cc,"UYARICI KABLO",left,stimY-18,"#ff9aa2",12);label(cc,"KAYIT KABLOSU · "+(cableType==="free"?"SERBEST":cableType==="twisted"?"BÜKÜMLÜ ÇİFT":"KOAKSİYEL"),left,recY-17,"#8edce5",12);
  line(cc,[[left,stimY],[right,stimY]],"#eb5a65",7);dot(cc,left-10,stimY,10,"#27161a","#eb5a65");label(cc,"stim",left-10,stimY+4,"#ffb0b6",9,"center");
  drawRecordingCable(cc,left,right,recY,cableType);dot(cc,right+10,recY,11,"#112b31","#36c9d7");label(cc,"AMP",right+10,recY+4,"#d9fbff",9,"center");
  if(overlap>2){
    cc.fillStyle=`rgba(54,201,215,${.04+.15*k})`;cc.fillRect(overlapStart,stimY-11,right-overlapStart,recY-stimY+22);
    line(cc,[[overlapStart,stimY-20],[right,stimY-20]],"#a9bcc5",1,[4,4]);
    label(cc,`paralel/örtüşen bölüm %${overlap}`,Math.max(left,overlapStart),stimY-27,"#b9c9d0",10);
    const count=Math.max(2,Math.round(2+8*k));for(let i=0;i<count;i++){const x=overlapStart+(right-overlapStart)*(i+.5)/count;cc.strokeStyle=`rgba(54,201,215,${.18+.68*k})`;cc.lineWidth=1.4;cc.setLineDash([4,4]);cc.beginPath();cc.moveTo(x,stimY+6);cc.bezierCurveTo(x+12,(stimY+recY)/2,x-12,(stimY+recY)/2,x,recY-6);cc.stroke()}cc.setLineDash([]);
  }
  line(cc,[[right-18,stimY+10],[right-18,recY-10]],"#ffc857",1,[3,3]);label(cc,`${spacing} cm`,right-24,(stimY+recY)/2+4,"#ffc857",10,"right");
  label(cc,"dV/dt",w*.54,stimY-16,"#ff9aa2",10);label(cc,"kuplaj",w*.56,(stimY+recY)/2,"#59d9e5",10);
  if(stimStart>=0){
    const e=(now-stimStart)/1000,p=clamp(e/.55,0,1),px=left+(right-left)*p;dot(cc,px,stimY,7,"#fff","#eb5a65");
    const flash=Math.max(0,1-Math.abs(e-.45)/.35);if(flash>0&&k>.01){for(let i=0;i<3;i++){cc.beginPath();cc.arc(px,stimY,12+i*10+12*(1-flash),0,Math.PI*2);cc.strokeStyle=`rgba(235,90,101,${flash*(.75-i*.18)})`;cc.lineWidth=2;cc.stroke()}}
    if(e>.38&&e<1.3&&k>.01){const q=clamp((e-.38)/.7,0,1),ix=overlapStart+(right-overlapStart)*q;dot(cc,ix,recY,5+5*k,"#36c9d7","#fff");label(cc,"indüklenen geçici",Math.min(right-120,ix+8),recY-16,"#70e8f1",10)}
    if(e>1.55)stimStart=-1;
  }
}
function drawScope(now){
  const {w,h}=fit(scope,scopeWrap);sc.clearRect(0,0,w,h);sc.fillStyle="#06140f";sc.fillRect(0,0,w,h);
  const L=50,R=w-22,T=25,B=h-31,mid=(T+B)/2,windowMs=8,halfUv=50,k=couplingValue();
  const x=t=>L+(R-L)*t/windowMs,y=v=>mid+(v/halfUv)*(B-T)/2;
  sc.strokeStyle="#143326";sc.lineWidth=1;for(let i=0;i<=8;i++){sc.beginPath();sc.moveTo(x(i),T);sc.lineTo(x(i),B);sc.stroke()}for(let i=0;i<=6;i++){const yy=T+(B-T)*i/6;sc.beginPath();sc.moveTo(L,yy);sc.lineTo(R,yy);sc.stroke()}
  sc.strokeStyle="#27533e";sc.lineWidth=1.3;sc.beginPath();sc.moveTo(L,mid);sc.lineTo(R,mid);sc.stroke();sc.fillStyle="#789486";sc.font="700 10px Segoe UI";sc.textAlign="center";for(let i=0;i<=8;i+=2)sc.fillText(i+" ms",x(i),B+16);sc.textAlign="left";sc.fillText("20 µV/div",L,T-8);
  const elapsed=stimStart>=0?(now-stimStart)/1000:99,progress=Math.min(1,Math.max(.02,elapsed/1.7));
  function plot(fn,color,width,dash=[]){sc.strokeStyle=color;sc.lineWidth=width;sc.setLineDash(dash);sc.beginPath();const n=Math.floor(720*progress);for(let i=0;i<=n;i++){const t=windowMs*i/720,v=clamp(fn(t),-halfUv,halfUv);i?sc.lineTo(x(t),y(v)):sc.moveTo(x(t),y(v))}sc.stroke();sc.setLineDash([])}
  plot(t=>induced(t,k),"#36c9d7",1.5);plot(t=>trueSnap(t),"#ffc857",1.6,[6,4]);sc.save();sc.shadowColor="#5eea8d";sc.shadowBlur=5;plot(t=>induced(t,k)+trueSnap(t)+noise(t),"#5eea8d",2.2);sc.restore();
  sc.strokeStyle="#ffc85788";sc.setLineDash([3,4]);sc.beginPath();sc.moveTo(x(TRUE_LAT),T);sc.lineTo(x(TRUE_LAT),B);sc.stroke();sc.setLineDash([]);sc.fillStyle="#ffc857";sc.font="800 10px Segoe UI";sc.fillText("gerçek onset 2,4 ms",x(TRUE_LAT)+5,B-7);
  const a=induced(TRUE_LAT,k);sc.fillStyle="#36c9d7";sc.fillText(`indüklenen @ onset ${a.toFixed(1)} µV`,x(4.8),T+14);
}
function updateUI(){
  const k=couplingValue(),pct=Math.round(k*100),at=induced(TRUE_LAT,k),recovery=k<.08?"onsetten önce":k<.32?"onset çevresinde":"onsetten sonra";
  spacingEl.value=spacing;overlapEl.value=overlap;spacingOut.value=spacing+" cm";overlapOut.value="%"+overlap;
  couplingOut.textContent=pct<1&&k>0?"<%1":"%"+pct;couplingFill.style.width=Math.max(k>0?1:0,pct)+"%";couplingFill.style.background=pct<10?"#5aa977":pct<35?"#d79a3a":"#eb5a65";
  artifactOut.textContent=at.toFixed(1).replace(".",",")+" µV";recoveryOut.textContent=recovery;
  [freeBtn,twistedBtn,coaxBtn].forEach(b=>b.classList.remove("active"));({free:freeBtn,twisted:twistedBtn,coax:coaxBtn})[cableType].classList.add("active");
  const isClean=cableType==="coax"&&spacing===25&&overlap===15,isNear=cableType==="coax"&&spacing===3&&overlap===85,isWorst=cableType==="free"&&spacing===0&&overlap===100;
  cleanBtn.classList.toggle("active",isClean);nearBtn.classList.toggle("active",isNear);worstBtn.classList.toggle("active",isWorst);
  if(pct<10){stateBadge.textContent="Koaksiyel + ayrık";stateBadge.className="state";lesson.innerHTML="<b>Klinik hedef:</b> Ayrım ve kısa paralel güzergâh kuplajı azaltır; bükümlü çift loop alanını, koaksiyel kalkan kapasitif pickup'ı küçültür."}
  else if(pct<35){stateBadge.textContent="Kuplaj var · DSAP seçilebilir";stateBadge.className="state warn";lesson.innerHTML="<b>Koaksiyel mutlak koruma değildir:</b> Çok yakın ve uzun paralel güzergâh, kalkan olsa bile bir miktar kuplaj bırakabilir."}
  else{stateBadge.textContent="Artefakt DSAP üzerine biniyor";stateBadge.className="state bad";lesson.innerHTML="<b>Şekil 8.12'nin ana noktası:</b> Serbest teller geniş loop alanı oluşturur; örtüşme ile kuplaj artar ve stimulus kuyruğu onset/amplitüd ölçümünü bozar."}
  window.__cableCouplingState={spacing,overlap,cableType,coupling:+k.toFixed(4),artifactAtOnset:+at.toFixed(3),trueAmp:TRUE_AMP,trueLatency:TRUE_LAT,recovery};
}
function setState(s,o,t){spacing=s;overlap=o;cableType=t;updateUI();draw(performance.now())}
spacingEl.addEventListener("input",e=>{spacing=Number(e.target.value);updateUI();draw(performance.now())});overlapEl.addEventListener("input",e=>{overlap=Number(e.target.value);updateUI();draw(performance.now())});
freeBtn.addEventListener("click",()=>{cableType="free";updateUI();draw(performance.now())});twistedBtn.addEventListener("click",()=>{cableType="twisted";updateUI();draw(performance.now())});coaxBtn.addEventListener("click",()=>{cableType="coax";updateUI();draw(performance.now())});
cleanBtn.addEventListener("click",()=>setState(25,15,"coax"));nearBtn.addEventListener("click",()=>setState(3,85,"coax"));worstBtn.addEventListener("click",()=>setState(0,100,"free"));
document.getElementById("stimBtn").addEventListener("click",()=>{stimStart=performance.now();if(!raf)raf=requestAnimationFrame(loop)});
function draw(now){drawCables(now);drawScope(now)}function loop(now){draw(now);if(stimStart>=0)raf=requestAnimationFrame(loop);else raf=0}
new ResizeObserver(()=>draw(performance.now())).observe(document.querySelector(".app"));setState(25,15,"coax");
</script>
<script data-standard-nav-v3>document.addEventListener("keydown",e=>{if(["INPUT","SELECT","TEXTAREA"].includes(document.activeElement?.tagName))return;const k=e.key.toUpperCase();const a=k==="F1"?document.querySelector(".bottom-bar .fkey:nth-child(1)"):k==="F2"?document.querySelector(".bottom-bar .fkey:nth-child(2)"):k==="F3"?document.querySelector(".bottom-bar .fkey:nth-child(3)"):null;if(a){e.preventDefault();location.href=a.href}});</script>
</body>
</html>'''

OUT.write_text(HTML, encoding="utf-8")
print(OUT)
