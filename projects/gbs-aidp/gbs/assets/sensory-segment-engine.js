(function(){
 const $=id=>document.getElementById(id),Wv=window.NCSWave,canvas=$("scope"),ctx=canvas.getContext("2d"),wrap=$("scopeWrap");
 const order=["median","ulnar","sural"];
 const nerves={
  median:{label:"Median · 2. parmak",baseAmp:22.4,lat:2.8,dur:.72,lln:15},
  ulnar:{label:"Ulnar · 5. parmak",baseAmp:18.6,lat:2.7,dur:.70,lln:12},
  sural:{label:"Sural",baseAmp:16.8,lat:3.1,dur:.82,lln:10}
 };
 const days={0:{median:1,ulnar:1,sural:1},3:{median:.96,ulnar:.97,sural:.99},7:{median:.72,ulnar:.78,sural:.98},14:{median:.38,ulnar:.44,sural:.94},21:{median:.24,ulnar:.31,sural:.86}};
 let day=0,nerve="median",seen=new URLSearchParams(location.search).has("demo")?new Set(order.map(k=>`0-${k}`)):new Set(),sweep=null,W=900,H=520,dpr=Math.max(1,devicePixelRatio||1);
 function key(k=nerve){return `${day}-${k}`}
 function cfg(k=nerve){const n=nerves[k],factor=days[day][k],amp=n.baseAmp*factor,lat=n.lat+(day>=14&&k!=="sural"?.12:0),dur=n.dur*(1+(1-factor)*.22),width=.18+(dur-.70)*.10;return{...n,key:k,amp,lat,dur,width}}
 function active(id,k,v){document.querySelectorAll(`#${id} button`).forEach(b=>b.classList.toggle("active",b.dataset[k]===String(v)))}
 function resize(){const r=wrap.getBoundingClientRect();W=Math.max(620,Math.round(r.width));H=Math.max(400,Math.round(r.height));canvas.width=W*dpr;canvas.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);draw()}
 new ResizeObserver(resize).observe(wrap);
 function grid(x0,y0,x1,y1,lh){ctx.fillStyle="#050a12";ctx.fillRect(x0,y0,x1-x0,y1-y0);for(let i=0;i<=50;i++){ctx.strokeStyle=i%5===0?"rgba(238,244,248,.30)":"rgba(214,225,234,.09)";ctx.lineWidth=1;const x=x0+(x1-x0)*i/50;ctx.beginPath();ctx.moveTo(x,y0);ctx.lineTo(x,y1);ctx.stroke()}for(let i=0;i<=10;i++){ctx.strokeStyle=i%2===0?"rgba(238,244,248,.28)":"rgba(214,225,234,.09)";const y=y0+lh*i/10;ctx.beginPath();ctx.moveTo(x0,y);ctx.lineTo(x1,y);ctx.stroke()}}
 function value(t,c,seed){return Wv.artifact(t,.55)+Wv.snap(t,{latency:c.lat,amplitude:c.amp,width:c.width})+Wv.noise(t,seed,.10)}
 function trace(x0,x1,mid,c,seed,limit,scale,color){ctx.beginPath();const n=1000;for(let i=0;i<=n*limit;i++){const t=8*i/n,x=x0+(x1-x0)*i/n,y=mid+value(t,c,seed)*scale;i?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.strokeStyle=color;ctx.lineWidth=color==="#ffe84a"?1.9:1.5;ctx.stroke()}
 function dot(x,y,color){ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,3.5,0,Math.PI*2);ctx.fill()}
 function measurements(x0,x1,y,lh,mid,c,scale,selected){
  const map=t=>x0+(x1-x0)*t/8,onX=map(c.lat),negX=map(c.lat+c.width*1.2),posX=map(c.lat+c.width*3.3);
  const negY=mid-.56*c.amp*scale,posY=mid+.44*c.amp*scale,color=c.amp>=c.lln?"#65e09c":"#ff7b86";
  ctx.strokeStyle=color;ctx.setLineDash([4,3]);ctx.beginPath();ctx.moveTo(onX,y+7);ctx.lineTo(onX,y+lh-7);ctx.stroke();ctx.setLineDash([]);dot(onX,mid,color);dot(negX,negY,color);dot(posX,posY,color);
  ctx.fillStyle=color;ctx.font="800 10.5px Segoe UI";ctx.textAlign="left";ctx.fillText(`${c.lat.toFixed(2)} ms`,onX+4,y+14);
  if(selected){const bx=posX+15;ctx.lineWidth=1.6;ctx.beginPath();ctx.moveTo(negX,negY);ctx.lineTo(bx,negY);ctx.moveTo(posX,posY);ctx.lineTo(bx,posY);ctx.moveTo(bx,negY);ctx.lineTo(bx,posY);ctx.stroke();ctx.fillText(`${c.amp.toFixed(1)} µV`,bx+4,(negY+posY)/2+4)}
 }
 function draw(){
  ctx.clearRect(0,0,W,H);const x0=145,x1=W-18,top=18,gap=12,lh=(H-50-gap*2)/3,scale=lh/28;
  order.forEach((k,i)=>{const c=cfg(k),y=top+i*(lh+gap),mid=y+lh/2,done=seen.has(key(k));grid(x0,y,x1,y+lh,lh);ctx.strokeStyle="rgba(238,244,248,.28)";ctx.beginPath();ctx.moveTo(x0,mid);ctx.lineTo(x1,mid);ctx.stroke();ctx.fillStyle=k===nerve?"#ffe84a":done?"#bd72ff":"#82909b";ctx.font=`${k===nerve?850:700} 13px Segoe UI`;ctx.textAlign="right";ctx.fillText(c.label,x0-10,mid-6);ctx.fillStyle="#b6c4ce";ctx.font="700 11px Segoe UI";ctx.fillText(`Distal · ${c.amp.toFixed(1)} µV · LLN ${c.lln}`,x0-10,mid+13);if(done){const live=sweep&&sweep.nerve===k,lim=live?sweep.progress:1,color=live?"#ffffff":k===nerve?"#ffe84a":"#bd72ff";trace(x0,x1,mid,c,i+day+4,lim,scale,color);if(!live)measurements(x0,x1,y,lh,mid,c,scale,k===nerve)}})
 }
 function update(){
  active("timeSeg","day",day);active("nerveSeg","nerve",nerve);const c=cfg(),done=seen.has(key()),dayCount=order.filter(k=>seen.has(key(k))).length;
  $("scopeTitle").textContent=`Median · Ulnar · Sural — Gün ${day}`;$("phaseLabel").textContent=`${c.label} · distal uyarım`;$("stateBadge").textContent=`${dayCount} / 3 kayıt`;
  $("latOut").textContent=done?c.lat.toFixed(2)+" ms":"—";$("ampOut").textContent=done?c.amp.toFixed(1)+" µV":"—";$("durOut").textContent=done?c.dur.toFixed(2)+" ms":"—";$("llnOut").textContent=c.lln+" µV";$("statusOut").textContent=done?(c.amp>=c.lln?"Korunmuş":"Düşük"):"—";
  if(done){if(day<=3)$("note").innerHTML="<b>Erken kayıt:</b> Distal duyusal yanıtlar normaldir; bu bulgu AIDP'yi dışlamaz.";else if(nerve==="sural")$("note").innerHTML="<b>Sural korunma:</b> Median ve ulnar DSAP azalırken sural DSAP görece korunur.";else $("note").innerHTML="<b>Üst ekstremite DSAP azalması:</b> Sural yanıtla aynı gün ve aynı teknikle karşılaştırın."}else $("note").innerHTML=`<b>${c.label} hazır:</b> Distal uyarımla DSAP'ı kaydet.`;
  $("stimBtn").disabled=!!sweep;draw()
 }
 function stimulate(){if(sweep)return;seen.add(key());sweep={nerve,start:performance.now(),progress:0};update();requestAnimationFrame(function tick(t){sweep.progress=Math.min(1,(t-sweep.start)/620);draw();if(sweep.progress<1)requestAnimationFrame(tick);else{sweep=null;update()}})}
 $("timeSeg").onclick=e=>{const b=e.target.closest("button");if(!b)return;day=+b.dataset.day;update()};
 $("nerveSeg").onclick=e=>{const b=e.target.closest("button");if(!b)return;nerve=b.dataset.nerve;update()};
 $("stimBtn").onclick=stimulate;$("clearBtn").onclick=()=>{seen.clear();sweep=null;update()};resize();update();
})();
