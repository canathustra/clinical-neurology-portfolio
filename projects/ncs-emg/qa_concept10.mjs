import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\katot-polarite\\animasyon-0-depolarizasyon-anodal-blok.html";
const out = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser = await chromium.launch({headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]});
const page = await browser.newPage({viewport:{width:1600,height:900}});
const errors=[];
page.on("pageerror",e=>errors.push(`pageerror: ${e.message}`));
page.on("console",m=>{if(m.type()==="error")errors.push(`console: ${m.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(300);

async function sample(name){
  const state=await page.evaluate(()=>window.__anodalBlockState);
  const ui=await page.evaluate(()=>({badge:document.querySelector("#stateBadge")?.textContent?.trim(),fiber:document.querySelector("#fiberOut")?.textContent?.trim(),arrival:document.querySelector("#arrivalOut")?.textContent?.trim(),amp:document.querySelector("#ampOut")?.textContent?.trim(),lesson:document.querySelector("#lesson")?.textContent?.trim()}));
  await page.screenshot({path:path.join(out,`concept10_${name}.png`)});
  return{state,ui};
}
const pass=await sample("pass");
await page.click("#partialBtn");await page.waitForTimeout(120);const partial=await sample("partial");
await page.click("#blockBtn");await page.waitForTimeout(120);const blocked=await sample("blocked");
await page.click("#partialBtn");await page.click("#stimBtn");await page.waitForTimeout(930);await page.screenshot({path:path.join(out,"concept10_partial_travel.png")});

const metrics=await page.evaluate(()=>{
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),rect=nav?.getBoundingClientRect();
  return{overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:rect?Math.round(rect.bottom):null,imageFailures:[...document.images].filter(img=>!img.complete||!img.naturalWidth).length,geo:{width:document.querySelector("#geoCanvas")?.width,height:document.querySelector("#geoCanvas")?.height},scope:{width:document.querySelector("#scopeCanvas")?.width,height:document.querySelector("#scopeCanvas")?.height},buttons:document.querySelectorAll(".controls button").length,warning:document.querySelector(".warning")?.textContent?.trim(),sourceAlt:document.querySelector(".source img")?.alt};
});
const failures=[...errors];
for(const s of [pass.state,partial.state,blocked.state]){if(!s)failures.push("missing state");else if(!s.stimulusFixed||s.polarity!=="reversed"||s.cathodeX!==.19||s.anodeX!==.48||s.latency!==2.5||s.referenceAmp!==38)failures.push("fixed mechanism changed")}
if(pass.state?.blockedFraction!==0||partial.state?.blockedFraction!==.5||blocked.state?.blockedFraction!==1)failures.push("blocked fraction states");
if(pass.state?.liveAmp!==38||partial.state?.liveAmp!==19||blocked.state?.liveAmp!==0)failures.push("amplitude model");
if(pass.state?.arrival!=="TAM"||partial.state?.arrival!=="KISMİ"||blocked.state?.arrival!=="YOK")failures.push("arrival states");
if(!partial.ui.lesson.includes("onseti değişmez")||!blocked.ui.lesson.includes("yanıt kaydedilmez"))failures.push("teaching text");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation layout");
if(metrics.imageFailures||metrics.geo.width<900||metrics.scope.width<900||metrics.buttons!==4)failures.push("visual assets");
if(!metrics.warning.includes("kanıtı değildir")||!metrics.sourceAlt.includes("8.15"))failures.push("clinical caveat or figure");
console.log(JSON.stringify({failures,pass,partial,blocked,metrics},null,2));
await browser.close();if(failures.length)process.exitCode=1;
