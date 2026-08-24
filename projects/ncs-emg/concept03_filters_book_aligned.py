from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(
    r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\10_Projects\presentations\artifacts_of_ncs_emg"
)
BASE = (
    ROOT
    / "animations_ncs_emg_codex_backup_20260729_before_overlap_refinement_v4"
    / "filtreler"
    / "animasyon-1-gecirgen-bant.html"
)
LIVE = ROOT / "animations"


EXTRA_CSS = r"""
/* concept-03-filter-sequence-book-aligned */
.app{grid-template-rows:auto auto minmax(0,1fr) auto 56px}
.toolbar{padding:9px 18px}
.workspace{padding:10px;grid-template-columns:minmax(0,1fr) 310px}
.panel-head{padding:8px 14px}
.same-recording{margin-left:auto;color:var(--green);font-size:11px;font-weight:800;letter-spacing:.04em}
.side-body{padding:10px;gap:8px;overflow:hidden}
.stat-row{padding:7px 10px;font-size:13px}.stat-row b{font-size:14px}
.note-box{padding:9px 10px;font-size:12px;line-height:1.35}
.source-card{display:grid;grid-template-columns:94px 1fr;gap:8px;align-items:center;padding:7px;background:#fff;border:1px solid var(--line)}
.source-card img{width:94px;height:92px;object-fit:contain;display:block}
.source-card div{font-size:10.5px;line-height:1.25;color:var(--muted)}.source-card b{display:block;color:var(--ink);font-size:11.5px;margin-bottom:2px}
footer{padding:8px 18px;gap:6px}
.footer-explain{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.footer-explain span{padding:7px 9px;background:#f8fafb;border:1px solid var(--line);font-size:11px;line-height:1.25;color:var(--muted)}
.footer-explain b{color:var(--cyan)}
.slider-row span.lbl{min-width:138px}
"""


def nav(prev_href: str, next_href: str) -> str:
    return f"""<div class="bottom-bar" aria-label="Standart sunum gezinmesi">
<a class="fkey" href="{prev_href}"><span>F1</span><b>Önceki</b></a>
<a class="fkey" href="../index.html"><span>F2</span><b>İçindekiler</b></a>
<a class="fkey" href="{next_href}"><span>F3</span><b>Sonraki</b></a>
</div>"""


def mode_buttons(items: list[tuple[str, str]], active: str) -> str:
    return "".join(
        f'<button class="mbtn{" active" if key == active else ""}" data-mode="{key}" type="button">{label}</button>'
        for key, label in items
    )


def workspace(
    stage_title: str,
    buttons: list[tuple[str, str]],
    active: str,
    stats: list[tuple[str, str, str]],
    source_image: str,
    source_title: str,
    source_text: str,
    footer: str,
) -> str:
    stat_html = "".join(
        f'<div class="stat-row"><span id="{sid}Label">{label}</span><b id="{sid}Value">{value}</b></div>'
        for sid, label, value in stats
    )
    return f"""
<div class="workspace">
  <div class="panel">
    <div class="panel-head">
      <span>{stage_title}</span>
      <div class="modetoggle" id="modeToggle">{mode_buttons(buttons, active)}</div>
      <span class="same-recording">AYNI HAM KAYIT</span>
    </div>
    <div class="stage-wrap" id="stageWrap"><canvas id="sceneCanvas"></canvas></div>
  </div>
  <div class="panel side">
    <div class="panel-head"><span>Kitapla birlikte oku</span></div>
    <div class="side-body">
      {stat_html}
      <div class="note-box" id="mechNote"></div>
      <div class="source-card">
        <img src="../figures/source-v3/{source_image}" alt="{source_title}">
        <div><b>{source_title}</b>{source_text}</div>
      </div>
    </div>
  </div>
</div>
{footer}
"""


