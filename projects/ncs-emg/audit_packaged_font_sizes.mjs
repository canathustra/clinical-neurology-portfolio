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
  await page.goto(pathToFileURL(path.join(root, item.file)).href, { waitUntil: "load", timeout: 20000 });
  await page.waitForTimeout(60);
  const data = await page.evaluate(() => {
    const samples = [...document.body.querySelectorAll("*")]
      .filter(element => !(element instanceof SVGElement))
      .filter(element => !["SCRIPT", "STYLE", "NOSCRIPT"].includes(element.tagName))
      .filter(element => [...element.childNodes].some(node => node.nodeType === Node.TEXT_NODE && node.textContent.trim()))
      .map(element => {
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        return {
          element,
          size: Number.parseFloat(style.fontSize),
          text: [...element.childNodes]
            .filter(node => node.nodeType === Node.TEXT_NODE)
            .map(node => node.textContent.trim())
            .filter(Boolean)
            .join(" ")
            .slice(0, 100),
          visible: style.display !== "none" && style.visibility !== "hidden"
            && Number(style.opacity || 1) > 0 && rect.width > 0 && rect.height > 0,
        };
      })
      .filter(sample => sample.visible && Number.isFinite(sample.size));
    const sizes = samples.map(sample => sample.size).sort((a, b) => a - b);
    const median = sizes.length ? sizes[Math.floor(sizes.length / 2)] : null;
    return {
      count: samples.length,
      min: sizes[0] ?? null,
      median,
      under10: samples.filter(sample => sample.size < 10).length,
      under11: samples.filter(sample => sample.size < 11).length,
      under12: samples.filter(sample => sample.size < 12).length,
      smallest: samples
        .sort((a, b) => a.size - b.size)
        .slice(0, 8)
        .map(({ size, text }) => ({ size, text })),
    };
  });
  rows.push({ ...item, ...data });
}

await browser.close();
const summary = {
  pages: rows.length,
  pagesWithUnder10: rows.filter(row => row.under10).length,
  pagesWithUnder11: rows.filter(row => row.under11).length,
  lowestMin: Math.min(...rows.map(row => row.min ?? Infinity)),
  lowestMedian: Math.min(...rows.map(row => row.median ?? Infinity)),
  worstPages: [...rows]
    .sort((a, b) => b.under11 - a.under11 || (a.min ?? Infinity) - (b.min ?? Infinity))
    .slice(0, 15)
    .map(row => ({
      number: row.number,
      type: row.type,
      file: row.file,
      min: row.min,
      median: row.median,
      under10: row.under10,
      under11: row.under11,
      smallest: row.smallest,
    })),
};
fs.writeFileSync("packaged-font-size-audit.json", JSON.stringify({ summary, rows }, null, 2));
console.log(JSON.stringify(summary, null, 2));
