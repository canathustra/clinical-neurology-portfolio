(function(){
  document.documentElement.classList.add("neuroedx-signal-paper");
  if(!document.querySelector('link[data-neuroedx-system]')){
    const style=document.createElement("link");
    style.rel="stylesheet";
    style.href="assets/neuroedx-deck.css";
    style.dataset.neuroedxSystem="signal-paper-03";
    document.head.appendChild(style);
  }
  const slides=[
    ["index.html","Açılış olgusu"],
    ["gbs-acil-sendrom.html","GBS: acil sendrom"],
    ["gbs-varyantlari.html","GBS spektrumu"],
    ["animasyon-1-sendrom-agaci.html","Sendrom ağacı"],
    ["klinik-motor-refleks.html","Motor bulgular ve refleksler"],
    ["animasyon-klinik-vucut-haritasi.html","Asendan güçsüzlük haritası"],
    ["klinik-duyusal-agrili-bulgular.html","Duyusal bulgular ve ağrı"],
    ["kranial-bulgular.html","Kranial sinir tutulumu"],
    ["animasyon-kranial-otonomik-vucut-haritasi.html","Kranial-otonomik harita"],
    ["otonomik-solunumsal-izlem.html","Otonomik ve solunumsal izlem"],
    ["hastalik-seyri.html","Hastalık seyri"],
    ["animasyon-hastalik-seyri.html","Gün gün GBS"],
    ["etyoloji-tetikleyiciler.html","Etyoloji ve tetikleyiciler"],
    ["icpi-irae-baglam.html","ICPI ve nörolojik irAE"],
    ["icpi-bos-pleositoz.html","ICPI-GBS mekanizması"],
    ["icpi-bos-yorum.html","ICPI-GBS'de BOS yorumu"],
    ["bos-protein-zamanlama.html","BOS proteini ve zamanlama"],
    ["bos-pleositoz-ayirici.html","BOS hücre sayısı: alarm eşikleri"],
    ["ncs-baslangic-nasil-okunur.html","NCS ekranını okumak"],
    ["animasyon-ncs-olcum-rehberi.html","İzi ölçme laboratuvarı"],
    ["sinir-ileti-calismalari.html","İlk NCS bulguları"],
    ["animasyon-h-refleksi-a-yaniti-mekanizma.html","H refleksi ve A yanıtı mekanizması"],
    ["animasyon-erken-gec-yanitlar.html","H refleksi kayıtları"],
    ["animasyon-f-yanitlari-normal.html","Normal F yanıtları"],
    ["animasyon-f-yanitlari-aidp.html","AIDP'de F yanıtları"],
    ["motor-ncs-segmental-demiyelinizasyon.html","Motor NCS: demiyelinizasyon"],
    ["animasyon-temporal-dispersiyon-iletim-blogu.html","Temporal dispersiyon ve iletim bloğu"],
    ["iletim-blogu-ncs-ornegi.html","İletim bloğu NCS örneği"],
    ["peroneal-tuzak-ncs-ornegi.html","Fibula başında peroneal tuzak"],
    ["animasyon-ncs-zaman-cizelgesi.html","Motor NCS laboratuvarı"],
    ["duyusal-ncs-temelleri.html","Duyusal NCS temelleri"],
    ["sural-sparing.html","Sural korunma paterni"],
    ["animasyon-duyusal-ncs-segment-simulatoru.html","Seri duyusal NCS"],
    ["elektrodiagnostik-guncel-yaklasim.html","Güncel elektrodiagnostik yaklaşım"],
    ["elektrodiagnostik-kriterler.html","Ders kitabı kriterleri"],
    ["animasyon-kriter-hesaplayici.html","Kriter hesaplayıcı"],
    ["igne-emg.html","İğne EMG'ye giriş"],
    ["erken-igne-emg-bulgulari.html","Erken iğne EMG"],
    ["igne-emg-buyuk-muap-miyokimi.html","Büyük MÜAP ve miyokimi"],
    ["sekonder-aksonal-kayip.html","Sekonder aksonal kayıp"],
    ["animasyon-fibrilasyon-zaman-cizelgesi.html","İğne EMG zaman çizelgesi"],
    ["animasyon-muap-morfoloji-yakinlastirma.html","MÜAP morfolojisi"],
    ["prognoz.html","Elektrofizyolojik prognoz"],
    ["animasyon-prognoz-yorunge.html","Prognoz yörüngeleri"]
  ];
  const file=decodeURIComponent(location.pathname.split("/").pop()||"index.html");
  const index=slides.findIndex(s=>s[0]===file);
  if(index<0)return;
  document.documentElement.style.setProperty("--deck-index",index+1);
  document.documentElement.style.setProperty("--deck-percent",`${((index+1)/slides.length)*100}%`);
  const workspace=document.querySelector(".workspace");
  if(workspace)workspace.id="main-content";
  if(!document.querySelector(".neuroedx-skip")){
    const skip=document.createElement("a");
    skip.className="neuroedx-skip";
    skip.href="#main-content";
    skip.textContent="İçeriğe geç";
    document.body.prepend(skip);
  }
  const crumb=document.querySelector(".tb-left");
  if(crumb){
    crumb.classList.add("neuroedx-breadcrumb");
    crumb.setAttribute("aria-label","İçerik yolu");
    crumb.innerHTML=`<a href="https://edx.ucugur.chatgpt.site/library">Library</a><span>/</span><a href="../index.html">Cross-domain</a><span>/</span><strong>${slides[index][1]}</strong>`;
  }
  let progress=document.querySelector(".deck-progress");
  if(!progress){const host=document.querySelector(".tb-right");if(host){progress=document.createElement("span");progress.className="deck-progress";progress.style.cssText="font-variant-numeric:tabular-nums;letter-spacing:.04em;color:#53636e;margin-right:12px";host.prepend(progress)}}
  if(progress)progress.textContent=`${String(index+1).padStart(2,"0")} / ${slides.length}`;
  const bar=document.querySelector(".bottom-bar");
  if(!bar)return;
  bar.setAttribute("aria-label","Konu gezinmesi");
  const prev=index?slides[index-1]:["../index.html","İçindekiler"];
  const next=index<slides.length-1?slides[index+1]:["../index.html","İçindekiler"];
  bar.innerHTML=`<a class="fkey" href="${prev[0]}"><small>F1</small><span><strong>Previous</strong><b>${prev[1]}</b></span></a><a class="fkey" href="../index.html"><small>F2</small><span><strong>Topic home</strong><b>GBS / AIDP contents</b></span></a><a class="fkey" href="${next[0]}"><small>F3</small><span><strong>Next</strong><b>${next[1]}</b></span></a>`;

  function go(href){
    location.href=href;
  }

  function toggleFullscreen(){
    if(!document.fullscreenElement && document.documentElement.requestFullscreen){
      document.documentElement.requestFullscreen();
    }else if(document.exitFullscreen){
      document.exitFullscreen();
    }
  }

  document.addEventListener("keydown",event=>{
    const target=event.target;
    const isInteractive=target && (
      target.matches("input, textarea, select, button, a") ||
      target.isContentEditable
    );
    if(isInteractive || event.altKey || event.ctrlKey || event.metaKey)return;

    if(event.key==="ArrowLeft" || event.key==="PageUp" || event.key==="F1"){
      event.preventDefault();
      go(prev[0]);
    }else if(event.key==="ArrowRight" || event.key==="PageDown" || event.key==="F3"){
      event.preventDefault();
      go(next[0]);
    }else if(event.key==="Home" || event.key==="F2"){
      event.preventDefault();
      go("../index.html");
    }else if(event.key==="f" || event.key==="F" || event.key==="F4"){
      event.preventDefault();
      toggleFullscreen();
    }
  });
})();