PAGE_10 = {
    "target": LIVE / "filtreler" / "animasyon-0-filtre-spektrumu.html",
    "step": "components",
    "title": "Ham kayıt tek bir frekanstan oluşmaz",
    "toolbar": "1 / 3 — Ham kaydın frekans bileşenleri",
    "workspace": workspace(
        "Önce bileşenleri ayır: bazal kayma, 50/60 Hz, DSAP ve yüksek frekanslı gürültü",
        [
            ("all", "Tüm kayıt"),
            ("drift", "<10 Hz bazal"),
            ("mains", "50/60 Hz"),
            ("dsap", "DSAP"),
            ("hf", ">10 kHz gürültü"),
        ],
        "all",
        [
            ("stat1", "Seçilen bileşen", "Tüm ham kayıt"),
            ("stat2", "Frekans bölgesi", "1 Hz–30 kHz"),
            ("stat3", "Kayıttaki görünüm", "Bileşik iz"),
            ("stat4", "Filtre kararı", "Henüz uygulanmadı"),
        ],
        "fig_8_8_filter_stack.png",
        "Şekil 8.8 — aynı DSAP, farklı HFF ayarları",
        "Kitap önce sinyalin bir frekans spektrumu olduğunu gösterir; filtre kararı bundan sonra gelir.",
        """<footer><div class="footer-explain">
<span><b>1 · Düşük frekans</b>Bazal kayma ve hareket bileşenleri.</span>
<span><b>2 · Hedef bant</b>DSAP'ın hızlı bileşenleri.</span>
<span><b>3 · Yüksek frekans</b>Hedefi örtebilen elektriksel gürültü.</span>
</div></footer>""",
    ),
    "nav": nav("index.html", "gecirgen-bant.html"),
}


PAGE_12 = {
    "target": LIVE / "filtreler" / "animasyon-1-gecirgen-bant.html",
    "step": "passband",
    "title": "Geçirgen bant kayıt türüne göre seçilir",
    "toolbar": "2 / 3 — Motor ve duysal geçirgen bant",
    "workspace": workspace(
        "Aynı ham kayda motor veya duysal preset uygula",
        [
            ("motor", "Motor 10 Hz–10 kHz"),
            ("sensory", "Duysal 20 Hz–2 kHz"),
            ("raw", "Ham kayıt"),
        ],
        "sensory",
        [
            ("stat1", "Alçak kesim (LFF)", "20 Hz"),
            ("stat2", "Yüksek kesim (HFF)", "2 kHz"),
            ("stat3", "DSAP amplitüdü", "30 µV"),
            ("stat4", "Süre / SNR", "1.00× / uygun"),
        ],
        "fig_8_7_passband.png",
        "Şekil 8.7 — geçirgen bant keskin bir duvar değildir",
        "Motor için 10 Hz–10 kHz; duysal için 20 Hz–2 kHz tipik başlangıç ayarlarıdır.",
        """<footer>
<div class="slider-row"><span class="lbl">Alçak kesim (LFF)</span><input id="lffSlider" type="range" min="1" max="100" step="1" value="20"><span class="val" id="lffVal">20 Hz</span></div>
<div class="slider-row"><span class="lbl">Yüksek kesim (HFF)</span><input id="hffSlider" type="range" min="500" max="10000" step="100" value="2000"><span class="val" id="hffVal">2 kHz</span></div>
</footer>""",
    ),
    "nav": nav("gecirgen-bant.html", "filtre-odunlesimi.html"),
}


