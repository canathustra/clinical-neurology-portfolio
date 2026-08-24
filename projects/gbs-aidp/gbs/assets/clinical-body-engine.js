(function(){
"use strict";

const config=window.CLINICAL_ANIMATION_CONFIG;
if(!config)return;

const stageWrap=document.getElementById("stageWrap");
const canvas=document.getElementById("sceneCanvas");
const ctx=canvas.getContext("2d");
const stateBadge=document.getElementById("stateBadge");
const regionOut=document.getElementById("regionOut");
const clueOut=document.getElementById("clueOut");
const mechNote=document.getElementById("mechNote");
const symptomGrid=document.getElementById("symptomGrid");
const prevBtn=document.getElementById("prevBtn");
const nextBtn=document.getElementById("nextBtn");
const resetBtn=document.getElementById("resetBtn");
const playBtn=document.getElementById("playBtn");
const bodyImg=new Image();
const maskCanvas=document.createElement("canvas");
const maskCtx=maskCanvas.getContext("2d");

let cssW=0,cssH=0,dpr=Math.max(1,window.devicePixelRatio||1);
const requestedKey=new URLSearchParams(location.search).get("symptom");
let selectedKey=config.symptoms.some(x=>x.key===requestedKey)?requestedKey:(config.startKey||config.symptoms[0].key);
const initialOffset=Math.max(0,Number(new URLSearchParams(location.search).get("time"))||0);
let firstSelection=true;
let startedAt=performance.now(),pausedAt=0,paused=true;

bodyImg.src=config.bodyAsset||"assets/clinical-nervous-system.svg";
bodyImg.addEventListener("load",resizeCanvas);

function resizeCanvas(){
  const r=stageWrap.getBoundingClientRect();
  cssW=Math.max(520,Math.round(r.width));
  cssH=Math.max(380,Math.round(r.height));
  canvas.width=Math.round(cssW*dpr);canvas.height=Math.round(cssH*dpr);
  canvas.style.width=cssW+"px";canvas.style.height=cssH+"px";
  ctx.setTransform(dpr,0,0,dpr,0,0);
  maskCanvas.width=cssW;maskCanvas.height=cssH;
}
new ResizeObserver(resizeCanvas).observe(stageWrap);

const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const mix=(a,b,t)=>a+(b-a)*t;
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
const pulse=(t,s=1)=>.5+.5*Math.sin(t*s);

function hexToRgba(hex,a){
  const n=parseInt(hex.slice(1),16);
  return `rgba(${(n>>16)&255},${(n>>8)&255},${n&255},${a})`;
}
function rr(c,x,y,w,h,r){
  c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath();
}
function bodyRect(){
  const h=cssH*.91,w=h*(500/1023),cx=cssW*.59;
  return{x:cx-w/2,y:cssH*.045,w,h};
}
function bp(r,nx,ny){return{x:r.x+r.w*nx,y:r.y+r.h*ny};}

function drawBackdrop(item,t){
  const bg=ctx.createLinearGradient(0,0,cssW,cssH);
  bg.addColorStop(0,"#fbfdff");bg.addColorStop(.58,"#f2f6f9");bg.addColorStop(1,"#e8eff4");
  ctx.fillStyle=bg;ctx.fillRect(0,0,cssW,cssH);
  const halo=ctx.createRadialGradient(cssW*.59,cssH*.48,10,cssW*.59,cssH*.48,cssH*.55);
  halo.addColorStop(0,hexToRgba(item.color,.13+.03*pulse(t,1.2)));halo.addColorStop(1,"rgba(255,255,255,0)");
  ctx.fillStyle=halo;ctx.fillRect(0,0,cssW,cssH);
  ctx.fillStyle="rgba(76,102,120,.075)";
  for(let y=24;y<cssH;y+=28)for(let x=24;x<cssW;x+=28){ctx.beginPath();ctx.arc(x,y,1,0,Math.PI*2);ctx.fill();}
}

function drawBody(r,alpha=.9){
  if(!bodyImg.complete)return;
  ctx.save();ctx.shadowColor="rgba(37,58,72,.20)";ctx.shadowBlur=20;ctx.shadowOffsetY=8;ctx.globalAlpha=alpha;
  ctx.drawImage(bodyImg,r.x,r.y,r.w,r.h);ctx.restore();
}

function tintBody(r,color,alpha,top=r.y,bottom=r.y+r.h){
  if(!bodyImg.complete)return;
  maskCtx.clearRect(0,0,cssW,cssH);
  maskCtx.drawImage(bodyImg,r.x,r.y,r.w,r.h);
  maskCtx.globalCompositeOperation="source-in";
  const g=maskCtx.createLinearGradient(0,top,0,bottom);
  g.addColorStop(0,hexToRgba(color,alpha));g.addColorStop(1,hexToRgba(color,alpha*.42));
  maskCtx.fillStyle=g;maskCtx.fillRect(r.x,top,r.w,Math.max(1,bottom-top));
  maskCtx.globalCompositeOperation="source-over";
  ctx.drawImage(maskCanvas,0,0);
}

function glowDot(x,y,r,color,a=.9){
  ctx.save();ctx.shadowColor=color;ctx.shadowBlur=r*2.5;ctx.fillStyle=hexToRgba(color,a);ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.restore();
}
function ring(x,y,r,color,a=.8,lw=2){
  ctx.save();ctx.globalAlpha=a;ctx.strokeStyle=color;ctx.lineWidth=lw;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.stroke();ctx.restore();
}
function arrow(x1,y1,x2,y2,color,a=.9,lw=4){
  ctx.save();ctx.globalAlpha=a;ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=lw;ctx.lineCap="round";ctx.shadowColor=color;ctx.shadowBlur=9;
  ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  const q=Math.atan2(y2-y1,x2-x1);ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-13*Math.cos(q-.5),y2-13*Math.sin(q-.5));ctx.lineTo(x2-13*Math.cos(q+.5),y2-13*Math.sin(q+.5));ctx.closePath();ctx.fill();ctx.restore();
}
function polyPoint(points,p){
  p=clamp(p);const scaled=p*(points.length-1),i=Math.min(points.length-2,Math.floor(scaled)),f=scaled-i;
  return{x:mix(points[i].x,points[i+1].x,f),y:mix(points[i].y,points[i+1].y,f)};
}
function labelPill(x,y,text,color,active=true){
  ctx.save();ctx.font="800 11px Segoe UI, sans-serif";const w=ctx.measureText(text).width+24;
  rr(ctx,x,y-15,w,30,15);ctx.fillStyle=active?hexToRgba(color,.13):"rgba(255,255,255,.74)";ctx.fill();ctx.strokeStyle=active?hexToRgba(color,.5):"rgba(117,137,151,.28)";ctx.stroke();
  ctx.fillStyle=active?color:"#7d8c97";ctx.textAlign="left";ctx.textBaseline="middle";ctx.fillText(text,x+12,y);ctx.restore();
}
function timelineTitle(title,subtitle,color){
  const x=cssW*.065,y=cssH*.105;
  ctx.textAlign="left";ctx.textBaseline="alphabetic";ctx.fillStyle="#20313c";ctx.font="900 16px Segoe UI, sans-serif";ctx.fillText(title,x,y);
  ctx.fillStyle="#71808c";ctx.font="700 11px Segoe UI, sans-serif";ctx.fillText(subtitle,x,y+19);
  ctx.fillStyle=color;ctx.fillRect(x,y+31,58,3);
}
function progressBar(value,color,label){
  const x=cssW*.065,y=cssH*.89,w=cssW*.29;
  ctx.fillStyle="#dbe4ea";rr(ctx,x,y,w,7,4);ctx.fill();ctx.fillStyle=color;rr(ctx,x,y,w*clamp(value),7,4);ctx.fill();
  ctx.fillStyle="#61717d";ctx.font="800 10px Segoe UI, sans-serif";ctx.textAlign="left";ctx.fillText(label,x,y-10);
}

function drawAscending(item,r,t){
  const cycle=(t%8)/8,progress=ease(clamp(cycle/.78));
  const frontNorm=mix(.975,.245,progress),frontY=r.y+r.h*frontNorm;
  tintBody(r,item.color,.48,frontY,r.y+r.h);
  ctx.save();ctx.strokeStyle=hexToRgba(item.color,.88);ctx.lineWidth=5;ctx.lineCap="round";ctx.shadowColor=item.color;ctx.shadowBlur=18;
  ctx.beginPath();ctx.moveTo(r.x+r.w*.13,frontY+3);ctx.bezierCurveTo(r.x+r.w*.34,frontY-12,r.x+r.w*.66,frontY-12,r.x+r.w*.87,frontY+3);ctx.stroke();
  ctx.strokeStyle=hexToRgba(item.color,.32);ctx.lineWidth=12;ctx.beginPath();ctx.moveTo(r.x+r.w*.18,frontY+7);ctx.bezierCurveTo(r.x+r.w*.37,frontY-4,r.x+r.w*.63,frontY-4,r.x+r.w*.82,frontY+7);ctx.stroke();ctx.restore();

  const left=[bp(r,.35,.98),bp(r,.34,.83),bp(r,.39,.67),bp(r,.45,.55),bp(r,.49,.42),bp(r,.49,.25)];
  const right=left.map(p=>({x:r.x+r.w-(p.x-r.x),y:p.y}));
  for(const path of[left,right])for(let i=0;i<12;i++){
    const q=(cycle*1.9+i/12)%1;if(q<=progress+.06){const pt=polyPoint(path,q);glowDot(pt.x,pt.y,2.3+(i%3)*.45,item.color,.58+.32*pulse(t+i,3));}
  }
  arrow(r.x-r.w*.12,r.y+r.h*.91,r.x-r.w*.12,r.y+r.h*.28,item.color,.8,4);
  arrow(r.x+r.w*1.12,r.y+r.h*.91,r.x+r.w*1.12,r.y+r.h*.28,item.color,.8,4);

  timelineTitle("ASSENDAN İLERLEME","Zayıflık dalgası distaldan proksimale yükselir",item.color);
  const phases=[{n:.86,t:"1  AYAKLAR"},{n:.67,t:"2  BACAKLAR"},{n:.43,t:"3  GÖVDE / KOLLAR"},{n:.24,t:"4  BULBER / SOLUNUM"}];
  const lx=cssW*.07,base=cssH*.25,gap=cssH*.115;
  ctx.strokeStyle="rgba(104,127,143,.25)";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(lx+8,base);ctx.lineTo(lx+8,base+gap*3);ctx.stroke();
  phases.forEach((ph,i)=>{const active=frontNorm<=ph.n+.07;const y=base+i*gap;ring(lx+8,y,active?8:6,item.color,active?.95:.22,active?3:2);if(active)glowDot(lx+8,y,3.2,item.color,.9);labelPill(lx+26,y,ph.t,item.color,active);});
  if(progress>.76){const lung=bp(r,.5,.29);ring(lung.x,lung.y,r.w*.22,item.color,.45+.35*pulse(t,4),4);}
  progressBar(progress,item.color,progress<.3?"DİSTAL BAŞLANGIÇ":progress<.72?"YÜKSELEN MOTOR KAYIP":"SOLUNUM RİSKİ");
}

function drawVariants(item,r,t){
  const cycle=(t%7)/7,progress=ease(clamp(cycle/.8));
  const downY=r.y+r.h*mix(.12,.7,progress);
  tintBody(r,item.color,.24,r.y,downY);
  [[.24,.24],[.76,.24],[.37,.53],[.63,.53]].forEach((p,i)=>{const q=bp(r,p[0],p[1]);ring(q.x,q.y,12+10*pulse(t+i,2.8),item.color,.42,3);glowDot(q.x,q.y,5,item.color,.75);});
  arrow(r.x+r.w*1.12,r.y+r.h*.14,r.x+r.w*1.12,r.y+r.h*.62,item.color,.85,4);
  timelineTitle("ATİPİK DAĞILIM","Proksimal başlangıç veya kranialden aşağı ilerleme",item.color);
  labelPill(cssW*.07,cssH*.31,"OMUZ KUŞAĞI",item.color,true);labelPill(cssW*.07,cssH*.42,"KALÇA KUŞAĞI",item.color,true);labelPill(cssW*.07,cssH*.57,"DESENDAN DALGA",item.color,progress>.35);
  progressBar(progress,item.color,"VARYANT MOTOR DAĞILIM");
}

function drawMfs(item,r,t){
  const head=bp(r,.5,.09),eyeY=head.y-2,dx=Math.sin(t*2.1)*8;
  tintBody(r,item.color,.13,r.y,r.y+r.h);
  for(const s of[-1,1]){const x=head.x+s*r.w*.07;ring(x,eyeY,11,item.color,.65,2.5);glowDot(x+dx,eyeY,3,item.color,.95);}
  const kneeL=bp(r,.38,.78),kneeR=bp(r,.62,.78);[kneeL,kneeR].forEach((q,i)=>{ring(q.x,q.y,18+8*pulse(t+i,2),item.color,.25,2);ctx.strokeStyle=hexToRgba(item.color,.55);ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(q.x-10,q.y);ctx.lineTo(q.x+10,q.y);ctx.stroke();});
  const sway=Math.sin(t*1.5)*18;ctx.strokeStyle=item.color;ctx.lineWidth=4;ctx.setLineDash([8,7]);ctx.beginPath();ctx.moveTo(r.x+r.w*.18,r.y+r.h*.98);ctx.quadraticCurveTo(r.x+r.w*.5+sway,r.y+r.h*.93,r.x+r.w*.82,r.y+r.h*.98);ctx.stroke();ctx.setLineDash([]);
  timelineTitle("MILLER–FISHER TRIADI","Göz hareketi · denge · refleks",item.color);
  labelPill(cssW*.07,cssH*.33,"OFTALMOPLEJİ",item.color,true);labelPill(cssW*.07,cssH*.45,"ATAKSİ",item.color,true);labelPill(cssW*.07,cssH*.57,"AREFLEKSİ",item.color,true);
  progressBar(.66+.22*pulse(t,1),item.color,"ÜÇ BULGU BİRLİKTE");
}

function drawGait(item,r,t){
  tintBody(r,item.color,.12,r.y+r.h*.5,r.y+r.h);
  const sway=Math.sin(t*2)*24;arrow(r.x+r.w*.5,r.y+r.h*.55,r.x+r.w*.5+sway,r.y+r.h*.55,item.color,.72,4);
  const fy=r.y+r.h*.965;for(let i=0;i<7;i++){const phase=(t*1.3+i*.42)%3.2;const x=r.x-r.w*.45+i*r.w*.24,y=fy+Math.sin(i)*5;ctx.save();ctx.globalAlpha=.18+.7*(1-phase/3.2);ctx.fillStyle=item.color;ctx.translate(x,y);ctx.rotate(i%2?.12:-.12);ctx.beginPath();ctx.ellipse(0,0,7,15,0,0,Math.PI*2);ctx.fill();ctx.restore();}
  timelineTitle("DİNAMİK DENGE KAYBI","Yürüme ekseni sağa-sola salınır",item.color);
  labelPill(cssW*.07,cssH*.38,"TABAN GENİŞLER",item.color,true);labelPill(cssW*.07,cssH*.51,"GÖVDE SALINIR",item.color,true);
  progressBar(.45+.35*pulse(t,1.4),item.color,"YÜRÜYÜŞ ATAKSİSİ");
}

function spark(x,y,color,t,seed){
  const a=t*4+seed*2.1,r=8+8*pulse(t+seed,2.5);ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.strokeStyle=color;ctx.lineWidth=2;ctx.shadowColor=color;ctx.shadowBlur=10;
  for(let i=0;i<5;i++){ctx.rotate(Math.PI*2/5);ctx.beginPath();ctx.moveTo(3,0);ctx.lineTo(r*.55,0);ctx.lineTo(r,Math.sin(t*6+seed+i)*3);ctx.stroke();}ctx.restore();
}
function drawParesthesia(item,r,t){
  tintBody(r,item.color,.1,r.y,r.y+r.h);const pts=[bp(r,.07,.52),bp(r,.93,.52),bp(r,.31,.98),bp(r,.69,.98)];
  pts.forEach((q,i)=>{spark(q.x,q.y,item.color,t,i);ring(q.x,q.y,17+9*pulse(t+i,2.2),item.color,.28,2);});
  timelineTitle("DİSTAL PARESTEZİ","Elektriklenme ellerde ve ayaklarda belirgin",item.color);
  labelPill(cssW*.07,cssH*.38,"EL PARMAKLARI",item.color,true);labelPill(cssW*.07,cssH*.51,"AYAK PARMAKLARI",item.color,true);
  progressBar(.52+.3*pulse(t,1.8),item.color,"DUYUSAL YAKINMA > OBJEKTİF KAYIP");
}

function drawReflex(item,r,t){
  const pts=[bp(r,.15,.42),bp(r,.85,.42),bp(r,.38,.78),bp(r,.62,.78)];
  pts.forEach((q,i)=>{for(let k=0;k<3;k++){const phase=(t*1.35+k*.32+i*.08)%1;ring(q.x,q.y,8+phase*28,item.color,(1-phase)*.62,2.4);}ctx.save();ctx.strokeStyle=item.color;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(q.x-10,q.y-10);ctx.lineTo(q.x+10,q.y+10);ctx.stroke();ctx.restore();});
  timelineTitle("REFLEKS ARKI SÖNÜYOR","Diz ve dirsek yanıtı erken azalır",item.color);
  labelPill(cssW*.07,cssH*.38,"DİRSEK ↓",item.color,true);labelPill(cssW*.07,cssH*.51,"DİZ ↓",item.color,true);
  progressBar(.82-.55*((t%5)/5),item.color,"HİPOREFLEKSİ → AREFLEKSİ");
}

function drawFace(item,r,t){
  const h=bp(r,.5,.09);tintBody(r,item.color,.1,r.y,r.y+r.h*.23);
  for(const s of[-1,1]){const x=h.x+s*r.w*.07;ring(x,h.y+5,18+5*pulse(t+s,2.5),item.color,.55,3);}
  ctx.strokeStyle=item.color;ctx.lineWidth=4;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(h.x-18,h.y+27);ctx.quadraticCurveTo(h.x,h.y+20+4*pulse(t,2),h.x+18,h.y+27);ctx.stroke();
  timelineTitle("SİMETRİK YÜZ TUTULUMU","İki yüz yarısında eş zamanlı motor kayıp",item.color);
  labelPill(cssW*.07,cssH*.40,"SAĞ YÜZ",item.color,true);labelPill(cssW*.07,cssH*.52,"SOL YÜZ",item.color,true);
  progressBar(.55+.22*pulse(t,1.4),item.color,"BİFASİYAL ZAAF");
}

function drawBulbar(item,r,t){
  const q=bp(r,.5,.17);tintBody(r,item.color,.16,r.y+r.h*.08,r.y+r.h*.25);
  for(let i=0;i<3;i++){const phase=(t*1.4+i/3)%1;ring(q.x,q.y,10+phase*42,item.color,(1-phase)*.55,3);}
  for(let i=0;i<3;i++){ctx.strokeStyle=hexToRgba(item.color,.68-i*.16);ctx.lineWidth=3;ctx.beginPath();ctx.arc(q.x+r.w*(.22+i*.09),q.y-10,r.w*(.12+i*.05),-.45,.45);ctx.stroke();}
  timelineTitle("BULBER GÜVENLİK","Konuşma ve yutma koordinasyonu bozulur",item.color);
  labelPill(cssW*.07,cssH*.38,"DİZARTRİ",item.color,true);labelPill(cssW*.07,cssH*.51,"DİSFAJİ",item.color,true);
  progressBar(.62+.2*pulse(t,1.5),item.color,"HAVA YOLU / ASPİRASYON RİSKİ");
}

function drawPain(item,r,t){
  const spine=[bp(r,.5,.2),bp(r,.5,.35),bp(r,.5,.53),bp(r,.44,.67),bp(r,.36,.82)];
  ctx.save();ctx.strokeStyle=item.color;ctx.lineWidth=5;ctx.shadowColor=item.color;ctx.shadowBlur=12;ctx.beginPath();spine.forEach((p,i)=>i?ctx.lineTo(p.x+(i%2?6:-6),p.y):ctx.moveTo(p.x,p.y));ctx.stroke();ctx.restore();
  for(const side of[-1,1]){const p1=bp(r,.5,.52),p2=bp(r,.5+side*.19,.69),p3=bp(r,.5+side*.15,.86);ctx.strokeStyle=hexToRgba(item.color,.65+.25*pulse(t+side,3));ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(p1.x,p1.y);ctx.quadraticCurveTo(p2.x,p2.y,p3.x,p3.y);ctx.stroke();}
  timelineTitle("RADİKÜLER YAYILIM","Köklerden sırta ve ekstremitelere elektriklenme",item.color);
  labelPill(cssW*.07,cssH*.40,"SIRT AĞRISI",item.color,true);labelPill(cssW*.07,cssH*.52,"KÖK AĞRISI",item.color,true);
  progressBar(.35+.5*pulse(t,2.1),item.color,"DALGALI AĞRI ATAĞI");
}

function drawCardiac(item,r,t){
  const h=bp(r,.44,.31),beat=Math.pow(pulse(t,5),8);ring(h.x,h.y,17+beat*8,item.color,.6,3);glowDot(h.x,h.y,7+beat*4,item.color,.86);
  const x=cssW*.065,y=cssH*.51,w=cssW*.3;ctx.strokeStyle=item.color;ctx.lineWidth=3;ctx.shadowColor=item.color;ctx.shadowBlur=8;ctx.beginPath();ctx.moveTo(x,y);for(let i=0;i<=80;i++){const px=x+w*i/80;let py=y;if(i%20===10)py-=22;if(i%20===11)py+=30;if(i%20===12)py-=10;ctx.lineTo(px,py);}ctx.stroke();ctx.shadowBlur=0;
  timelineTitle("OTONOMİK DALGALANMA","Kalp hızı ve kan basıncı hızla değişir",item.color);
  labelPill(cssW*.07,cssH*.35,"TAŞİKARDİ",item.color,true);labelPill(cssW*.07,cssH*.64,"LABİL KB",item.color,true);
  progressBar(.45+.4*pulse(t,2.4),item.color,"YAKIN MONİTÖRİZASYON");
}

function drawVisceral(item,r,t){
  const gut=bp(r,.5,.45),bladder=bp(r,.5,.57);tintBody(r,item.color,.12,r.y+r.h*.35,r.y+r.h*.63);
  for(let i=0;i<4;i++){const phase=(t*.7+i/4)%1;ring(gut.x,gut.y,16+phase*42,item.color,(1-phase)*.38,3);}
  ctx.fillStyle=hexToRgba(item.color,.3+.25*pulse(t,1.6));ctx.strokeStyle=item.color;ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(bladder.x,bladder.y,22,15+5*pulse(t,1.6),0,0,Math.PI*2);ctx.fill();ctx.stroke();
  timelineTitle("VİSSERAL OTONOMİ","Motilite yavaşlar; mesane boşalması bozulur",item.color);
  labelPill(cssW*.07,cssH*.40,"İLEUS",item.color,true);labelPill(cssW*.07,cssH*.52,"MESANE",item.color,true);
  progressBar(.68-.26*pulse(t,1.2),item.color,"MOTİLİTE ↓");
}

function drawHomeostasis(item,r,t){
  const head=bp(r,.5,.08);ring(head.x,head.y,19+8*pulse(t,2),item.color,.55,3);
  for(let i=0;i<9;i++){const a=i*Math.PI*2/9+t*.2,rad=r.w*(.62+.06*pulse(t+i,1.3));const x=r.x+r.w*.5+Math.cos(a)*rad,y=r.y+r.h*.47+Math.sin(a)*r.h*.4;glowDot(x,y,2.5,item.color,.45);}
  const x=cssW*.11,y=cssH*.48;ctx.strokeStyle=item.color;ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x,y-45);ctx.lineTo(x,y+30);ctx.stroke();ctx.beginPath();ctx.arc(x,y+42,13,0,Math.PI*2);ctx.fillStyle=item.color;ctx.fill();
  timelineTitle("HOMEOSTAZ BOZULUR","Su-sodyum dengesi ve ısı kontrolü etkilenir",item.color);
  labelPill(cssW*.16,cssH*.43,"SIADH",item.color,true);labelPill(cssW*.16,cssH*.55,"ISI KONTROLÜ",item.color,true);
  progressBar(.46+.32*pulse(t,.9),item.color,"SIVI / ISI DALGALANMASI");
}

