(function(){
 const $=id=>document.getElementById(id),canvas=$("scope"),ctx=canvas.getContext("2d"),wrap=$("scopeWrap");
 const C={ink:"#dce9ef",muted:"#8fa6b2",grid:"rgba(220,233,239,.10)",major:"rgba(220,233,239,.22)",cyan:"#41c4de",green:"#65c58b",yellow:"#f4e25c",red:"#ef6670",amber:"#edaa45"};
 const traces={
  ankle:{label:"Ayak bileği",lat:4.1,amp:5.8,area:28.6,dur:5.2,color:C.cyan},
  below:{label:"Fibula başı altı",lat:10.2,amp:5.6,area:27.7,dur:5.3,color:C.green},
  pop:{label:"Popliteal fossa",lat:13.4,amp:2.4,area:11.8,dur:5.5,color:C.yellow}
 };
 const params=new URLSearchParams(location.search);
 const recorded=new Set(params.get("show")==="all"?["ankle","below","pop"]:[]);
 let selected=["ankle","below","pop"].includes(params.get("trace"))?params.get("trace"):"ankle",fixed=params.has("frame")?Math.max(0,Math.min(1,+params.get("frame")||0)):null,sweeping=false,sweepStart=0,W=900,H=520,dpr=Math.max(1,devicePixelRatio||1);
 function line(x1,y1,x2,y2,c,w=1,d=[]){ctx.save();ctx.strokeStyle=c;ctx.lineWidth=w;ctx.setLineDash(d);ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();ctx.restore()}
 function label(t,x,y,s=12,c=C.ink,w=650,a="left"){ctx.fillStyle=c;ctx.font=`${w} ${s}px Segoe UI`;ctx.textAlign=a;ctx.textBaseline="middle";ctx.fillText(t,x,y)}
 function cmap(t,d){const x=t-d.lat;if(x<0)return 0;if(x<=d.dur){const u=x/d.dur;return-d.amp*Math.pow(Math.sin(Math.PI*u),1.6)}if(x<=d.dur+1.8){const u=(x-d.dur)/1.8;return d.amp*.30*Math.sin(Math.PI*u)}if(x<=d.dur+3.0){const u=(x-d.dur-1.8)/1.2;return-d.amp*.07*Math.sin(Math.PI*u)}return 0}
 function artifact(t){const g=(m,s)=>Math.exp(-.5*((t-m)/s)**2);return .9*g(.20,.035)-.75*g(.29,.05)}
 function xAt(t,l,r){return l+(r-l)*t/22}
 function drawTrace(key,top,limit){
  const d=traces[key],left=82,right=968,base=top+109,scale=13;
  for(let i=0;i<=11;i++){const x=left+(right-left)*i/11;line(x,top,x,top+145,i%2===0?C.major:C.grid)}
  for(let i=0;i<=6;i++){const y=top+i*24.2;line(left,y,right,y,i===4.5?C.major:C.grid)}
  label(d.label,left+10,top+14,12,d.color,800);if(limit>=1)label(`${d.lat.toFixed(1)} ms · ${d.amp.toFixed(1)} mV · ${d.area.toFixed(1)} mV·ms`,right-10,top+14,10.5,C.muted,700,"right");line(left,base,right,base,C.major,1.2);
  const shown=Math.min(22,22*limit),onset=xAt(d.lat,left,right),peakT=d.lat+d.dur/2,peakX=xAt(peakT,left,right),peakY=base+cmap(peakT,d)*scale;
  ctx.beginPath();let begun=false;for(let t=0;t<=shown;t+=.025){const x=xAt(t,left,right),y=base+(cmap(t,d)+artifact(t))*scale;if(!begun){ctx.moveTo(x,y);begun=true}else ctx.lineTo(x,y)}ctx.strokeStyle=d.color;ctx.lineWidth=2.1;ctx.shadowColor=d.color;ctx.shadowBlur=4;ctx.stroke();ctx.shadowBlur=0;
  if(key===selected&&limit>.49){line(onset,top+27,onset,base+9,C.green,1.4,[4,3]);label("başlangıç",onset+5,top+36,9.5,C.green,750);line(peakX,base,peakX,peakY,C.red,2);line(peakX-4,base,peakX+4,base,C.red,2);line(peakX-4,peakY,peakX+4,peakY,C.red,2);label(`${d.amp.toFixed(1)} mV`,peakX+7,(base+peakY)/2-8,9.5,C.red,800)}
 }
 function draw(){
  ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);const s=Math.min(W/1000,H/520),ox=(W-1000*s)/2,oy=(H-520*s)/2;ctx.setTransform(dpr*s,0,0,dpr*s,dpr*ox,dpr*oy);ctx.fillStyle="#071019";ctx.fillRect(0,0,1000,520);
  let p=0;if(sweeping){p=fixed===null?Math.min(1,(performance.now()-sweepStart)/1300):fixed;if(p>=1){recorded.add(selected);sweeping=false;update(false)}}
  const limit=key=>recorded.has(key)?1:sweeping&&selected===key?p:0;drawTrace("ankle",12,limit("ankle"));drawTrace("below",174,limit("below"));drawTrace("pop",336,limit("pop"));
  if(recorded.has("below")&&recorded.has("pop")){line(48,292,48,346,C.red,3);line(42,292,54,292,C.red,3);line(42,346,54,346,C.red,3);label("FİBULA BAŞI · 10 cm · 31 m/s",62,320,10,C.red,850,"left")}
  for(let i=0;i<=11;i++)label(String(i*2),82+(968-82)*i/11,498,9.5,C.muted,650,"center");label("ms",974,498,9.5,C.muted,750);
  if(sweeping)requestAnimationFrame(draw)
 }
 function update(redraw=true){
  document.querySelectorAll("#traceSeg button").forEach(b=>b.classList.toggle("active",b.dataset.trace===selected));const d=traces[selected],has=recorded.has(selected),distalReady=recorded.has("ankle")&&recorded.has("below"),headReady=recorded.has("below")&&recorded.has("pop"),all=recorded.size===3;$("siteOut").textContent=d.label;$("latOut").textContent=has?`${d.lat.toFixed(1)} ms`:"—";$("ampOut").textContent=has?`${d.amp.toFixed(1)} mV`:"—";$("distalCvOut").textContent=distalReady?"64 m/s":"—";$("headCvOut").textContent=headReady?"31 m/s":"—";$("ampDropOut").textContent=headReady?"%57":"—";$("areaDropOut").textContent=headReady?"%57":"—";$("stateBadge").textContent=all?"LOKAL TUZAK":`${recorded.size} / 3 KAYIT`;$("phaseLabel").textContent=sweeping?`${d.label} kaydediliyor`:has?`${d.label} kayıtlı`:`${d.label} uyarısı hazır`;
  $("note").innerHTML=all?"<b>Lokal tuzak paterni:</b> Bilekten fibula başı altına iletim normal. Yavaşlama ve blok yalnız fibula başı geçişinde.":recorded.size===0?"<b>Hazır:</b> Ayak bileğinde UYAR VE KAYDET'e basın; sonra daha proksimal kayıtları ekleyin.":!recorded.has("below")?"<b>Sonraki kayıt:</b> Fibula başı altını seçin ve uyarın.":!recorded.has("pop")?"<b>Sonraki kayıt:</b> Popliteal fossayı seçin; fibula başı segmentini tamamlayın.":"<b>Sonraki kayıt:</b> Ayak bileğini seçin; distal segmenti tamamlayın.";if(redraw)draw()
 }
 function stimulate(){recorded.delete(selected);sweeping=true;sweepStart=performance.now();update()}
 function resize(){const r=wrap.getBoundingClientRect();W=Math.max(620,Math.round(r.width));H=Math.max(390,Math.round(r.height));canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);draw()}
 new ResizeObserver(resize).observe(wrap);$("traceSeg").onclick=e=>{const b=e.target.closest("button");if(!b)return;sweeping=false;selected=b.dataset.trace;update()};$("stimBtn").onclick=stimulate;resize();update();
})();