PAGE_14 = {
    "target": LIVE / "filtreler" / "animasyon-2-filtre-odunlesimi.html",
    "step": "tradeoff",
    "title": "Filtre değişince amplitüd ve süre de değişir",
    "toolbar": "3 / 3 — Şekil 8.9 ile filtre ödünleşimi",
    "workspace": workspace(
        "Standart kaydı seçilen filtreyle üst üste karşılaştır",
        [
            ("hff500", "HFF 0.5 kHz"),
            ("standard", "Standart 20 Hz–2 kHz"),
            ("lff2", "LFF 2 Hz"),
        ],
        "hff500",
        [
            ("stat1", "Standart amplitüd", "30 µV"),
            ("stat2", "Seçilen amplitüd", "16 µV"),
            ("stat3", "Amplitüd farkı", "−14 µV"),
            ("stat4", "Süre değişimi", "1.00×"),
        ],
        "fig_8_9_filter_tradeoff.png",
        "Şekil 8.9 — HFF 2 kHz→0.5 kHz: 30→16 µV",
        "Filtre değişikliğinden sonra oluşan amplitüd veya süre farkı patoloji olarak yorumlanmaz.",
        """<footer>
<div class="slider-row"><span class="lbl">Alçak kesim (LFF)</span><input id="lffSlider" type="range" min="1" max="100" step="1" value="20"><span class="val" id="lffVal">20 Hz</span></div>
<div class="slider-row"><span class="lbl">Yüksek kesim (HFF)</span><input id="hffSlider" type="range" min="500" max="3000" step="100" value="500"><span class="val" id="hffVal">0.5 kHz</span></div>
</footer>""",
    ),
    "nav": nav("filtre-odunlesimi.html", "../elektronik-ortalama/index.html"),
}


