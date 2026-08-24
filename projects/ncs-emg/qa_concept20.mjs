import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\antidromik-ortodromik\\animasyon-1-antidromik-vs-ortodromik.html";
const explanation="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\antidromik-ortodromik\\index.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({
  headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",error=>errors.push(`pageerror: ${error.message}`));
page.on("console",message=>{if(message.type()==="error")errors.push(`console: ${message.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(350);
async function setTechnique(value){
  await page.locator("#technique").evaluate((element,v)=>{element.value=String(v);element.dispatchEvent(new Event("input",{bubbles:true}))},value);
  await page.waitForTimeout(160);
}
async function snap(name){
  const data=await page.evaluate(()=>({
    state:window.__antiOrthoState,
    output:document.querySelector("#techniqueOutput")?.textContent?.trim(),
    technique:document.querySelector("#techniqueText")?.textContent?.trim(),
    record:document.querySelector("#recordText")?.textContent?.trim(),
    amp:document.querySelector("#ampText")?.textContent?.trim(),
    latency:document.querySelector("#latencyText")?.textContent?.trim(),
    logic:document.querySelector("#logicText")?.textContent?.trim(),
    mode:document.querySelector("#modeBadge")?.textContent?.trim()
  }));
  await page.screenshot({path:path.join(out,`concept20_${name}.png`)});
  return data;
}
const ortho=await snap("orthodromic");
await setTechnique(1);const anti=await snap("antidromic");
await page.click("#scanButton");await page.waitForTimeout(2100);await page.screenshot({path:path.join(out,"concept20_auto_switch.png")});
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
const explanationPage=await browser.newPage({viewport:{width:1600,height:900}});
await explanationPage.goto(pathToFileURL(explanation).href,{waitUntil:"load"});await explanationPage.waitForTimeout(150);
const explanationCheck=await explanationPage.evaluate(()=>({text:document.body.innerText,navCount:document.querySelectorAll(".bottom-bar .fkey").length}));
const failures=[...errors];
function fixed(s){
  return s?.variable==="sensory_recording_direction"&&s?.sameMedianNerveSegment===true&&s?.distance==="matched"&&
    s?.temperatureC===32&&s?.interelectrodeDistance==="matched"&&s?.peakLatencyMs===2.2&&s?.conductionVelocity==="same"&&
    s?.motorContamination==="not_modeled_reserved_for_next_concept"&&s?.bookCalibration?.antidromicUv===33&&
    s?.bookCalibration?.orthodromicUv===22&&s?.bookCalibration?.antidromicPeakMs===2.2&&s?.bookCalibration?.orthodromicPeakMs===2.2;
}
for(const sample of [ortho,anti])if(!fixed(sample.state))failures.push("fixed model");
if(ortho.state.technique!=="orthodromic"||ortho.state.stimulusSite!=="digit_2"||ortho.state.recordingSite!=="wrist"||ortho.state.amplitudeUv!==22||ortho.state.recordingGeometry!=="deeper_wrist_nerve_beneath_connective_tissue"||!ortho.logic.includes("daha az akson anlamına gelmez"))failures.push("orthodromic state");
if(anti.state.technique!=="antidromic"||anti.state.stimulusSite!=="wrist"||anti.state.recordingSite!=="digit_2"||anti.state.amplitudeUv!==33||anti.state.recordingGeometry!=="superficial_digital_nerve"||!anti.logic.includes("2,2 ms"))failures.push("antidromic state");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1||metrics.imageFailures||!metrics.imageAlt.includes("Şekil 8.26")||metrics.canvas.width<900)failures.push("visual assets");
if(!metrics.visibleText.includes("33 / 22 µV")||!metrics.visibleText.includes("her ikisi 2,2 ms")||!metrics.visibleText.includes("Normal değerler kullanılan tekniğe özgü")||!metrics.visibleText.includes("Negatif ↑ · pozitif ↓"))failures.push("resident teaching");
if(explanationCheck.navCount!==3||!explanationCheck.text.includes("ters ilişkilidir")||explanationCheck.text.includes("doğru orantılıdır")||!explanationCheck.text.includes("Aynı mesafe ve aynı ölçüm koşullarında"))failures.push("explanation correction");
console.log(JSON.stringify({failures,ortho,anti,metrics,explanationCheck},null,2));
await browser.close();if(failures.length)process.exitCode=1;
