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
    / "animasyon-2-gurultu-azaltma.html"
)
TARGET = ROOT / "animations" / "impedans-gurultu" / "animasyon-2-gurultu-azaltma.html"


EXTRA_CSS = r"""
/* concept-02-box83-book-aligned */
.app{grid-template-rows:auto auto minmax(0,1fr) 56px}
.toolbar{padding:9px 18px}
.workspace{padding:10px;grid-template-columns:350px minmax(0,1fr)}
.panel-head{padding:8px 14px}
.checklist{padding:10px;gap:6px;overflow:hidden}
.chk-item{padding:7px 9px;border-radius:4px}
.chk-item input{width:16px;height:16px;margin-top:2px}
.chk-item .txt{font-size:12.5px;line-height:1.25}
.book-ref{display:grid;grid-template-columns:72px 1fr;gap:8px;align-items:center;margin-top:2px;padding:6px;background:#fff;border:1px solid var(--line)}
.book-ref img{display:block;width:72px;height:68px;object-fit:contain}
.book-ref div{font-size:10.5px;line-height:1.25;color:var(--muted)}
.book-ref b{display:block;color:var(--ink);font-size:11px;margin-bottom:2px}
.meterbar{display:grid;grid-template-columns:minmax(220px,1.4fr) repeat(3,minmax(110px,.75fr)) 95px;gap:10px;padding:8px 12px;align-items:center}
.effect-note{font-size:11px;line-height:1.25;color:var(--ink);font-weight:650}
.effect-note b{color:var(--cyan)}
.component{min-width:0}.component label{display:flex;justify-content:space-between;gap:7px;margin-bottom:4px;font-size:9.5px;color:var(--muted);font-weight:800;text-transform:uppercase}
.component-track{height:8px;background:#dbe3e8;border-radius:4px;overflow:hidden}
.component-fill{height:100%;width:100%;background:var(--red);transition:width .25s,background .25s}
.score-readout{font-size:15px;min-width:90px}
"""


BOOK_REFERENCE = r"""
<div class="book-ref">
  <img src="../figures/source-v3/fig_8_6_frayed_cable.png" alt="Şekil 8.6 yıpranmış elektrot kablosu">
  <div><b>Box 8.3 + Şekil 8.6</b>Kontrol maddeleri aynı kalır. Her tıklama yalnız toplam gürültüyü değil, hedeflediği teknik örüntüyü azaltır.</div>
</div>
"""


METERBAR = r"""
<div class="effect-note" id="effectNote"><b>Başlangıç:</b> Box 8.3 adımlarını tek tek uygulayın; hangi kayıt örüntüsünün değiştiğini izleyin.</div>
<div class="component"><label><span>Sürekli 50/60 Hz</span><output id="mainsOut">100%</output></label><div class="component-track"><div class="component-fill" id="mainsFill"></div></div></div>
<div class="component"><label><span>Kablo geçicileri</span><output id="cableOut">100%</output></label><div class="component-track"><div class="component-fill" id="cableFill"></div></div></div>
<div class="component"><label><span>Stimulus bağlaşımı</span><output id="stimOut">100%</output></label><div class="component-track"><div class="component-fill" id="stimFill"></div></div></div>
<div class="score-readout" id="scoreOut">8/8 eksik</div>
"""


