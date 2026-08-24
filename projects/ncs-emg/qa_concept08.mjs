import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import path from "path";

const live = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\stimulus-artefakti\\animasyon-3-kablo-induksiyonu.html";
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
  const state = await page.evaluate(() => window.__cableCouplingState);
  const ui = await page.evaluate(() => ({
    badge: document.querySelector("#stateBadge")?.textContent?.trim(),
    lesson: document.querySelector("#lesson")?.textContent?.trim(),
    coupling: document.querySelector("#couplingOut")?.textContent?.trim(),
    artifact: document.querySelector("#artifactOut")?.textContent?.trim(),
    recovery: document.querySelector("#recoveryOut")?.textContent?.trim(),
    trueOut: document.querySelector("#trueOut")?.textContent?.trim(),
  }));
  await page.screenshot({ path: path.join(out, `concept08_${name}.png`) });
  return { state, ui };
}

const clean = await sample("clean");
await page.click("#nearBtn"); await page.waitForTimeout(120);
const near = await sample("near_coax");
await page.click("#worstBtn"); await page.waitForTimeout(120);
const worst = await sample("free_overlap");

await page.click("#coaxBtn"); const sameCoax = await page.evaluate(() => window.__cableCouplingState);
await page.click("#twistedBtn"); const sameTwisted = await page.evaluate(() => window.__cableCouplingState);
await page.click("#freeBtn"); const sameFree = await page.evaluate(() => window.__cableCouplingState);

await page.click("#cleanBtn"); await page.click("#stimBtn"); await page.waitForTimeout(650);
await page.screenshot({ path: path.join(out, "concept08_pulse.png") });
const animated = await page.evaluate(() => window.__cableCouplingState);

const metrics = await page.evaluate(() => {
  const root=document.documentElement,app=document.querySelector(".app"),nav=document.querySelector(".bottom-bar"),rect=nav?.getBoundingClientRect();
  return {
    overflowX:root.scrollWidth>root.clientWidth+1,overflowY:root.scrollHeight>root.clientHeight+1,
    appOverflowX:app.scrollWidth>app.clientWidth+1,appOverflowY:app.scrollHeight>app.clientHeight+1,
    navCount:document.querySelectorAll(".bottom-bar .fkey").length,navBottom:rect?Math.round(rect.bottom):null,
    imageFailures:[...document.images].filter(img=>!img.complete||!img.naturalWidth).length,
    cable:{width:document.querySelector("#cableCanvas")?.width,height:document.querySelector("#cableCanvas")?.height},
    scope:{width:document.querySelector("#scopeCanvas")?.width,height:document.querySelector("#scopeCanvas")?.height},
    buttons:document.querySelectorAll(".controls button,.presets button").length,
  };
});

const states=[clean.state,near.state,worst.state,sameCoax,sameTwisted,sameFree,animated];
const failures=[...errors];
if(states.some(s=>!s))failures.push("missing exposed state");
if(states.some(s=>s.trueAmp!==14||s.trueLatency!==2.4))failures.push("true DSAP changed");
if(!(clean.state.coupling<near.state.coupling&&near.state.coupling<worst.state.coupling&&worst.state.coupling>.9))failures.push("preset coupling order");
if(!(sameCoax.coupling<sameTwisted.coupling&&sameTwisted.coupling<sameFree.coupling))failures.push("cable type order");
if(!clean.ui.badge.includes("Koaksiyel")||!near.ui.badge.includes("Kuplaj")||!worst.ui.badge.includes("Artefakt"))failures.push("teaching states");
if(!worst.ui.lesson.includes("Şekil 8.12")||worst.ui.recovery!=="onsetten sonra")failures.push("book mechanism");
if(metrics.overflowX||metrics.overflowY||metrics.appOverflowX||metrics.appOverflowY)failures.push("overflow");
if(metrics.navCount!==3||metrics.navBottom===null||metrics.navBottom<860)failures.push("navigation layout");
if(metrics.imageFailures||metrics.cable.width<900||metrics.scope.width<900||metrics.buttons!==7)failures.push("visual assets");

console.log(JSON.stringify({failures,clean,near,worst,sameCoax,sameTwisted,sameFree,animated,metrics},null,2));
await browser.close();
if(failures.length)process.exitCode=1;
