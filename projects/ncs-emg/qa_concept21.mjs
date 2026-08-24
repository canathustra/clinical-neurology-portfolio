import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\antidromik-ortodromik\\animasyon-2-sahte-dsap.html";
const explanation="C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\antidromik-ortodromik\\hacim-iletilen-motor.html";
const out="C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser=await chromium.launch({
  headless:true,executablePath:"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args:["--disable-gpu","--no-first-run","--allow-file-access-from-files"]
});
const page=await browser.newPage({viewport:{width:1600,height:900}}),errors=[];
page.on("pageerror",error=>errors.push(`pageerror: ${error.message}`));
page.on("console",message=>{if(message.type()==="error")errors.push(`console: ${message.text()}`)});
await page.goto(pathToFileURL(live).href,{waitUntil:"load"});await page.waitForTimeout(350);
async function setIntegrity(value){
  await page.locator("#sensory").evaluate((element,v)=>{element.value=String(v);element.dispatchEvent(new Event("input",{bubbles:true}))},value);
  await page.waitForTimeout(160);
}
async function snap(name){
  const data=await page.evaluate(()=>({
    state:window.__falseSnapState,
    output:document.querySelector("#sensoryOutput")?.textContent?.trim(),
    anti:document.querySelector("#antiSnapText")?.textContent?.trim(),
    ortho:document.querySelector("#orthoSnapText")?.textContent?.trim(),
    motor:document.querySelector("#motorText")?.textContent?.trim(),
    verdict:document.querySelector("#verdictText")?.textContent?.trim(),
    logic:document.querySelector("#logicText")?.textContent?.trim(),
    mode:document.querySelector("#modeBadge")?.textContent?.trim()
  }));
  await page.screenshot({path:path.join(out,`concept21_${name}.png`)});
  return data;
}
const normal=await snap("normal");
await setIntegrity(20);const small=await snap("small");
await setIntegrity(0);const absent=await snap("absent");
await page.click("#scanButton");await page.waitForTimeout(2800);await page.screenshot({path:path.join(out,"concept21_auto_mid.png")});
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
  return s?.variable==="true_sensory_axon_contribution_percent"&&s?.stimulation==="fixed_median_wrist_supramaximal"&&
    s?.recording==="fixed_digit2_antidromic"&&s?.motorFibersStimulated===true&&s?.motorComponentFixed===true&&
    s?.motorComponentAmplitudeUv===80&&s?.earlySnapPeakMs===2.2&&s?.lateMotorOnsetMs===4.8&&s?.lateMotorPeakMs===6.3&&
    s?.bookCalibration?.normalSnapUv===33&&s?.bookCalibration?.normalSnapPeakMs===2.2;
}
for(const sample of [normal,small,absent])if(!fixed(sample.state))failures.push("fixed model");
if(normal.state.sensoryIntegrity!==100||normal.state.antidromicSnapAmplitudeUv!==33||normal.state.orthodromicConfirmationUv!==22||normal.state.trueSnapPresent!==true||normal.state.interpretation!=="early_snap_then_late_motor"||!normal.verdict.includes("Erken DSAP var"))failures.push("normal state");
if(small.state.sensoryIntegrity!==20||small.state.antidromicSnapAmplitudeUv!==6.6||small.state.orthodromicConfirmationUv!==4.4||small.state.trueSnapPresent!==true||small.state.interpretation!=="small_snap_separate_from_motor"||!small.verdict.includes("Küçük DSAP"))failures.push("small state");
if(absent.state.sensoryIntegrity!==0||absent.state.antidromicSnapAmplitudeUv!==0||absent.state.orthodromicConfirmationUv!==0||absent.state.trueSnapPresent!==false||absent.state.interpretation!=="absent_snap_false_motor_risk"||!absent.verdict.includes("DSAP yok")||!absent.logic.includes("sahte DSAP"))failures.push("absent state");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation");
if(metrics.buttons!==1||metrics.ranges!==1||metrics.imageFailures||!metrics.imageAlt.includes("Şekil 8.26")||metrics.canvas.width<900)failures.push("visual assets");
if(!metrics.visibleText.includes("Geç motor uzak-alan bileşeni sabit")||!metrics.visibleText.includes("Geç, geniş motor bileşene DSAP imleci konmamalıdır")||!metrics.visibleText.includes("Negatif ↑ · pozitif ↓"))failures.push("resident teaching");
if(explanationCheck.navCount!==3||!explanationCheck.text.includes("hem motor hem duysal")||!explanationCheck.text.includes("ilk bileşeni")||!explanationCheck.text.includes("DSAP sanmaktan kaçının"))failures.push("explanation preservation");
console.log(JSON.stringify({failures,normal,small,absent,metrics,explanationCheck},null,2));
await browser.close();if(failures.length)process.exitCode=1;