SCRIPT = r"""
const checklist=document.getElementById("checklist");
const stageWrap=document.getElementById("stageWrap");
const canvas=document.getElementById("sceneCanvas");
const ctx=canvas.getContext("2d");
const scoreOut=document.getElementById("scoreOut");
const effectNote=document.getElementById("effectNote");
const mainsFill=document.getElementById("mainsFill"),cableFill=document.getElementById("cableFill"),stimFill=document.getElementById("stimFill");
const mainsOut=document.getElementById("mainsOut"),cableOut=document.getElementById("cableOut"),stimOut=document.getElementById("stimOut");
let W=0,H=0,dpr=Math.min(2,window.devicePixelRatio||1),checked=new Set(),lastFix="";
function resize(){const r=stageWrap.getBoundingClientRect();W=Math.max(500,r.width);H=Math.max(280,r.height);canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0)}
new ResizeObserver(resize).observe(stageWrap);resize();
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function gauss(x,m,s){const z=(x-m)/s;return Math.exp(-.5*z*z)}
function pseudo(x){return .5*Math.sin(x*37.1)+.28*Math.sin(x*79.3+1.2)+.15*Math.sin(x*141.7+.4)}
function dsap(t){return -.12*gauss(t,.43,.009)+.86*gauss(t,.47,.020)-.62*gauss(t,.515,.030)+.16*gauss(t,.59,.055)}
function components(){
  let mains=1,cable=1,stim=1,drift=1;
  if(checked.has("type"))mains*=.65;
  if(checked.has("wires"))cable*=.12;
  if(checked.has("clean")){mains*=.60;drift*=.45}
  if(checked.has("gel")){mains*=.60;drift*=.55}
  if(checked.has("fix")){cable*=.55;drift*=.35}
  if(checked.has("ground")){mains*=.80;stim*=.22}
  if(checked.has("coax")){cable*=.45;stim*=.50}
  if(checked.has("close"))mains*=.55;
  return{mains,cable,stim,drift}
}
const EFFECTS={
  type:"Aynı tip elektrotlar, elektrot özelliklerinden doğan giriş farkını azaltır → sürekli 50/60 Hz azalır.",
  wires:"Sağlam kablo ve bağlantı, aralıklı kesilme ile sivri temas geçicilerini azaltır.",
  clean:"Deri temizliği empedansı ve yavaş bazal kaymayı azaltır; ortak mod eşleşmesi iyileşir.",
  gel:"İletken jel elektrot–deri temasını düzeltir → empedans farkı ve 50/60 Hz azalır.",
  fix:"Elektrotların sabitlenmesi hareketle oluşan bazal kayma ve temas geçicilerini azaltır.",
  ground:"Toprağın stimülatör ile kayıt arasına yerleştirilmesi stimulusun kayıt devresine bağlaşımını azaltır.",
  coax:"Koaksiyel geometri elektromanyetik indüksiyon ile sivri stimulus/kablo geçicilerini azaltır.",
  close:"G1 ve G2 birbirine yaklaştıkça aynı çevresel alanı görür → ortak gürültü daha iyi iptal edilir."
};
function color(v){return v<.2?"#2f7d52":v<.55?"#c97a2a":"#b43b47"}
function updateStatics(){
  const c=components(),done=checked.size;
  [[mainsFill,mainsOut,c.mains],[cableFill,cableOut,c.cable],[stimFill,stimOut,c.stim]].forEach(([fill,out,v])=>{fill.style.width=`${Math.round(v*100)}%`;fill.style.background=color(v);out.textContent=`${Math.round(v*100)}%`});
  scoreOut.textContent=`${8-done}/8 eksik`;
  effectNote.innerHTML=lastFix?`<b>Son müdahale:</b> ${EFFECTS[lastFix]}`:`<b>Başlangıç:</b> Box 8.3 adımlarını tek tek uygulayın; hangi kayıt örüntüsünün değiştiğini izleyin.`;
}
function line(points,color,width=2,dash=[]){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.restore()}
function text(s,x,y,color="#b8d1c8",size=11,align="left",weight=700){ctx.fillStyle=color;ctx.font=`${weight} ${size}px Segoe UI`;ctx.textAlign=align;ctx.fillText(s,x,y);ctx.textAlign="left"}
function grid(x,y,w,h){ctx.fillStyle="#061710";ctx.fillRect(x,y,w,h);ctx.strokeStyle="#17392b";for(let i=0;i<=12;i++){const xx=x+w*i/12;ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke()}for(let i=0;i<=8;i++){const yy=y+h*i/8;ctx.beginPath();ctx.moveTo(x,yy);ctx.lineTo(x+w,yy);ctx.stroke()}ctx.strokeStyle="#2a5945";ctx.beginPath();ctx.moveTo(x,y+h/2);ctx.lineTo(x+w,y+h/2);ctx.stroke()}
function draw(){
  const c=components(),x=24,y=36,w=W-48,h=H-65;ctx.clearRect(0,0,W,H);grid(x,y,w,h);
  const now=performance.now()/1000,pts=[];
  for(let i=0;i<=800;i++){
    const t=i/800;
    const mains=.92*c.mains*Math.sin(2*Math.PI*(6*t+now*.08));
    const drift=.40*c.drift*Math.sin(2*Math.PI*(.72*t+now*.025));
    const cable=c.cable*(1.35*gauss(t,.23,.004)-1.05*gauss(t,.245,.013)+1.10*gauss(t,.74,.005)-.85*gauss(t,.755,.016));
    const stim=c.stim*(1.55*gauss(t,.055,.003)-1.15*gauss(t,.068,.012));
    const grain=.035*pseudo(t*4+now*.02);
    const v=clamp(mains+drift+cable+stim+.62*dsap(t)+grain,-1,1);
    pts.push([x+w*t,y+h/2-v*h*.41]);
  }
  line(pts,"#69dfa0",2);
  text("20 µV/div · 2 ms/div",x+10,y+18);text(`Box 8.3: ${checked.size}/8 uygulandı`,x+w-10,y+18,"#b8d1c8",11,"right");
  text("stimulus",x+w*.055,y+h-12,"#ff9aa3",10,"center");text("DSAP",x+w*.47,y+h-12,"#ffc05c",10,"center");
  const clean=c.mains<.22&&c.cable<.18&&c.stim<.2;
  text(clean?"TEKNİK OLARAK YORUMLANABİLİR KAYIT":"ÖNCE TEKNİK ZİNCİRİ DÜZELT",x+w-10,y+h-12,clean?"#79e3ac":"#ff9aa3",11,"right",800);
  requestAnimationFrame(draw);
}
checklist.addEventListener("change",e=>{
  const item=e.target.closest(".chk-item");if(!item)return;const key=item.dataset.fix;lastFix=key;
  if(e.target.checked){checked.add(key);item.classList.add("on")}else{checked.delete(key);item.classList.remove("on")}
  updateStatics();
});
updateStatics();requestAnimationFrame(draw);
"""


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    text = text.replace(
        "<title>Gürültüyü Azaltma — Box 8.3 Kontrol Listesi</title>",
        "<title>Box 8.3 — Gürültüyü örüntüsüne göre azaltma</title>",
    )
    text = text.replace(
        "2 / 2 — Gürültüyü Azaltma (Box 8.3)",
        "Kitap sırası — Box 8.3 teknik kontrol zinciri",
    )
    text = text.replace(
        '<div class="panel-head"><span>Kontrol Listesi</span></div>',
        '<div class="panel-head"><span>Box 8.3 — adımı tıkla, kayıttaki karşılığını gör</span></div>',
    )
    text = text.replace(
        '<div class="panel-head"><span>Kayıt — Uygulanan Düzeltmelere Göre</span></div>',
        '<div class="panel-head"><span>Aynı kayıt — her müdahaleden sonra</span></div>',
    )
    text = text.replace("</div>\n</div>\n\n<div class=\"panel\">", BOOK_REFERENCE + "\n</div>\n</div>\n\n<div class=\"panel\">", 1)
    text = re.sub(
        r'<div class="meterbar">.*?</div>\s*</div>\s*</div>\s*<div class="bottom-bar"',
        '<div class="meterbar">' + METERBAR + '</div>\n</div>\n</div>\n<div class="bottom-bar"',
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace("</style>", EXTRA_CSS + "\n</style>", 1)
    text = re.sub(
        r"<script>\s*const checklist=.*?</script>",
        "<script>\n" + SCRIPT + "\n</script>",
        text,
        count=1,
        flags=re.S,
    )
    TARGET.write_text(text, encoding="utf-8")
    print(TARGET)


if __name__ == "__main__":
    main()
