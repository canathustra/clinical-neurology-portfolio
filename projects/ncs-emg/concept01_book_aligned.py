from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\10_Projects\presentations\artifacts_of_ncs_emg"
)
SOURCE = (
    ROOT
    / "animations_ncs_emg_codex_backup_20260729_before_overlap_refinement_v4"
    / "impedans-gurultu"
    / "animasyon-1-diferansiyel-amp.html"
)
TARGET = ROOT / "animations" / "impedans-gurultu" / "animasyon-1-diferansiyel-amp.html"


EXTRA_CSS = r"""
/* concept-01-book-aligned */
.app{grid-template-rows:auto auto minmax(0,1fr) auto 56px}
.toolbar{padding:9px 18px}
.workspace{padding:10px;grid-template-columns:minmax(0,1fr) 318px}
.panel-head{padding:8px 14px}
.side-body{padding:10px;gap:8px;overflow:hidden}
.stat-row{padding:7px 10px;font-size:13px}.stat-row b{font-size:14px}
.badge-row{padding:8px 10px}.badge-row b{font-size:13px}
.note-box{padding:9px 10px;font-size:12px;line-height:1.35}
.book-link{display:grid;grid-template-columns:96px 1fr;gap:9px;align-items:center;padding:7px;background:#fff;border:1px solid var(--line)}
.book-link img{width:96px;height:86px;object-fit:contain;display:block}
.book-link div{font-size:11px;line-height:1.3;color:var(--muted)}.book-link b{display:block;color:var(--ink);font-size:12px;margin-bottom:3px}
.sequence{display:grid;grid-template-columns:repeat(3,1fr);gap:5px}
.sequence span{padding:6px;background:#eef4f6;border:1px solid var(--line);font-size:10px;line-height:1.2;color:var(--muted)}
.sequence b{display:block;color:var(--cyan);font-size:11px;margin-bottom:2px}
footer{padding:8px 18px}
"""


SIDE_BODY = r"""
<div class="sequence" aria-label="Kitaptaki neden-sonuç sırası">
  <span><b>1 · Aynı akım</b>Çevresel 50/60 Hz iki elektroda da ulaşır.</span>
  <span><b>2 · E = I × Z</b>Empedanslar farklıysa giriş voltajları eşit olmaz.</span>
  <span><b>3 · G1 − G2</b>Eşit voltaj iptal; fark ise çıkışta kalır.</span>
</div>
<div class="stat-row"><span>G1 empedansı</span><b id="r1Out">5.0 kΩ</b></div>
<div class="stat-row"><span>G2 empedansı</span><b id="r2Out">5.0 kΩ</b></div>
<div class="stat-row"><span>Empedans farkı</span><b id="deltaOut">0.0 kΩ</b></div>
<div class="stat-row"><span>Çıkışta kalan 50/60 Hz</span><b id="residOut">~0 µV</b></div>
<div class="badge-row"><span class="lbl">Sonuç</span><b id="verdictOut" class="ok">ORTAK MOD REDDİ ÇALIŞIYOR</b></div>
<div class="note-box" id="mechNote"><b>Kitap mesajı:</b> düşük empedans kadar G1 ve G2 empedanslarının birbirine yakın olması gerekir.</div>
<div class="book-link">
  <img src="../figures/source-v3/fig_8_4_differential.png" alt="Kitaptaki Şekil 8.4 diferansiyel amplifikasyon kaydı">
  <div><b>Şekil 8.4 ile aynı neden–sonuç</b>İki girişte ortak görülen voltaj çıkarılır. Uyumsuz empedans ortak gürültüyü diferansiyel hataya dönüştürür.</div>
</div>
"""


