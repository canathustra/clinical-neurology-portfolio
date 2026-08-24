(function(){
"use strict";

const canvas=document.getElementById("mechanismCanvas");
const ctx=canvas.getContext("2d");
const stageWrap=document.getElementById("stageWrap");
const phaseIndex=document.getElementById("phaseIndex");
const phaseText=document.getElementById("phaseText");
const stateBadge=document.getElementById("stateBadge");
const playPauseBtn=document.getElementById("playPauseBtn");
const replayBtn=document.getElementById("replayBtn");
const phaseButtons=Array.from(document.querySelectorAll(".phase-btn"));
const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const COLORS={ink:"#16232c",muted:"#5c6b78",dim:"#8a97a3",line:"#d7dee5",cyan:"#0f7a95",blue:"#2f6fbd",amber:"#c97a2a",green:"#2f7d52",red:"#b43b47",purple:"#5b3a8e"};
const AGENTS=[
  {name:"Nivolumab",target:"anti-PD-1",color:COLORS.blue},
  {name:"Pembrolizumab",target:"anti-PD-1",color:COLORS.cyan},
  {name:"Ipilimumab",target:"anti-CTLA-4",color:COLORS.red},
  {name:"Atezolizumab",target:"anti-PD-L1",color:COLORS.purple},
  {name:"Avelumab",target:"anti-PD-L1",color:COLORS.green}
];
const PHASES=[
  {label:"ICPI kontrol noktasına ulaşır",short:"ICPI blokajı",duration:3000},
  {label:"T-hücresi freni kalkar",short:"T-hücresi aktive",duration:3200},
  {label:"Sinir kökü hedeflenir",short:"Kök inflamasyonu",duration:3400},
  {label:"Kan-sinir ve kan-BOS bariyeri geçirgenleşir",short:"Bariyer geçirgenliği artar",duration:3400},
  {label:"Lenfositler BOS'a geçer",short:"Hafif pleositoz",duration:4300}
];

const query=new URLSearchParams(location.search);
const requested=Number(query.get("phase"));
const forcedPhase=Number.isInteger(requested)&&requested>=1&&requested<=5?requested-1:null;
const forcedProgress=Math.max(0,Math.min(1,Number(query.get("progress"))||1));
let cssW=0,cssH=0,dpr=Math.max(1,window.devicePixelRatio||1);
let phase=forcedPhase!==null?forcedPhase:(reducedMotion?4:0);
let phaseStart=performance.now()-(forcedPhase!==null?PHASES[phase].duration*forcedProgress:0);
let pausedProgress=forcedPhase!==null?forcedProgress:0;
let playing=false,finished=forcedPhase!==null||reducedMotion;

const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const ease=t=>{t=clamp(t);return t*t*(3-2*t);};
const mix=(a,b,t)=>a+(b-a)*t;
const rgba=(hex,a)=>{const n=parseInt(hex.slice(1),16);return `rgba(${(n>>16)&255},${(n>>8)&255},${n&255},${a})`;};

function rr(c,x,y,w,h,r){c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath();}
function label(txt,x,y,size=12,color=COLORS.ink,weight=700,align="center"){
  ctx.save();ctx.fillStyle=color;ctx.font=`${weight} ${size}px Segoe UI, sans-serif`;ctx.textAlign=align;ctx.textBaseline="middle";ctx.fillText(txt,x,y);ctx.restore();
}
function glow(x,y,r,color,alpha=.75){
  ctx.save();ctx.shadowColor=color;ctx.shadowBlur=r*2.3;ctx.fillStyle=rgba(color,alpha);ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.restore();
}
function arrow(x1,y1,x2,y2,color,alpha=.86,width=4){
  ctx.save();ctx.globalAlpha=alpha;ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=width;ctx.lineCap="round";ctx.shadowColor=color;ctx.shadowBlur=8;
  ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();const a=Math.atan2(y2-y1,x2-x1);
  ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-12*Math.cos(a-.5),y2-12*Math.sin(a-.5));ctx.lineTo(x2-12*Math.cos(a+.5),y2-12*Math.sin(a+.5));ctx.closePath();ctx.fill();ctx.restore();
}

function resize(){
  const r=stageWrap.getBoundingClientRect();cssW=Math.max(760,Math.round(r.width));cssH=Math.max(420,Math.round(r.height));
  canvas.width=Math.round(cssW*dpr);canvas.height=Math.round(cssH*dpr);canvas.style.width=cssW+"px";canvas.style.height=cssH+"px";ctx.setTransform(dpr,0,0,dpr,0,0);
}
new ResizeObserver(resize).observe(stageWrap);

function drawBackdrop(activeColor){
  const g=ctx.createLinearGradient(0,0,cssW,cssH);g.addColorStop(0,"#fbfdff");g.addColorStop(.58,"#f4f7f9");g.addColorStop(1,"#edf4f7");ctx.fillStyle=g;ctx.fillRect(0,0,cssW,cssH);
  const h=ctx.createRadialGradient(cssW*.49,cssH*.45,10,cssW*.49,cssH*.45,cssW*.42);h.addColorStop(0,rgba(activeColor,.10));h.addColorStop(1,"rgba(255,255,255,0)");ctx.fillStyle=h;ctx.fillRect(0,0,cssW,cssH);
  ctx.fillStyle="rgba(80,105,122,.07)";for(let y=22;y<cssH;y+=26)for(let x=22;x<cssW;x+=26){ctx.beginPath();ctx.arc(x,y,1,0,Math.PI*2);ctx.fill();}
}

function drawAgents(p){
  label("GBS İLE BİLDİRİLEN ICPI ÖRNEKLERİ",cssW*.045,cssH*.047,10.5,COLORS.muted,850,"left");
  const left=cssW*.045,right=cssW*.955,gap=9,w=(right-left-gap*4)/5,h=Math.min(44,cssH*.083),y=cssH*.066;
  AGENTS.forEach((a,i)=>{
    const x=left+i*(w+gap),lift=phase===0?Math.sin(clamp(p*1.3-i*.08)*Math.PI)*3:0;
    rr(ctx,x,y-lift,w,h,7);ctx.fillStyle="rgba(255,255,255,.88)";ctx.fill();ctx.strokeStyle=rgba(a.color,.55);ctx.lineWidth=1.4;ctx.stroke();
    ctx.fillStyle=a.color;ctx.fillRect(x,y-lift,4,h);label(a.name,x+w*.49,y-lift+h*.38,11.5,COLORS.ink,800);label(a.target,x+w*.49,y-lift+h*.70,9.5,COLORS.muted,700);
  });
}

function organicCell(x,y,r,active,labelText,t){
  ctx.save();
  if(active){const q=.5+.5*Math.sin(t*3);ctx.beginPath();ctx.arc(x,y,r+8+q*4,0,Math.PI*2);ctx.fillStyle=rgba(COLORS.red,.08+.07*q);ctx.fill();}
  const g=ctx.createRadialGradient(x-r*.25,y-r*.28,2,x,y,r);g.addColorStop(0,active?"#ef9aa0":"#c5d7e8");g.addColorStop(1,active?"#b43b47":"#7098bc");ctx.fillStyle=g;
  ctx.beginPath();for(let i=0;i<=32;i++){const a=i/32*Math.PI*2,rough=1+.035*Math.sin(a*5+t*1.4);const px=x+Math.cos(a)*r*rough,py=y+Math.sin(a)*r*rough;if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);}ctx.closePath();ctx.fill();ctx.strokeStyle=active?"#8f2731":"#557d9e";ctx.lineWidth=2;ctx.stroke();
  ctx.beginPath();ctx.ellipse(x+r*.08,y-r*.04,r*.39,r*.33,-.25,0,Math.PI*2);ctx.fillStyle=active?"#7f2029":"#3d678d";ctx.fill();
  label(labelText,x,y+r+16,11,active?COLORS.red:COLORS.muted,850);ctx.restore();
}