const DRAWERS={ascending:drawAscending,variants:drawVariants,mfs:drawMfs,gait:drawGait,paresthesia:drawParesthesia,reflex:drawReflex,face:drawFace,bulbar:drawBulbar,pain:drawPain,cardiac:drawCardiac,visceral:drawVisceral,homeostasis:drawHomeostasis};

function draw(t){
  if(!cssW||!cssH)return;const item=config.symptoms.find(x=>x.key===selectedKey),r=bodyRect();
  ctx.clearRect(0,0,cssW,cssH);drawBackdrop(item,t);drawBody(r,.9);(DRAWERS[item.key]||function(){})(item,r,t);
  ctx.fillStyle="rgba(68,88,102,.58)";ctx.font="800 10px Segoe UI, sans-serif";ctx.textAlign="center";ctx.fillText("PERİFERİK SİNİR SİSTEMİ",r.x+r.w*.5,cssH-11);
}

function select(key){
  selectedKey=key;const item=config.symptoms.find(x=>x.key===key);if(!item)return;
  stateBadge.textContent=item.label;stateBadge.style.color=item.color;stateBadge.style.borderColor=hexToRgba(item.color,.35);stateBadge.style.background=hexToRgba(item.color,.08);
  regionOut.textContent=item.region;clueOut.textContent=item.clue;mechNote.innerHTML=item.note;
  symptomGrid.querySelectorAll(".symptom-btn").forEach(b=>b.classList.toggle("active",b.dataset.key===key));
  const initial=firstSelection,offset=initial?initialOffset:0;firstSelection=false;
  startedAt=performance.now()-offset*1000;pausedAt=offset;paused=initial;if(playBtn)playBtn.textContent=initial?"Başlat":"Duraklat";
}
function step(delta){const i=config.symptoms.findIndex(x=>x.key===selectedKey);select(config.symptoms[(i+delta+config.symptoms.length)%config.symptoms.length].key);}
function restart(){startedAt=performance.now();pausedAt=0;paused=false;if(playBtn)playBtn.textContent="Duraklat";}
function togglePlay(){if(!playBtn)return;if(paused){startedAt=performance.now()-pausedAt*1000;paused=false;playBtn.textContent="Duraklat";}else{paused=true;playBtn.textContent=pausedAt===0?"Başlat":"Devam Et";}}

symptomGrid.addEventListener("click",e=>{const b=e.target.closest(".symptom-btn");if(b)select(b.dataset.key);});
prevBtn.addEventListener("click",()=>step(-1));nextBtn.addEventListener("click",()=>step(1));resetBtn.addEventListener("click",restart);if(playBtn)playBtn.addEventListener("click",togglePlay);

function loop(now){if(!paused)pausedAt=(now-startedAt)/1000;draw(pausedAt);requestAnimationFrame(loop);}
resizeCanvas();select(selectedKey);requestAnimationFrame(loop);
})();
