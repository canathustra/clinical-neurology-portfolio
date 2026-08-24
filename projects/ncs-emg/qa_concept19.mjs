import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\motor-elektrot-yerlesimi\\animasyon-2-g2-tendon-potansiyeli.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({
  headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",error=>errors.push(`pageerror: ${error.message}`));
page.on("console",message=>{if(message.type()==="error")errors.push(`console: ${message.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(350);
async function setPosition(value){
  await page.locator("#g2Position").evaluate((element,v)=>{element.value=String(v);element.dispatchEvent(new Event("input",{bubbles:true}))},value);
  await page.waitForTimeout(140);
}
async function snap(name){
  const data=await page.evaluate(()=>({
    state:window.__g2TendonState,
    position:document.querySelector("#positionText")?.textContent?.trim(),
    metric:document.querySelector("#positionMetric")?.textContent?.trim(),
    amp:document.querySelector("#ampText")?.textContent?.trim(),
    g2:document.querySelector("#g2Text")?.textContent?.trim(),
    loss:document.querySelector("#lossText")?.textContent?.trim(),
    verdict:document.querySelector("#verdictText")?.textContent?.trim(),
    logic:document.querySelector("#logicText")?.textContent?.trim()
  }));
  await page.screenshot({path:path.join(out,`concept19_${name}.png`)});
  return data;
}
const p1=await snap("position1");
await setPosition(50);const p2=await snap("position2");
await setPosition(100);const p3=await snap("position3");
await page.click("#scanButton");await page.waitForTimeout(2400);await page.screenshot({path:path.join(out,"concept19_auto_scan_mid.png")});
const metrics=await page.evaluate(()=>{
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),r=nav?.getBoundingClientRect();
  return{
    overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,
    appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,
    navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:r?Math.round(r.bottom):null,
    buttons:document.querySelectorAll(".controls button").length,ranges:document.querySelectorAll(".controls input[type=range]").length,
    imageFailures:[...document.images].filter(image=>!image.complete||!image.naturalWidth).length,
    imageAlts:[...document.images].map(image=>image.alt),
    canvas:{width:document.querySelector("#labCanvas")?.width,height:document.querySelector("#labCanvas")?.height},
    visibleText:document.body.innerText
  };
});
const failures=[...errors];
function fixed(s){
  return s?.variable==="g2_distal_position"&&s?.g1Fixed===true&&s?.g1Location==="fixed_motor_point"&&
    s?.stimulation==="fixed_supramaximal"&&s?.underlyingNerveMuscle==="normal_ulnar_adm"&&
    s?.isolatedG1ModelAmp===5.6&&s?.formula==="G1 - G2"&&s?.polarity==="g2_predominantly_positive"&&
    s?.bookCalibration?.position1===8.3&&s?.bookCalibration?.position2===7.2&&s?.bookCalibration?.position3===5.6;
}
for(const sample of [p1,p2,p3])if(!fixed(sample.state))failures.push("fixed model");
if(p1.state.sliderPosition!==0||p1.state.bookPosition!==1||p1.state.outputAmplitude!==8.3||p1.state.g2PositiveContribution!==2.7||p1.state.apparentLossPercent!==0||p1.state.morphology!=="bifid_prominent"||!p1.verdict.includes("güçlü"))failures.push("position 1");
if(p2.state.sliderPosition!==50||p2.state.bookPosition!==2||p2.state.outputAmplitude!==7.2||p2.state.g2PositiveContribution!==1.6||p2.state.apparentLossPercent!==13.3||p2.state.morphology!=="bifid_partial")failures.push("position 2");
if(p3.state.sliderPosition!==100||p3.state.bookPosition!==3||p3.state.outputAmplitude!==5.6||p3.state.g2PositiveContribution!==0||p3.state.apparentLossPercent!==32.5||p3.state.morphology!=="g1_dominant"||!p3.verdict.includes("akson kaybı değil"))failures.push("position 3");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1||metrics.imageFailures||metrics.imageAlts.length!==2||!metrics.imageAlts.join(" ").includes("Şekil 8.24")||!metrics.imageAlts.join(" ").includes("Şekil 8.25")||metrics.canvas.width<900)failures.push("visual assets");
if(!metrics.visibleText.includes("Negatif ↑ · pozitif ↓")||!metrics.visibleText.includes("8,3 / 7,2 / 5,6 mV")||!metrics.visibleText.includes("farklı bir montajdır")||!metrics.visibleText.includes("G1 − G2"))failures.push("resident teaching");
console.log(JSON.stringify({failures,p1,p2,p3,metrics},null,2));
await browser.close();if(failures.length)process.exitCode=1;