function drawCheckpoint(p,t){
  const y=cssH*.31,apcX=cssW*.11,tX=cssW*.30,r=Math.min(41,cssH*.073);
  organicCell(apcX,y,r,false,"APC / tümör hücresi",t);
  organicCell(tX,y,r,phase>=1,"T hücresi",t);
  const ligandX=apcX+r*.82,receptorX=tX-r*.82;
  rr(ctx,ligandX-2,y-14,50,28,5);ctx.fillStyle="#566773";ctx.fill();label("PD-L1 / B7",ligandX+23,y,9,"#fff",800);
  rr(ctx,receptorX-58,y-14,58,28,5);ctx.fillStyle="#566773";ctx.fill();label("PD-1 / CTLA-4",receptorX-29,y,8.7,"#fff",800);
  const x1=ligandX+48,x2=receptorX-58,m=(x1+x2)/2;
  if(phase===0){
    ctx.strokeStyle=COLORS.green;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x1,y);ctx.lineTo(x2,y);ctx.stroke();
    const travel=ease(p),sx=cssW*.49,sy=cssH*.09,tx=m,ty=y;const cx=mix(sx,tx,travel),cy=mix(sy,ty,travel)-Math.sin(travel*Math.PI)*50;
    ctx.save();ctx.translate(cx,cy);ctx.rotate(travel*Math.PI);rr(ctx,-22,-11,44,22,11);ctx.fillStyle=COLORS.purple;ctx.fill();label("ICPI",0,0,9,"#fff",900);ctx.restore();
    label(p<.72?"İnhibitör sinyal: fren devrede":"ICPI reseptöre bağlanır",m,y+34,10,p<.72?COLORS.green:COLORS.purple,850);
  }else{
    ctx.strokeStyle="#c8d3dc";ctx.lineWidth=2.5;ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(x1,y);ctx.lineTo(x2,y);ctx.stroke();ctx.setLineDash([]);
    ctx.beginPath();ctx.arc(m,y,15,0,Math.PI*2);ctx.strokeStyle=COLORS.red;ctx.lineWidth=3;ctx.stroke();ctx.beginPath();ctx.moveTo(m-10,y-10);ctx.lineTo(m+10,y+10);ctx.stroke();
    label("KONTROL NOKTASI BLOKE",m,y+34,10,COLORS.red,900);
  }
  return{tX,y,r};
}

