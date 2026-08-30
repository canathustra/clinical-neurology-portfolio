(function(){
  const script=document.currentScript;
  if(!script)return;
  const index=Math.max(1,Number(script.dataset.index)||1);
  const total=Math.max(index,Number(script.dataset.total)||1);
  const label=script.dataset.label||document.title.split("—")[0].trim();
  const canonical=script.dataset.canonical||"https://edx.ucugur.chatgpt.site/library/ncs/technical-factors";

  document.documentElement.classList.add("neuroedx-signal-paper");
  document.documentElement.style.setProperty("--neuroedx-progress",`${index/total*100}%`);
  document.body.classList.add("neuroedx-adapted");

  const content=document.querySelector(".workspace, main, .app");
  if(content && !content.id)content.id="main-content";
  if(content && !document.querySelector(".neuroedx-skip")){
    const skip=document.createElement("a");
    skip.className="neuroedx-skip";
    skip.href=`#${content.id}`;
    skip.textContent="İçeriğe geç";
    document.body.prepend(skip);
  }

  const crumb=document.querySelector(".tb-left");
  if(crumb){
    crumb.classList.add("neuroedx-breadcrumb");
    crumb.setAttribute("aria-label","İçerik yolu");
    crumb.innerHTML=`<a href="https://edx.ucugur.chatgpt.site/library">Library</a><span>/</span><a href="${canonical}">NCS</a><span>/</span><strong>${label}</strong>`;
  }

  const progress=document.createElement("span");
  progress.className="neuroedx-progress";
  progress.textContent=`${String(index).padStart(2,"0")} / ${String(total).padStart(2,"0")}`;
  progress.setAttribute("aria-label",`Bölüm adımı ${index} / ${total}`);
  const progressHost=document.querySelector(".tb-right, .titlebar");
  if(progressHost && !progressHost.querySelector(".neuroedx-progress"))progressHost.prepend(progress);

  const links=Array.from(document.querySelectorAll("a.fkey"));
  if(!links.length)return;
  const bar=links[0].parentElement;
  if(!bar)return;
  bar.classList.add("neuroedx-bottom-bar");
  bar.setAttribute("aria-label","Konu gezinmesi");

  links.forEach((link,position)=>{
    const old=(link.querySelector("b")?.textContent||link.textContent||"").trim();
    const isFirst=position===0;
    const isLast=position===links.length-1;
    const key=isFirst?"F1":isLast?"F3":"F2";
    const action=isFirst?"Previous":isLast?"Next":"Topic home";
    const cleaned=old.replace(/^(Önceki|Sıradaki|Sonraki|İçindekiler|Ana sayfa)\s*:?\s*/i,"")||label;
    link.innerHTML=`<small>${key}</small><span><strong>${action}</strong><b>${cleaned}</b></span>`;
    link.setAttribute("aria-label",`${action}: ${cleaned}`);
  });
})();
