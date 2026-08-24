(function(){
"use strict";

const stageWrap=document.getElementById("stageWrap");
const canvas=document.getElementById("sceneCanvas");
const ctx=canvas.getContext("2d");
const stateBadge=document.getElementById("stateBadge");
const stat1Out=document.getElementById("stat1Out");
const stat2Out=document.getElementById("stat2Out");
const riskRow=document.getElementById("riskRow");
const mechNote=document.getElementById("mechNote");
const mainSlider=document.getElementById("mainSlider");
const mainReadout=document.getElementById("mainReadout");
const playPauseBtn=document.getElementById("playPauseBtn");
const resetBtn=document.getElementById("resetBtn");
const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const PROG_END=21,PLATEAU_END=28,CHART_END=42,INTUB_START=6,INTUB_END=18;
const MS_PER_DAY=950;
const COLORS={ink:"#16232c",muted:"#5c6b78",dim:"#8a97a3",line:"#d7dee5",blue:"#2f6fbd",cyan:"#0f7a95",red:"#b43b47",amber:"#c97a2a",green:"#2f7d52"};

let cssW=0,cssH=0,dpr=Math.max(1,window.devicePixelRatio||1);
const requestedDay=Number(new URLSearchParams(location.search).get("day"));
let dayFloat=Number.isFinite(requestedDay)?Math.max(0,Math.min(CHART_END,requestedDay)):0;
let playing=false,lastFrame=0,holdUntil=0,loopPending=false;

const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const mix=(a,b,t)=>a+(b-a)*t;
const rgba=(hex,a)=>{const n=parseInt(hex.slice(1),16);return `rgba(${(n>>16)&255},${(n>>8)&255},${n&255},${a})`;};
function rr(c,x,y,w,h,r){c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath();}
function text(txt,x,y,size=12,color=COLORS.ink,weight=700,align="center"){
  ctx.save();ctx.fillStyle=color;ctx.font=`${weight} ${size}px Segoe UI, sans-serif`;ctx.textAlign=align;ctx.textBaseline="middle";ctx.fillText(txt,x,y);ctx.restore();
}
function phaseAt(day){if(day<=PROG_END)return"İlerleme";if(day<=PLATEAU_END)return"Plato";return"İyileşme";}
function phaseColor(day){return day<=PROG_END?COLORS.red:day<=PLATEAU_END?COLORS.amber:COLORS.green;}
function severityAt(day){
  if(day<=PROG_END){const t=day/PROG_END;return 1-Math.pow(t,1.3)*.85;}
  if(day<=PLATEAU_END)return.15;
  const t=(day-PLATEAU_END)/(CHART_END-PLATEAU_END);return.15+t*.45;
}

function resize(){
  const r=stageWrap.getBoundingClientRect();cssW=Math.max(560,Math.round(r.width));cssH=Math.max(360,Math.round(r.height));
  canvas.width=Math.round(cssW*dpr);canvas.height=Math.round(cssH*dpr);canvas.style.width=cssW+"px";canvas.style.height=cssH+"px";ctx.setTransform(dpr,0,0,dpr,0,0);
}
new ResizeObserver(resize).observe(stageWrap);

function updateStatics(){
  const rounded=Math.round(dayFloat),phase=phaseAt(dayFloat),inIntub=dayFloat>=INTUB_START&&dayFloat<=INTUB_END;
  mainSlider.value=dayFloat.toFixed(1);mainReadout.textContent="Gün "+rounded;stateBadge.textContent=phase;
  stateBadge.classList.toggle("on",phase==="İlerleme");stateBadge.classList.toggle("warn",phase==="Plato");
  stat1Out.textContent=phase;stat2Out.textContent=inIntub?"Yüksek · 6–18. gün":dayFloat<INTUB_START?"Henüz düşük":"Pencere geçti";riskRow.classList.toggle("risk-active",inIntub);
  if(dayFloat<=PROG_END){mechNote.innerHTML="<b>İlerleme:</b> Güçsüzlük günler içinde artar. "+(inIntub?"Şimdi <b>entübasyon riskinin en yüksek olduğu 6–18. gün</b> penceresindeyiz.":"Solunum ve bulber fonksiyon yakın izlenir.");}
  else if(dayFloat<=PLATEAU_END){mechNote.innerHTML="<b>Plato:</b> Kötüleşme durur; belirgin iyileşme henüz başlamamıştır. <b>4 haftayı aşan ilerleme</b> tanıyı sorgulatır.";}
  else{mechNote.innerHTML="<b>İyileşme:</b> Düzelme başlar; toparlanma çoğunlukla haftalar–aylar boyunca sürer.";}
  playPauseBtn.textContent=playing?"Duraklat":dayFloat===0?"Başlat":"Devam Et";
}

function drawPhaseBands(left,right,top,bottom,xOf){
  const zones=[{a:0,b:PROG_END,c:COLORS.red,l:"İLERLEME",sub:"0–21. gün"},{a:PROG_END,b:PLATEAU_END,c:COLORS.amber,l:"PLATO",sub:"21–28. gün"},{a:PLATEAU_END,b:CHART_END,c:COLORS.green,l:"İYİLEŞME",sub:"28. gün sonrası"}];
  zones.forEach(z=>{const zoneW=xOf(z.b)-xOf(z.a),progress=clamp((dayFloat-z.a)/(z.b-z.a));ctx.fillStyle=rgba(z.c,.045);ctx.fillRect(xOf(z.a),top,zoneW,bottom-top);ctx.fillStyle=z.c;if(progress>0)ctx.fillRect(xOf(z.a),top,zoneW*progress,3);text(z.l,(xOf(z.a)+xOf(z.b))/2,top-31,11,z.c,900);text(z.sub,(xOf(z.a)+xOf(z.b))/2,top-16,9.5,COLORS.dim,750);});
}

function strokeSegment(start,end,color,xOf,yOf,width=4,alpha=1){
  if(end<=start)return;ctx.save();ctx.globalAlpha=alpha;ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap="round";ctx.lineJoin="round";ctx.shadowColor=color;ctx.shadowBlur=width>3?8:0;ctx.beginPath();
  for(let d=start;d<=end+.001;d+=.18){const actual=Math.min(d,end),x=xOf(actual),y=yOf(severityAt(actual));if(d===start)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();ctx.restore();
}

function draw(now){
  const W=cssW,H=cssH;if(!W||!H)return;ctx.clearRect(0,0,W,H);
  const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,"#fcfdfe");bg.addColorStop(1,"#f1f5f8");ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
  const left=W*.09,right=W*.95,top=H*.20,bottom=H*.80,plotW=right-left,plotH=bottom-top;
  const xOf=d=>left+plotW*(d/CHART_END),yOf=sev=>top+plotH*(1-sev);
  drawPhaseBands(left,right,top,bottom,xOf);

  for(let d=0;d<=CHART_END;d+=7){ctx.strokeStyle="rgba(110,131,145,.15)";ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(xOf(d),top);ctx.lineTo(xOf(d),bottom);ctx.stroke();text(String(d),xOf(d),bottom+19,10,COLORS.dim,750);}
  for(let i=0;i<=4;i++){const y=top+plotH*i/4;ctx.strokeStyle="rgba(110,131,145,.10)";ctx.beginPath();ctx.moveTo(left,y);ctx.lineTo(right,y);ctx.stroke();}

  const winX=xOf(INTUB_START),winW=xOf(INTUB_END)-winX,active=dayFloat>=INTUB_START&&dayFloat<=INTUB_END;
  const riskG=ctx.createLinearGradient(winX,0,winX+winW,0);riskG.addColorStop(0,"rgba(180,59,71,.035)");riskG.addColorStop(.5,active?"rgba(180,59,71,.16)":"rgba(180,59,71,.08)");riskG.addColorStop(1,"rgba(180,59,71,.035)");ctx.fillStyle=riskG;ctx.fillRect(winX,top,winW,plotH);
  ctx.strokeStyle=active?rgba(COLORS.red,.48):rgba(COLORS.red,.25);ctx.lineWidth=1.2;ctx.setLineDash([4,4]);ctx.strokeRect(winX,top,winW,plotH);ctx.setLineDash([]);text("ENTÜBASYON RİSKİ · 6–18. GÜN",winX+winW/2,top+18,10,COLORS.red,900);

  ctx.strokeStyle=rgba(COLORS.amber,.6);ctx.lineWidth=1.5;ctx.setLineDash([6,5]);ctx.beginPath();ctx.moveTo(xOf(PLATEAU_END),top);ctx.lineTo(xOf(PLATEAU_END),bottom);ctx.stroke();ctx.setLineDash([]);
  rr(ctx,xOf(PLATEAU_END)-43,bottom-31,86,22,11);ctx.fillStyle="rgba(255,255,255,.88)";ctx.fill();ctx.strokeStyle=rgba(COLORS.amber,.5);ctx.stroke();text("4 HAFTA SINIRI",xOf(PLATEAU_END),bottom-20,9.5,COLORS.amber,900);

  ctx.strokeStyle="#d2dce3";ctx.lineWidth=3;ctx.beginPath();for(let d=0;d<=CHART_END;d+=.18){const x=xOf(d),y=yOf(severityAt(d));if(d===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();
  strokeSegment(0,Math.min(dayFloat,PROG_END),COLORS.red,xOf,yOf,4.5);
  if(dayFloat>PROG_END)strokeSegment(PROG_END,Math.min(dayFloat,PLATEAU_END),COLORS.amber,xOf,yOf,4.5);
  if(dayFloat>PLATEAU_END)strokeSegment(PLATEAU_END,dayFloat,COLORS.green,xOf,yOf,4.5);

  [[0,COLORS.red],[PROG_END,COLORS.amber],[PLATEAU_END,COLORS.green],[CHART_END,COLORS.green]].forEach(([d,c])=>{ctx.beginPath();ctx.arc(xOf(d),yOf(severityAt(d)),4,0,Math.PI*2);ctx.fillStyle=c;ctx.fill();ctx.strokeStyle="#fff";ctx.lineWidth=1.5;ctx.stroke();});

  const cx=xOf(dayFloat),cy=yOf(severityAt(dayFloat)),color=phaseColor(dayFloat),q=.5+.5*Math.sin(now/350);
  for(let i=1;i<=7;i++){const d=dayFloat-i*.36;if(d<0)continue;ctx.beginPath();ctx.arc(xOf(d),yOf(severityAt(d)),Math.max(1,3-i*.28),0,Math.PI*2);ctx.fillStyle=rgba(color,.38-i*.035);ctx.fill();}
  ctx.strokeStyle=rgba(color,.26);ctx.lineWidth=1.5;ctx.setLineDash([4,4]);ctx.beginPath();ctx.moveTo(cx,top);ctx.lineTo(cx,bottom);ctx.stroke();ctx.setLineDash([]);
  ctx.beginPath();ctx.arc(cx,cy,12+q*4,0,Math.PI*2);ctx.fillStyle=rgba(color,.12);ctx.fill();ctx.beginPath();ctx.arc(cx,cy,8,0,Math.PI*2);ctx.fillStyle=color;ctx.fill();ctx.strokeStyle="#fff";ctx.lineWidth=2.5;ctx.stroke();ctx.beginPath();ctx.arc(cx,cy,2.2,0,Math.PI*2);ctx.fillStyle="#fff";ctx.fill();

  const pillW=112,pillX=clamp(cx-pillW/2,left,right-pillW),pillY=Math.max(top+42,cy-48);rr(ctx,pillX,pillY,pillW,30,15);ctx.fillStyle="rgba(255,255,255,.94)";ctx.fill();ctx.strokeStyle=rgba(color,.55);ctx.lineWidth=1.4;ctx.stroke();text("GÜN "+Math.round(dayFloat)+" · "+phaseAt(dayFloat).toUpperCase(),pillX+pillW/2,pillY+15,10,color,900);

  ctx.save();ctx.translate(left-28,(top+bottom)/2);ctx.rotate(-Math.PI/2);text("KLİNİK ŞİDDET · AŞAĞI = DAHA KÖTÜ",0,0,9.5,COLORS.dim,800);ctx.restore();
  text("HASTALIK GÜNÜ",(left+right)/2,bottom+39,10,COLORS.muted,850);
}

function pause(){playing=false;updateStatics();}
mainSlider.addEventListener("input",()=>{dayFloat=Number(mainSlider.value);holdUntil=0;loopPending=false;pause();});
playPauseBtn.addEventListener("click",()=>{playing=!playing;lastFrame=performance.now();holdUntil=0;if(dayFloat>=CHART_END){dayFloat=0;loopPending=false;}updateStatics();});
resetBtn.addEventListener("click",()=>{dayFloat=0;playing=!reducedMotion;holdUntil=0;loopPending=false;lastFrame=performance.now();updateStatics();});

function tick(now){
  if(!lastFrame)lastFrame=now;const delta=Math.min(100,now-lastFrame);lastFrame=now;
  if(playing){
    if(now>=holdUntil){
      if(loopPending){dayFloat=0;loopPending=false;}
      const next=dayFloat+delta/MS_PER_DAY;
      if(dayFloat<PROG_END&&next>=PROG_END){dayFloat=PROG_END;holdUntil=now+1400;}
      else if(dayFloat<PLATEAU_END&&next>=PLATEAU_END){dayFloat=PLATEAU_END;holdUntil=now+1200;}
      else if(dayFloat<CHART_END&&next>=CHART_END){dayFloat=CHART_END;holdUntil=now+2600;loopPending=true;}
      else dayFloat=Math.min(CHART_END,next);
      updateStatics();
    }
  }
  draw(playing?now:0);requestAnimationFrame(tick);
}

resize();updateStatics();requestAnimationFrame(tick);
})();