function drawNerve(attack,t){
  const x=cssW*.46,y=cssH*.225,w=cssW*.25,h=cssH*.17;
  ctx.save();ctx.shadowColor=attack?rgba(COLORS.red,.55):"rgba(51,82,101,.18)";ctx.shadowBlur=attack?18:10;
  rr(ctx,x,y,w,h,16);ctx.fillStyle="rgba(255,255,255,.94)";ctx.fill();ctx.strokeStyle=attack?COLORS.red:"#a7b7c3";ctx.lineWidth=attack?2.4:1.5;ctx.stroke();ctx.restore();
  label("PERİFERİK SİNİR / KÖK",x+w/2,y-14,11,attack?COLORS.red:COLORS.muted,900);
  const axY=y+h*.57;ctx.strokeStyle="#c97a2a";ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x+14,axY);ctx.lineTo(x+w-14,axY);ctx.stroke();
  const n=6,seg=(w-26)/n;for(let i=0;i<n;i++){const sx=x+13+i*seg+3;rr(ctx,sx,axY-17,seg-6,34,9);ctx.fillStyle=attack?"#e9c8ca":"#cde5d6";ctx.fill();ctx.strokeStyle=attack?"#b43b47":"#75a58a";ctx.lineWidth=1.2;ctx.stroke();if(attack&&i%2===0){ctx.beginPath();ctx.moveTo(sx+seg*.25,axY-20);ctx.lineTo(sx+seg*.48,axY+20);ctx.lineTo(sx+seg*.68,axY-18);ctx.strokeStyle=COLORS.red;ctx.lineWidth=2;ctx.stroke();}}
  if(attack){for(let i=0;i<4;i++){const q=.5+.5*Math.sin(t*3+i);glow(x+w*(.2+i*.2),y+h*.18,3+q*3,COLORS.red,.55);}}
  return{x,y,w,h};
}

