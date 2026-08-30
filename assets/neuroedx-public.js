(function(){
  const script=document.currentScript;
  if(!script)return;
  const kind=script.dataset.kind||"material";
  const domain=script.dataset.domain||"Cross-domain";
  const title=script.dataset.title||document.title;
  const canonical=script.dataset.canonical||"https://edx.ucugur.chatgpt.site/library";
  const total=Math.max(1,Number(script.dataset.total)||1);

  document.documentElement.classList.add("neuroedx-signal-paper");
  document.body.classList.add("neuroedx-public");
  const content=document.querySelector("main, #stage, #root, #muap-preview-root")||document.body;
  if(content!==document.body && !content.id)content.id="main-content";

  const skip=document.createElement("a");
  skip.className="neuroedx-skip";
  skip.href=content===document.body?"#neuroedx-dock":`#${content.id}`;
  skip.textContent="İçeriğe geç";
  document.body.prepend(skip);

  const dock=document.createElement("nav");
  dock.className="neuroedx-dock";
  dock.id="neuroedx-dock";
  dock.setAttribute("aria-label","NeuroEDX learning navigation");
  dock.innerHTML=`<div class="neuroedx-dock-crumb"><a href="https://edx.ucugur.chatgpt.site/library">Library</a><span>/</span><a href="${canonical}">${domain}</a><span>/</span><strong>${title}</strong></div><div class="neuroedx-dock-progress"><div class="neuroedx-dock-segments" aria-hidden="true"></div><b>01/${String(total).padStart(2,"0")}</b></div><div class="neuroedx-dock-nav"><button type="button" data-action="previous" aria-label="Previous">←</button><a href="${canonical}" aria-label="Topic home">⌂</a><button type="button" data-action="next" aria-label="Next">→</button></div>`;
  document.body.appendChild(dock);

  const segments=dock.querySelector(".neuroedx-dock-segments");
  const segmentCount=Math.min(total,16);
  for(let i=0;i<segmentCount;i++)segments.appendChild(document.createElement("span"));
  const readout=dock.querySelector(".neuroedx-dock-progress b");
  const previous=dock.querySelector('[data-action="previous"]');
  const next=dock.querySelector('[data-action="next"]');

  function update(position){
    const safe=Math.max(1,Math.min(total,position||1));
    readout.textContent=`${String(safe).padStart(2,"0")}/${String(total).padStart(2,"0")}`;
    readout.parentElement.setAttribute("aria-label",`Item ${safe} of ${total}`);
    [...segments.children].forEach((segment,index)=>segment.classList.toggle("active",index/segmentCount<(safe/total)));
    previous.disabled=safe<=1;
    next.disabled=safe>=total;
  }

  function hashSlide(){
    const match=location.hash.match(/^#\/(\d+)/);
    return match?Number(match[1]):1;
  }

  function dispatch(key){
    window.dispatchEvent(new KeyboardEvent("keydown",{key,bubbles:true}));
  }

  if(kind==="muap-atlas" || kind==="muap-analysis"){
    const sync=()=>update(hashSlide());
    sync();
    window.addEventListener("hashchange",sync);
    previous.addEventListener("click",()=>dispatch("ArrowLeft"));
    next.addEventListener("click",()=>dispatch("ArrowRight"));
  }else if(kind==="quantal"){
    const sync=()=>{
      const chapters=[...document.querySelectorAll(".chap")];
      const current=chapters.findIndex((chapter)=>chapter.getAttribute("aria-current")==="true");
      update(current<0?1:current+1);
    };
    const go=(delta)=>{
      const chapters=[...document.querySelectorAll(".chap")];
      const current=Math.max(0,chapters.findIndex((chapter)=>chapter.getAttribute("aria-current")==="true"));
      chapters[Math.max(0,Math.min(chapters.length-1,current+delta))]?.click();
    };
    new MutationObserver(sync).observe(document.body,{subtree:true,attributes:true,attributeFilter:["aria-current"]});
    sync();
    previous.addEventListener("click",()=>go(-1));
    next.addEventListener("click",()=>go(1));
  }else{
    update(1);
    previous.hidden=true;
    next.hidden=true;
  }
})();
