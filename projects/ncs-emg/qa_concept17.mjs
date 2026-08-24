import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\motor-elektrot-yerlesimi\\animasyon-0-belly-tendon-montaj.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({
  headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",error=>errors.push(`pageerror: ${error.message}`));
page.on("console",message=>{if(message.type()==="error")errors.push(`console: ${message.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(350);

async function setTime(value){
  await page.locator("#time").evaluate((element,v)=>{element.value=String(v);element.dispatchEvent(new Event("input",{bubbles:true}))},value);
  await page.waitForTimeout(120);
}
async function snap(name){
  const data=await page.evaluate(()=>({
    state:window.__bellyTendonBaselineState,
    time:document.querySelector("#timeText")?.textContent?.trim(),
    result:document.querySelector("#resultText")?.textContent?.trim(),
    activeSteps:[...document.querySelectorAll(".step.active")].map(x=>x.id),
    doneSteps:[...document.querySelectorAll(".step.done")].map(x=>x.id)
  }));
  await page.screenshot({path:path.join(out,`concept17_${name}.png`)});
  return data;
}
const start=await snap("start");
await setTime(35);const endplate=await snap("endplate");
await setTime(62);const g1=await snap("g1");
await setTime(100);const complete=await snap("complete");
await page.click("#playButton");await page.waitForTimeout(1850);await page.screenshot({path:path.join(out,"concept17_animation_mid.png")});

const metrics=await page.evaluate(()=>{
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),r=nav?.getBoundingClientRect();
  return{
    overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,
    appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,
    navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:r?Math.round(r.bottom):null,
    buttons:document.querySelectorAll(".controls button").length,ranges:document.querySelectorAll(".controls input[type=range]").length,
    imageFailures:[...document.images].filter(image=>!image.complete||!image.naturalWidth).length,
    imageAlt:document.querySelector(".book img")?.alt||"",
    canvas:{width:document.querySelector("#labCanvas")?.width,height:document.querySelector("#labCanvas")?.height},
    visibleText:document.body.innerText
  };
});
const failures=[...errors];
function fixed(s){
  return s?.variable==="depolarization_time"&&s?.g1Location==="motor_point"&&s?.g2Location==="distal_tendon"&&
    s?.g2Assumption==="electrically_inert_model"&&s?.g1Amp===8&&s?.g2Amp===0&&s?.outputAmp===8&&
    s?.outputFormula==="G1-G2"&&s?.negativeDisplay==="upward"&&!s?.activeG2Demonstrated;
}
for(const sample of [start,endplate,g1,complete])if(!fixed(sample.state))failures.push("fixed baseline montage");
if(start.state.progress!==0||start.activeSteps.length||start.doneSteps.length)failures.push("start");
if(endplate.state.progress!==.35||!endplate.activeSteps.includes("step1")||endplate.doneSteps.length)failures.push("endplate phase");
if(g1.state.progress!==.62||!g1.activeSteps.includes("step2")||!g1.doneSteps.includes("step1"))failures.push("g1 phase");
if(complete.state.progress!==1||complete.activeSteps.length||complete.doneSteps.length!==3||!complete.result.includes("G2 = 0"))failures.push("complete formula");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1||metrics.imageFailures||!metrics.imageAlt.includes("belly-tendon")||metrics.canvas.width<900)failures.push("visual assets");
if(!metrics.visibleText.includes("Negatif ↑")||!metrics.visibleText.includes("G1−G2")||!metrics.visibleText.includes("aktif G2 daha sonra")||!metrics.visibleText.includes("ulnar ve tibial"))failures.push("clinical teaching");
console.log(JSON.stringify({failures,start,endplate,g1,complete,metrics},null,2));
await browser.close();if(failures.length)process.exitCode=1;