function drawAttack(tCell,nerve,p,t){
  if(phase<1)return;
  const activeP=phase===1?ease(p):1;arrow(tCell.tX+tCell.r+6,tCell.y,nerve.x-12,nerve.y+nerve.h*.48,phase>=2?COLORS.red:COLORS.amber,.35+.58*activeP,3+activeP*2);
  const cellX=mix(tCell.tX+tCell.r+18,nerve.x-25,activeP),cellY=mix(tCell.y,nerve.y+nerve.h*.5,activeP)-Math.sin(activeP*Math.PI)*28;organicCell(cellX,cellY,16,true,"",t);
  label(phase===1?"Otoreaktif klon genişler":"Kök / miyelin hedeflenir",cssW*.40,cssH*.43,10,phase===1?COLORS.amber:COLORS.red,850);
}

function drawBarrier(p,t){
  const y=cssH*.62,left=cssW*.38,right=cssW*.79,h=32,n=10,cellW=(right-left)/n;
  ctx.fillStyle="#dff2f5";ctx.fillRect(left-18,y+h/2,right-left+36,cssH-y);
  label("KAN / RADİKÜLER DOLAŞIM",left,y-29,10,COLORS.muted,850,"left");label("BOS · RADİKÜLOMENİNGEAL ALAN",left,cssH*.94,10,COLORS.cyan,850,"left");
  const open=phase>=3?(phase===3?ease(p):1):0,gap=22*open;
  for(let i=0;i<n;i++){let shift=0,w=cellW-4;if(i===4){w-=gap*.46;}if(i===5){shift=gap;}const x=left+i*cellW+shift;rr(ctx,x,y,w,h,7);ctx.fillStyle="#c8d8e6";ctx.fill();ctx.strokeStyle="#819aac";ctx.lineWidth=1;ctx.stroke();ctx.beginPath();ctx.arc(x+w/2,y+h/2,3.2,0,Math.PI*2);ctx.fillStyle="#688397";ctx.fill();}
  label("KAN–BOS BARİYERİ",right,y-12,10,phase>=3?COLORS.amber:COLORS.muted,900,"right");
  if(phase>=3){for(let i=0;i<8;i++){const x=left+(i+.4)*(right-left)/8,q=.5+.5*Math.sin(t*4+i*1.3);glow(x,y-18-(i%2)*8,2.5+q*2,COLORS.amber,.38+.35*open);}label("Sitokinler → geçirgenlik ↑",(left+right)/2,y-43,10,COLORS.amber,900);}
  return{y,left,right,h,gap};
}

function drawCrossing(barrier,p,t){
  if(phase<4)return 5;
  const progress=ease(p),cells=7;
  for(let i=0;i<cells;i++){const local=clamp(progress*1.38-i*.105),x=barrier.left+(barrier.right-barrier.left)*(.39+i*.035)+(i%2?8:-6),y0=barrier.y-62,y1=barrier.y+barrier.h+70,y=mix(y0,y1,ease(local));organicCell(x,y,8.5,local>.25,"",t);}
  return Math.round(5+progress*10);
}

function drawGauge(count,p){
  const x=cssW*.835,y=cssH*.23,w=cssW*.125,h=cssH*.57;
  rr(ctx,x,y,w,h,12);ctx.fillStyle="rgba(255,255,255,.91)";ctx.fill();ctx.strokeStyle="#ccd7df";ctx.lineWidth=1.4;ctx.stroke();
  label("BOS HÜCRE SAYISI",x+w/2,y+22,10.5,COLORS.muted,900);
  const gx=x+w*.22,gy=y+46,gw=w*.18,gh=h-92,zones=[{to:.18,c:COLORS.green,t:"0–5"},{to:.48,c:COLORS.blue,t:"6–20"},{to:.74,c:COLORS.amber,t:"21–50"},{to:1,c:COLORS.red,t:">50"}];let last=0;
  zones.forEach(z=>{ctx.fillStyle=rgba(z.c,.22);ctx.fillRect(gx,gy+gh*last,gw,gh*(z.to-last));ctx.strokeStyle=rgba(z.c,.55);ctx.strokeRect(gx,gy+gh*last,gw,gh*(z.to-last));label(z.t,gx+gw+11,gy+gh*(last+z.to)/2,10,z.c,850,"left");last=z.to;});
  const normalized=count<=5?count/5*.18:count<=20?.18+(count-5)/15*.30:count<=50?.48+(count-20)/30*.26:.74+Math.min((count-50)/30,.26),markerY=gy+gh*normalized;
  arrow(gx-14,markerY,gx-1,markerY,phase===4?COLORS.blue:COLORS.green,.95,3);label(count+" /µL",x+w*.60,y+h-38,17,phase===4?COLORS.blue:COLORS.green,900);
  label(phase===4?"hafif lenfositik":"normal",x+w*.60,y+h-18,9.5,phase===4?COLORS.cyan:COLORS.green,850);
  if(phase===4&&p>.65){label("Derleme: 4/33 · maks. 15/µL",x+w/2,y+h+20,9.5,COLORS.muted,800);label(">50 → alternatif tanı",x+w/2,y+h+37,9.5,COLORS.red,900);}
}

