import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";

const file = "C:\\Users\\uugur\\OneDrive\\Desktop\\Second_Brain\\10_Projects\\presentations\\artifacts_of_ncs_emg\\animations\\impedans-gurultu\\animasyon-2-gurultu-azaltma.html";
const output = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\concept02_box83_all_applied.png";
const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run", "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const errors = [];
page.on("pageerror", error => errors.push(error.message));
page.on("console", message => {
  if (message.type() === "error") errors.push(message.text());
});
await page.goto(pathToFileURL(file).href, { waitUntil: "load" });
for (const checkbox of await page.locator('.chk-item input').all()) {
  await checkbox.check();
  await page.waitForTimeout(80);
}
await page.waitForTimeout(250);
const metrics = await page.evaluate(() => ({
  checked: document.querySelectorAll('.chk-item input:checked').length,
  score: document.querySelector('#scoreOut')?.textContent,
  mains: document.querySelector('#mainsOut')?.textContent,
  cable: document.querySelector('#cableOut')?.textContent,
  stimulus: document.querySelector('#stimOut')?.textContent,
  overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  overflowY: document.documentElement.scrollHeight > document.documentElement.clientHeight + 1,
  navCount: document.querySelectorAll('.bottom-bar .fkey').length,
}));
await page.screenshot({ path: output });
await browser.close();
console.log(JSON.stringify({ errors, metrics }, null, 2));
if (errors.length || metrics.checked !== 8 || metrics.score !== "0/8 eksik" || metrics.overflowX || metrics.overflowY || metrics.navCount !== 3) process.exitCode = 1;
