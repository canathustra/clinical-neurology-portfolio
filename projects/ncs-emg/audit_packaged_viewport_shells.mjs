import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const root = "C:\\Users\\uugur\\OneDrive\\Desktop\\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu";
const manifest = JSON.parse(fs.readFileSync(path.join(root, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));
const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run"],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const rows = [];

for (const item of manifest.sequence) {
  await page.goto(pathToFileURL(path.join(root, item.file)).href, { waitUntil: "load" });
  const data = await page.evaluate(() => {
    const candidates = [...document.body.children].map(element => {
      const rect = element.getBoundingClientRect();
      return {
        tag: element.tagName.toLowerCase(),
        id: element.id,
        classes: [...element.classList],
        rect: {
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          right: Math.round(rect.right),
          bottom: Math.round(rect.bottom),
        },
        area: rect.width * rect.height,
      };
    }).sort((a, b) => b.area - a.area);
    const shell = candidates[0];
    return {
      bodyMargin: getComputedStyle(document.body).margin,
      bodyPadding: getComputedStyle(document.body).padding,
      shell,
      app: document.querySelector(".app")?.getBoundingClientRect().toJSON() || null,
      slide: document.querySelector(".slide")?.getBoundingClientRect().toJSON() || null,
    };
  });
  rows.push({ ...item, ...data });
}
await browser.close();

const groups = {};
for (const row of rows) {
  const shell = row.shell;
  const key = `${shell.tag}.${shell.classes.join(".")}#${shell.id}|${shell.rect.x},${shell.rect.y},${shell.rect.width},${shell.rect.height}`;
  (groups[key] ||= []).push(row.file);
}
console.log(JSON.stringify({ pages: rows.length, groups, rows }, null, 2));
