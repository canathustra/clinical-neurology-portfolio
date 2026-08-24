import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\katot-polarite\\animasyon-1-polarite-tersligi.html";
const out = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg";
const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const errors = [];
page.on("pageerror", error => errors.push(`pageerror: ${error.message}`));
page.on("console", message => { if (message.type() === "error") errors.push(`console: ${message.text()}`); });
await page.goto(pathToFileURL(live).href, { waitUntil: "load" });
await page.waitForTimeout(300);

async function sample(name) {
  const state = await page.evaluate(() => window.__reversedPolarityState);
  const ui = await page.evaluate(() => ({
    badge: document.querySelector("#stateBadge")?.textContent?.trim(),
    path: document.querySelector("#truePathOut")?.textContent?.trim(),
    latency: document.querySelector("#latOut")?.textContent?.trim(),
    cv: document.querySelector("#cvOut")?.textContent?.trim(),
    lesson: document.querySelector("#lesson")?.textContent?.trim(),
    changedRows: document.querySelectorAll(".readout.changed").length,
  }));
  await page.screenshot({ path: path.join(out, `concept09_${name}.png`) });
  return { state, ui };
}

const correct = await sample("correct");
await page.click("#reverseBtn"); await page.waitForTimeout(150);
const reversed = await sample("reversed");
await page.click("#stimBtn"); await page.waitForTimeout(900);
await page.screenshot({ path: path.join(out, "concept09_reversed_travel.png") });
const animated = await page.evaluate(() => window.__reversedPolarityState);

const metrics = await page.evaluate(() => {
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),rect=nav?.getBoundingClientRect();
  return {
    overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,
    appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,
    navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:rect?Math.round(rect.bottom):null,
    imageFailures:[...document.images].filter(img=>!img.complete||!img.naturalWidth).length,
    geo:{width:document.querySelector("#geoCanvas")?.width,height:document.querySelector("#geoCanvas")?.height},
    scope:{width:document.querySelector("#scopeCanvas")?.width,height:document.querySelector("#scopeCanvas")?.height},
    buttons:document.querySelectorAll(".controls button").length,
  };
});

const failures=[...errors];
if(!correct.state||!reversed.state||!animated)failures.push("missing exposed state");
if(correct.state.measuredDistance!==14||reversed.state.measuredDistance!==14)failures.push("measured distance changed");
if(correct.state.truePath!==14||reversed.state.truePath!==16.5)failures.push("true path mechanism");
if(correct.state.latency!==2.2||reversed.state.latency!==2.5)failures.push("figure 8.16 latencies");
if(correct.state.amplitude!==38||reversed.state.amplitude!==38)failures.push("DSAP morphology proxy changed");
if(!(reversed.state.apparentCV<correct.state.apparentCV&&Math.abs(correct.state.apparentCV-63.636)<.01&&Math.abs(reversed.state.apparentCV-56)<.01))failures.push("apparent CV calculation");
if(!correct.ui.badge.includes("Doğru")||!reversed.ui.badge.includes("Ters"))failures.push("state labels");
if(reversed.ui.changedRows!==3||!reversed.ui.lesson.includes("+2,5 cm")||!reversed.ui.lesson.includes("+0,3 ms"))failures.push("teaching emphasis");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation layout");
if(metrics.imageFailures||metrics.geo.width<900||metrics.scope.width<900||metrics.buttons!==3)failures.push("visual assets");

console.log(JSON.stringify({failures,correct,reversed,animated,metrics},null,2));
await browser.close();
if(failures.length)process.exitCode=1;
