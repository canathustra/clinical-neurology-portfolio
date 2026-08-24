import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const root = "C:\\Users\\uugur\\OneDrive\\Desktop\\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu";
const out = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\qa_final_nonphys_pages";
const manifest = JSON.parse(fs.readFileSync(path.join(root, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));
fs.mkdirSync(out, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
for (const item of manifest.sequence) {
  await page.goto(pathToFileURL(path.join(root, item.file)).href, { waitUntil: "load", timeout: 20000 });
  await page.waitForTimeout(120);
  await page.screenshot({
    path: path.join(out, `${String(item.number).padStart(2, "0")}-${item.type}.png`),
  });
}
await browser.close();
console.log(JSON.stringify({ pages: manifest.sequence.length, out }, null, 2));