SCRIPT = r"""
const STEP=document.body.dataset.filterStep;
const stageWrap=document.getElementById("stageWrap"),canvas=document.getElementById("sceneCanvas"),ctx=canvas.getContext("2d");
const modeToggle=document.getElementById("modeToggle"),mechNote=document.getElementById("mechNote");
const lffSlider=document.getElementById("lffSlider"),hffSlider=document.getElementById("hffSlider");
const lffVal=document.getElementById("lffVal"),hffVal=document.getElementById("hffVal");
const labels=[1,2,3,4].map(i=>document.getElementById(`stat${i}Label`)),values=[1,2,3,4].map(i=>document.getElementById(`stat${i}Value`));
let W=0,H=0,dpr=Math.min(2,devicePixelRatio||1),mode=document.querySelector(".mbtn.active")?.dataset.mode||"all",lff=Number(lffSlider?.value||1),hff=Number(hffSlider?.value||30000);
function resize(){const r=stageWrap.getBoundingClientRect();W=Math.max(600,r.width);H=Math.max(320,r.height);canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0)}
new ResizeObserver(resize).observe(stageWrap);resize();
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function gauss(x,m,s){const z=(x-m)/s;return Math.exp(-.5*z*z)}
function pseudo(x){return .52*Math.sin(37.1*x)+.27*Math.sin(83.7*x+1.1)+.13*Math.sin(151.3*x+.4)}
function drift(t){return .24*Math.sin(2*Math.PI*(.65*t+.12))}
function mains(t){return .18*Math.sin(2*Math.PI*(6*t+.05))}
function hf(t){return .11*pseudo(t*4.5)}
function snap(t,amp=1,width=1){return amp*(-.12*gauss(t,.43,.010*width)+1.0*gauss(t,.47,.021*width)-.72*gauss(t,.52,.032*width)+.18*gauss(t,.60,.06*width))}
function raw(t){return drift(t)+mains(t)+hf(t)+snap(t,.72,1)}
function ampFromHff(v){if(v<=500)return 16;if(v<=2000)return 16+14*Math.log(v/500)/Math.log(4);return Math.min(34,30+4*Math.log(v/2000)/Math.log(5))}
function durFromLff(v){return 1+.24*(1-clamp(v/20,0,1))}
function filtered(t,lo=lff,hi=hff){const amp=ampFromHff(hi)/30,dur=durFromLff(lo),wander=.22*clamp((20-lo)/19,0,1),mainsKeep=.10+.12*clamp((20-lo)/20,0,1),noise=.025+.085*clamp((hi-500)/9500,0,1);return wander*drift(t)+mainsKeep*mains(t)+noise/0.11*hf(t)+amp*snap(t,.72,dur)}
function line(points,color,width=2,dash=[]){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.restore()}
function text(s,x,y,color="#16232c",size=11,align="left",weight=700){ctx.fillStyle=color;ctx.font=`${weight} ${size}px Segoe UI`;ctx.textAlign=align;ctx.fillText(s,x,y);ctx.textAlign="left"}
function grid(x,y,w,h){ctx.fillStyle="#061710";ctx.fillRect(x,y,w,h);ctx.strokeStyle="#17392b";for(let i=0;i<=12;i++){const xx=x+w*i/12;ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke()}for(let i=0;i<=6;i++){const yy=y+h*i/6;ctx.beginPath();ctx.moveTo(x,yy);ctx.lineTo(x+w,yy);ctx.stroke()}ctx.strokeStyle="#2a5945";ctx.beginPath();ctx.moveTo(x,y+h/2);ctx.lineTo(x+w,y+h/2);ctx.stroke()}
function scope(x,y,w,h,fn,color,label,dash=[]){grid(x,y,w,h);const pts=[];for(let i=0;i<=700;i++){const t=i/700;pts.push([x+w*t,clamp(y+h/2-fn(t)*h*.38,y+2,y+h-2)])}line(pts,color,2,dash);text(label,x+9,y+17,"#b8d1c8",11)}
const fMin=1,fMax=100000;
function fx(f,x,w){return x+w*(Math.log10(f)-Math.log10(fMin))/(Math.log10(fMax)-Math.log10(fMin))}
function axes(x,y,w,h){ctx.strokeStyle="#aebcc7";ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x,y+h);ctx.lineTo(x+w,y+h);ctx.stroke();[1,10,100,1000,10000,100000].forEach(f=>{const xx=fx(f,x,w);ctx.beginPath();ctx.moveTo(xx,y+h);ctx.lineTo(xx,y+h+5);ctx.stroke();text(f>=1000?`${f/1000}k`:`${f}`,xx,y+h+18,"#5c6b78",10,"center")})}
function drawComponents(){
  const x=55,y=45,w=W-110,h=H*.36;axes(x,y,w,h);
  const bands=[
    ["drift",1,10,"#c97a2a","Bazal kayma <10 Hz"],
    ["mains",45,65,"#b43b47","50/60 Hz"],
    ["dsap",200,2500,"#2f7d52","DSAP ana bileşenleri"],
    ["hf",10000,100000,"#2f6fbd","HF gürültü >10 kHz"]
  ];
  bands.forEach(([key,a,b,c,label],i)=>{const active=mode==="all"||mode===key,xa=fx(a,x,w),xb=fx(b,x,w);ctx.globalAlpha=active?1:.18;ctx.fillStyle=c;ctx.fillRect(xa,y+18+i*25,Math.max(4,xb-xa),16);text(label,xa+4,y+30+i*25,"#16232c",10);ctx.globalAlpha=1});
  const fns={all:raw,drift,mains,dsap:t=>snap(t,.72,1),hf};
  scope(25,H*.50,W-50,H*.43,fns[mode]||raw,"#69dfa0",mode==="all"?"AYNI HAM KAYIT · bütün bileşenler birlikte":`İZOLE BİLEŞEN · ${mode}`);
}
function passStrength(f){const rise=1/(1+Math.pow(lff/f,4)),fall=1/(1+Math.pow(f/hff,4));return Math.sqrt(rise*fall)}
function drawPassband(overlay=false){
  const x=55,y=38,w=W-110,h=H*.32;axes(x,y,w,h);const pts=[];
  for(let i=0;i<=500;i++){const f=Math.pow(10,5*i/500);pts.push([fx(f,x,w),y+h-passStrength(f)*(h-15)])}line(pts,"#2f6fbd",3);
  ctx.strokeStyle="#b43b47";ctx.setLineDash([5,4]);[lff,hff].forEach(f=>{const xx=fx(f,x,w);ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke()});ctx.setLineDash([]);
  text(`LFF ${lff} Hz`,fx(lff,x,w)+4,y+15,"#b43b47",10);text(`HFF ${hff>=1000?(hff/1000).toFixed(1)+" kHz":hff+" Hz"}`,fx(hff,x,w)-4,y+15,"#b43b47",10,"right");
  const sy=H*.43,sh=H*.48;
  if(overlay){
    grid(25,sy,W-50,sh);const ref=[],sel=[];
    for(let i=0;i<=700;i++){const t=i/700;ref.push([25+(W-50)*t,sy+sh/2-filtered(t,20,2000)*sh*.38]);sel.push([25+(W-50)*t,sy+sh/2-filtered(t,lff,hff)*sh*.38])}
    line(ref,"#ffc05c",2,[7,5]);line(sel,"#69dfa0",2);text("KESİKLİ: standart 20 Hz–2 kHz",36,sy+18,"#ffc05c",10);text("DÜZ: seçilen filtre",36,sy+35,"#69dfa0",10);
  }else{
    grid(25,sy,W-50,sh);const rawPts=[],filPts=[];
    for(let i=0;i<=700;i++){const t=i/700;rawPts.push([25+(W-50)*t,sy+sh/2-raw(t)*sh*.30]);filPts.push([25+(W-50)*t,sy+sh/2-filtered(t)*sh*.38])}
    line(rawPts,"#ffc05c",1.7,[6,5]);line(filPts,"#69dfa0",2);text("KESİKLİ: ham kayıt",36,sy+18,"#ffc05c",10);text("DÜZ: filtrelenmiş kayıt",36,sy+35,"#69dfa0",10);
  }
}
function setStat(i,label,value){labels[i].textContent=label;values[i].textContent=value}
function update(){
  if(lffSlider){lff=Number(lffSlider.value);lffVal.textContent=`${lff} Hz`}
  if(hffSlider){hff=Number(hffSlider.value);hffVal.textContent=hff>=1000?`${(hff/1000).toFixed(1)} kHz`:`${hff} Hz`}
  if(STEP==="components"){
    const info={
      all:["Tüm ham kayıt","1 Hz–30 kHz","Bileşik iz","Henüz uygulanmadı","Ham kayıt, hedef yanıt ile istenmeyen bileşenleri aynı anda taşır. Önce hangi frekansın hangi görünümü oluşturduğunu ayırın."],
      drift:["Bazal kayma","<10 Hz","Yavaş taban gezinmesi","LFF etkiler","Alçak kesim filtresi yükseltildiğinde yavaş bazal bileşenler azalır; ancak hedef potansiyelin düşük frekans içeriği de değişebilir."],
      mains:["Şebeke gürültüsü","50/60 Hz","Periyodik sinüs","Empedans/CMRR önce","50/60 Hz yalnız filtre sorunu değildir. Elektrot empedansı ve ortak mod zinciri düzeltilmeden filtreyle bastırmak hedef yanıtı da değiştirebilir."],
      dsap:["Hedef DSAP","≈200 Hz–2.5 kHz","Hızlı çok fazlı yanıt","Bant içinde korunmalı","DSAP geniş bir frekans bandı taşır; dar bir bant hedef yanıtın amplitüd ve süresini değiştirir."],
      hf:["Yüksek frekans gürültüsü",">10 kHz","İnce hızlı titreşim","HFF etkiler","Yüksek kesim filtresi HF gürültüyü azaltır; fazla düşürülürse DSAP'ın hızlı bileşenleri ve amplitüdü de azalır."]
    }[mode];for(let i=0;i<4;i++)values[i].textContent=info[i];mechNote.innerHTML=`<b>Kitap mesajı:</b> ${info[4]}`;
  }else{
    const amp=ampFromHff(hff),dur=durFromLff(lff),snr=hff>6000?"gürültülü":hff<800?"temiz fakat atenüe":"uygun";
    if(STEP==="passband"){
      setStat(0,"Alçak kesim (LFF)",`${lff} Hz`);setStat(1,"Yüksek kesim (HFF)",hff>=1000?`${(hff/1000).toFixed(1)} kHz`:`${hff} Hz`);
      setStat(2,"DSAP amplitüdü",`${amp.toFixed(0)} µV`);setStat(3,"Süre / SNR",`${dur.toFixed(2)}× / ${snr}`);
      mechNote.innerHTML=mode==="motor"?"<b>Motor preset:</b> 10 Hz–10 kHz, motor potansiyelin geniş frekans içeriğini korur; aynı DSAP kaydı daha fazla HF gürültü içerir.":mode==="raw"?"<b>Ham kayıt:</b> filtre uygulanmadığında bazal kayma ve yüksek frekanslı gürültü hedef yanıtla birlikte görünür.":"<b>Duysal preset:</b> 20 Hz–2 kHz, küçük DSAP için gürültü ile hedef yanıt arasında dengeli başlangıç ayarıdır.";
    }else{
      setStat(0,"Standart amplitüd","30 µV");setStat(1,"Seçilen amplitüd",`${amp.toFixed(0)} µV`);setStat(2,"Amplitüd farkı",`${amp-30>=0?"+":""}${(amp-30).toFixed(0)} µV`);setStat(3,"Süre değişimi",`${dur.toFixed(2)}×`);
      mechNote.innerHTML=hff<=600?"<b>Şekil 8.9:</b> HFF 2 kHz'den 0.5 kHz'ye düşünce yüksek frekanslı DSAP bileşenleri atenüe olur; amplitüd 30 µV'den 16 µV'ye iner.":lff<5?"<b>Düşük LFF:</b> daha fazla düşük frekans bileşeni geçer; potansiyel süresi uzar.":"<b>Standart ayar:</b> seçilen kayıt, 20 Hz–2 kHz referansıyla örtüşür.";
    }
  }
}
function applyMode(next){
  mode=next;document.querySelectorAll(".mbtn").forEach(b=>b.classList.toggle("active",b.dataset.mode===mode));
  if(STEP==="passband"){if(mode==="motor"){lff=10;hff=10000}else if(mode==="sensory"){lff=20;hff=2000}else{lff=1;hff=10000}}
  if(STEP==="tradeoff"){if(mode==="hff500"){lff=20;hff=500}else if(mode==="standard"){lff=20;hff=2000}else{lff=2;hff=2000}}
  if(lffSlider)lffSlider.value=lff;if(hffSlider)hffSlider.value=hff;update();
}
modeToggle.addEventListener("click",e=>{const b=e.target.closest(".mbtn");if(b)applyMode(b.dataset.mode)});
[lffSlider,hffSlider].filter(Boolean).forEach(s=>s.addEventListener("input",()=>{mode="custom";document.querySelectorAll(".mbtn").forEach(b=>b.classList.remove("active"));update()}));
function draw(){ctx.clearRect(0,0,W,H);ctx.fillStyle="#fcfdfe";ctx.fillRect(0,0,W,H);if(STEP==="components")drawComponents();else drawPassband(STEP==="tradeoff");requestAnimationFrame(draw)}
applyMode(mode);requestAnimationFrame(draw);
"""


def build(page: dict) -> None:
    text = BASE.read_text(encoding="utf-8")
    text = re.sub(r"<title>.*?</title>", f"<title>{page['title']}</title>", text, count=1)
    text = text.replace(
        "1 / 1 — Geçirgen Bant ve Ödünleşim",
        page["toolbar"],
    )
    text = text.replace("<body>", f'<body data-filter-step="{page["step"]}">', 1)
    text = re.sub(
        r'<div class="workspace">.*?</footer>',
        page["workspace"],
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<div class="bottom-bar"[^>]*>.*?</div>',
        page["nav"],
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
    page["target"].write_text(text, encoding="utf-8")


def main() -> None:
    for page in (PAGE_10, PAGE_12, PAGE_14):
        build(page)
        print(page["target"])


if __name__ == "__main__":
    main()