SCRIPT = r"""
const stageWrap=document.getElementById("stageWrap");
const canvas=document.getElementById("sceneCanvas");
const ctx=canvas.getContext("2d");
const sensToggle=document.getElementById("sensToggle");
const r1Out=document.getElementById("r1Out");
const r2Out=document.getElementById("r2Out");
const deltaOut=document.getElementById("deltaOut");
const residOut=document.getElementById("residOut");
const verdictOut=document.getElementById("verdictOut");
const mechNote=document.getElementById("mechNote");
const mismatchSlider=document.getElementById("mismatchSlider");
const mismatchReadout=document.getElementById("mismatchReadout");

let W=0,H=0,dpr=Math.min(2,window.devicePixelRatio||1),mismatch=0,sens="20u";
const R1=5,MAX_R2=37.5;
function resize(){
  const r=stageWrap.getBoundingClientRect();W=Math.max(500,r.width);H=Math.max(300,r.height);
  canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);
}
new ResizeObserver(resize).observe(stageWrap);resize();
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function gauss(x,m,s){const z=(x-m)/s;return Math.exp(-.5*z*z)}
function dsap(t){return -.12*gauss(t,.18,.012)+.78*gauss(t,.24,.025)-.48*gauss(t,.31,.038)+.12*gauss(t,.42,.06)}
function mains(t,a){return a*(Math.sin(2*Math.PI*(5*t+.05))+0.05*Math.sin(2*Math.PI*(15*t+.4)))}
function line(points,color,width=2,dash=[]){
  ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();
  points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.restore();
}
function text(s,x,y,color="#16232c",size=12,align="left",weight=700){
  ctx.fillStyle=color;ctx.font=`${weight} ${size}px Segoe UI`;ctx.textAlign=align;ctx.fillText(s,x,y);ctx.textAlign="left";
}
function rr(x,y,w,h,r){
  ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);
  ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();
}
function r2(){return R1+(MAX_R2-R1)*mismatch/100}
function residualUv(){const q=mismatch/100;return 26000*(q*q*q+.0115*q)}
function fmtUv(v){return v>=1000?`${(v/1000).toFixed(1)} mV`:`${v.toFixed(0)} µV`}

function drawSchematic(x,y,w,h){
  ctx.fillStyle="#fcfdfe";ctx.fillRect(x,y,w,h);
  text("AYNI ÇEVRESEL AKIM",x+w*.38,y+30,"#5c6b78",12,"center",800);
  line([[x+w*.17,y+50],[x+w*.17,y+h-30]],"#b8c2cc",2,[5,4]);
  text("Iₙ",x+w*.17,y+44,"#b43b47",13,"center",800);
  const y1=y+h*.34,y2=y+h*.70,ex=x+w*.13,rx=x+w*.32,ax=x+w*.65,ay=(y1+y2)/2,ah=h*.38;
  [["G1",y1,true,"#2f6fbd"],["G2",y2,false,"#c97a2a"]].forEach(([lab,yy,fill,c])=>{
    ctx.fillStyle=fill?"#16232c":"#fff";ctx.strokeStyle="#16232c";ctx.lineWidth=2;ctx.beginPath();ctx.arc(ex,yy,8,0,Math.PI*2);ctx.fill();ctx.stroke();
    text(lab,ex-18,yy+5,"#16232c",13,"right",800);line([[ex+9,yy],[rx-18,yy]],c,2);
  });
  const vals=[R1,r2()];
  [y1,y2].forEach((yy,i)=>{
    ctx.fillStyle="#fff";ctx.strokeStyle=i?"#c97a2a":"#2f6fbd";ctx.lineWidth=2;ctx.fillRect(rx-18,yy-20,58,40);ctx.strokeRect(rx-18,yy-20,58,40);
    text(`Z${i+1}`,rx+11,yy-3,"#5c6b78",10,"center",700);text(`${vals[i].toFixed(1)} kΩ`,rx+11,yy+13,"#16232c",11,"center",800);
    line([[rx+40,yy],[ax,ay+(i?ah*.28:-ah*.28)]],i?"#c97a2a":"#2f6fbd",2);
    text(`V${i+1}=Iₙ×Z${i+1}`,rx+45,yy-8,i?"#c97a2a":"#2f6fbd",10);
  });
  ctx.fillStyle="#fff";ctx.strokeStyle="#16232c";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(ax,ay-ah/2);ctx.lineTo(ax,ay+ah/2);ctx.lineTo(ax+ah*.75,ay);ctx.closePath();ctx.fill();ctx.stroke();
  text("−",ax+12,ay-ah*.23,"#16232c",18);text("+",ax+12,ay+ah*.33,"#16232c",17);
  text("G1 − G2",ax+ah*.40,ay+5,"#0f7a95",12,"center",800);
  line([[ax+ah*.75,ay],[x+w,ay]],"#16232c",2);
  text(mismatch<4?"V1 ≈ V2 → ortak gürültü iptal": "V1 ≠ V2 → gürültü çıkışta kalır",x+w*.52,y+h-10,mismatch<4?"#2f7d52":"#b43b47",11,"center",800);
}
function grid(x,y,w,h){
  ctx.fillStyle="#061710";ctx.fillRect(x,y,w,h);ctx.strokeStyle="#18392c";ctx.lineWidth=1;
  for(let i=0;i<=10;i++){const xx=x+w*i/10;ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke()}
  for(let i=0;i<=4;i++){const yy=y+h*i/4;ctx.beginPath();ctx.moveTo(x,yy);ctx.lineTo(x+w,yy);ctx.stroke()}
  ctx.strokeStyle="#2b5a46";ctx.beginPath();ctx.moveTo(x,y+h/2);ctx.lineTo(x+w,y+h/2);ctx.stroke();
}
function trace(x,y,w,h,fn,color,label,scaleLabel){
  grid(x,y,w,h);text(label,x+9,y+17,"#b8d1c8",11);text(scaleLabel,x+w-9,y+17,"#b8d1c8",10,"right");
  const pts=[];for(let i=0;i<=650;i++){const t=i/650;pts.push([x+w*t,clamp(y+h/2-fn(t)*h*.34,y+2,y+h-2)])}line(pts,color,2);
}
function drawTraces(x,y,w,h){
  const gap=7,row=(h-gap*2)/3,q=mismatch/100,g1Noise=.31,g2Noise=.31*(1+1.7*q),outNoise=.82*q;
  trace(x,y,w,row,t=>mains(t,g1Noise)+.52*dsap(t),"#ffc05c","G1 · ortak 50/60 Hz + hedef DSAP","şematik giriş");
  trace(x,y+row+gap,w,row,t=>mains(t,g2Noise),"#75b8ff","G2 · ortak 50/60 Hz","şematik giriş");
  let out=t=>.52*dsap(t)+mains(t,outNoise);
  if(sens==="20u"&&q>.34){
    out=t=>clamp((.52*dsap(t)+mains(t,outNoise))*4.2,-1,1);
  }else if(sens==="10m"){
    out=t=>.08*dsap(t)+mains(t,outNoise*.95);
  }
  const scale=sens==="20u"?"20 µV/div":"10 mV/div";
  trace(x,y+(row+gap)*2,w,row,out,"#79e3ac","ÇIKIŞ · G1 − G2",scale);
}
function update(){
  const R2=r2(),res=residualUv(),q=mismatch/100;
  r1Out.textContent=`${R1.toFixed(1)} kΩ`;r2Out.textContent=`${R2.toFixed(1)} kΩ`;deltaOut.textContent=`${(R2-R1).toFixed(1)} kΩ`;
  residOut.textContent=`~${fmtUv(res)}`;mismatchReadout.textContent=`%${mismatch}`;
  if(q<.04){
    verdictOut.textContent="ORTAK MOD REDDİ ÇALIŞIYOR";verdictOut.className="ok";
    mechNote.innerHTML="<b>Sonuç:</b> Aynı çevresel akım, eşit empedanslarda benzer giriş voltajları oluşturdu. G1−G2 ortak 50/60 Hz'yi iptal etti; hedef DSAP kaldı.";
  }else if(sens==="20u"&&q>.34){
    verdictOut.textContent="ÇIKIŞ DOYUYOR";verdictOut.className="bad";
    mechNote.innerHTML="<b>Sonuç:</b> G2 empedansı arttı; aynı akım artık G1 ve G2'de farklı voltaj üretiyor. Fark yükseltilince ince sensitivitede kayıt doygunlaşıyor.";
  }else{
    verdictOut.textContent=sens==="10m"?"KALAN 50/60 Hz GÖRÜNÜR":"ORTAK MOD REDDİ EKSİK";verdictOut.className="warn";
    mechNote.innerHTML=sens==="10m"?"<b>10 mV/div:</b> Doyma kalktı ve alttaki 50/60 Hz sinüsü görüldü; bu ölçekte küçük DSAP görünmez.":"<b>Sonuç:</b> Empedans farkı ortak gürültünün bir bölümünü diferansiyel çıkışa taşıdı; DSAP artık gürültünün üzerinde değerlendiriliyor.";
  }
}
function draw(){
  ctx.clearRect(0,0,W,H);ctx.fillStyle="#fcfdfe";ctx.fillRect(0,0,W,H);
  const split=W*.43;drawSchematic(0,0,split-8,H);ctx.strokeStyle="#dfe6eb";ctx.beginPath();ctx.moveTo(split,12);ctx.lineTo(split,H-12);ctx.stroke();
  drawTraces(split+16,18,W-split-30,H-36);requestAnimationFrame(draw);
}
mismatchSlider.addEventListener("input",e=>{mismatch=Number(e.target.value);update()});
sensToggle.addEventListener("click",e=>{const b=e.target.closest(".mbtn");if(!b)return;sens=b.dataset.sens;[...sensToggle.querySelectorAll(".mbtn")].forEach(x=>x.classList.toggle("active",x===b));update()});
update();requestAnimationFrame(draw);
"""


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    text = text.replace(
        "<title>Diferansiyel Amplifikasyon ve 60 Hz İnterferansı</title>",
        "<title>G1 ve G2 eşitse ortak 50/60 Hz iptal olur</title>",
    )
    text = text.replace(
        "1 / 2 — Diferansiyel Amplifikasyon ve 60 Hz",
        "Kitap sırası — Ortak mod reddi ve empedans eşleşmesi",
    )
    text = text.replace(
        "G1/G2 → Amplifikatör → Kayıt (bkz. Şekil 8.4–8.5)",
        "Aynı çevresel akım → E = I × Z → G1 − G2 → kayıt",
    )
    text = text.replace(
        '<div class="panel-head"><span>Okuma</span></div>',
        '<div class="panel-head"><span>Kitaptaki neden–sonuç</span></div>',
    )
    text = re.sub(
        r'<div class="side-body">.*?</div>\s*</div>\s*</div>\s*</div>\s*<footer>',
        '<div class="side-body">' + SIDE_BODY + '</div>\n</div>\n</div>\n<footer>',
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace("</style>", EXTRA_CSS + "\n</style>", 1)
    text = re.sub(
        r"<script>\s*const stageWrap=.*?</script>",
        "<script>\n" + SCRIPT + "\n</script>",
        text,
        count=1,
        flags=re.S,
    )
    TARGET.write_text(text, encoding="utf-8")
    print(TARGET)


if __name__ == "__main__":
    main()