function drawPhaseCaption(p){
  const color=[COLORS.purple,COLORS.red,COLORS.red,COLORS.amber,COLORS.blue][phase],x=cssW*.045,y=cssH*.50,w=cssW*.27;
  label(`0${phase+1}`,x,y-13,24,rgba(color,.34),900,"left");label(PHASES[phase].short.toUpperCase(),x+45,y-13,15,color,900,"left");
  ctx.fillStyle="#dce5eb";rr(ctx,x,y+15,w,7,4);ctx.fill();ctx.fillStyle=color;rr(ctx,x,y+15,w*clamp(p),7,4);ctx.fill();
  const details=["PD-1 / PD-L1 veya CTLA-4 sinyali kesilir","İnhibitör sinyal kaybolur; otoreaktif T hücresi etkinleşir","Periferik sinir ve kök çevresinde hücresel inflamasyon gelişir","Sitokinler bariyer bağlantılarını gevşetir","BOS'ta çoğunlukla hafif lenfositik artış"];
  label(details[phase],x,y+48,11,COLORS.muted,750,"left");
}

function updateUI(){
  phaseIndex.textContent=(phase+1)+"/5";phaseText.textContent=PHASES[phase].label;stateBadge.textContent=PHASES[phase].short;
  const color=[COLORS.purple,COLORS.red,COLORS.red,COLORS.amber,COLORS.blue][phase];stateBadge.style.color=color;stateBadge.style.borderColor=rgba(color,.35);stateBadge.style.background=rgba(color,.08);
  phaseButtons.forEach((b,i)=>b.classList.toggle("active",i===phase));playPauseBtn.textContent=playing?"Duraklat":(finished?"Tekrar oynat":pausedProgress>0?"Devam Et":"Başlat");
}

function draw(p,t){
  const activeColor=[COLORS.purple,COLORS.red,COLORS.red,COLORS.amber,COLORS.blue][phase];ctx.clearRect(0,0,cssW,cssH);drawBackdrop(activeColor);drawAgents(p);
  const tCell=drawCheckpoint(phase===0?p:1,t);const nerve=drawNerve(phase>=2,t);drawAttack(tCell,nerve,p,t);const barrier=drawBarrier(p,t);const count=drawCrossing(barrier,p,t);drawGauge(count,p);drawPhaseCaption(p);
}

function tick(now){
  const p=playing?clamp((now-phaseStart)/PHASES[phase].duration):pausedProgress;draw(p,playing?now/1000:pausedProgress*PHASES[phase].duration/1000);
  if(playing&&p>=1){if(phase<PHASES.length-1){phase++;pausedProgress=0;phaseStart=now;updateUI();}else{pausedProgress=1;playing=false;finished=true;updateUI();}}
  requestAnimationFrame(tick);
}

phaseButtons.forEach(btn=>btn.addEventListener("click",()=>{phase=Number(btn.dataset.phase);pausedProgress=.78;playing=false;finished=phase===4;updateUI();}));
playPauseBtn.addEventListener("click",()=>{if(finished){phase=0;pausedProgress=0;phaseStart=performance.now();finished=false;playing=true;}else if(playing){pausedProgress=clamp((performance.now()-phaseStart)/PHASES[phase].duration);playing=false;}else{phaseStart=performance.now()-pausedProgress*PHASES[phase].duration;playing=true;}updateUI();});
replayBtn.addEventListener("click",()=>{phase=0;pausedProgress=0;phaseStart=performance.now();finished=false;playing=true;updateUI();});

resize();updateUI();requestAnimationFrame(tick);
})();
