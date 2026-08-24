import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const root = "C:\\Users\\uugur\\OneDrive\\Desktop\\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu";
const out = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\qa_font_scale_candidates";
const manifest = JSON.parse(fs.readFileSync(path.join(root, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));
const viewports = [
  { name: "1366x768", width: 1366, height: 768 },
  { name: "1600x900", width: 1600, height: 900 },
  { name: "1920x1080", width: 1920, height: 1080 },
];
const scales = [1.08, 1.12, 1.15];
const representatives = new Set([2, 19, 43, 46, 50, 72, 76, 79, 82, 83]);
fs.mkdirSync(out, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run"],
});
const results = [];

for (const scale of scales) {
  for (const viewport of viewports) {
    const page = await browser.newPage({ viewport });
    for (const item of manifest.sequence) {
      const runtimeErrors = [];
      const onPageError = error => runtimeErrors.push(`pageerror: ${error.message}`);
      const onConsole = message => {
        if (message.type() === "error") runtimeErrors.push(`console: ${message.text()}`);
      };
      page.on("pageerror", onPageError);
      page.on("console", onConsole);
      await page.goto(pathToFileURL(path.join(root, item.file)).href, { waitUntil: "load", timeout: 20000 });
      const inverse = 100 / scale;
      await page.addStyleTag({ content: `
        body > .app, body > .slide {
          zoom: ${scale} !important;
          width: ${inverse}vw !important;
          height: ${inverse}vh !important;
        }
      ` });
      await page.waitForTimeout(90);
      const metrics = await page.evaluate(({ expectedWidth, expectedHeight }) => {
        const shell = [...document.body.children]
          .map(element => ({ element, rect: element.getBoundingClientRect() }))
          .sort((a, b) => b.rect.width * b.rect.height - a.rect.width * a.rect.height)[0];
        const rect = shell.rect;
        const navRect = document.querySelector(".bottom-bar")?.getBoundingClientRect();
        const clipped = [...document.body.querySelectorAll("*")]
          .filter(element => !(element instanceof SVGElement))
          .filter(element => element.childElementCount === 0)
          .filter(element => (element.textContent || "").trim())
          .filter(element => {
            const style = getComputedStyle(element);
            const box = element.getBoundingClientRect();
            return style.display !== "none" && style.visibility !== "hidden"
              && Number(style.opacity || 1) > 0 && box.width > 0 && box.height > 0;
          })
          .filter(element => element.scrollWidth > element.clientWidth + 3
            || element.scrollHeight > element.clientHeight + 3)
          .map(element => ({
            tag: element.tagName,
            className: String(element.className || ""),
            text: (element.textContent || "").trim().slice(0, 80),
          }));
        return {
          rect: {
            x: Math.round(rect.x), y: Math.round(rect.y),
            width: Math.round(rect.width), height: Math.round(rect.height),
            right: Math.round(rect.right), bottom: Math.round(rect.bottom),
          },
          viewportFit: Math.abs(rect.x) <= 2 && Math.abs(rect.y) <= 2
            && Math.abs(rect.width - expectedWidth) <= 3
            && Math.abs(rect.height - expectedHeight) <= 3,
          docOverflow: document.documentElement.scrollWidth > expectedWidth + 2
            || document.documentElement.scrollHeight > expectedHeight + 2,
          shellOverflow: shell.element.scrollWidth > shell.element.clientWidth + 2
            || shell.element.scrollHeight > shell.element.clientHeight + 2,
          navCount: document.querySelectorAll(".bottom-bar .fkey").length,
          navBottom: navRect ? Math.round(navRect.bottom) : null,
          failedImages: [...document.images]
            .filter(image => !image.complete || image.naturalWidth === 0)
            .map(image => image.getAttribute("src")),
          clipped,
        };
      }, { expectedWidth: viewport.width, expectedHeight: viewport.height });
      const errors = [...runtimeErrors];
      if (!metrics.viewportFit) errors.push("shell does not fill viewport");
      if (metrics.docOverflow || metrics.shellOverflow) errors.push("page overflow");
      if (metrics.navCount !== 3 || metrics.navBottom === null
        || Math.abs(metrics.navBottom - viewport.height) > 3) {
        errors.push("navigation mismatch");
      }
      if (metrics.failedImages.length) errors.push("failed image");
      results.push({ scale, viewport: viewport.name, ...item, metrics, errors });
      if (viewport.name === "1600x900" && representatives.has(item.number)) {
        await page.screenshot({
          path: path.join(out, `s${String(scale).replace(".", "")}-${String(item.number).padStart(2, "0")}.png`),
        });
      }
      page.removeListener("pageerror", onPageError);
      page.removeListener("console", onConsole);
    }
    await page.close();
  }
}

await browser.close();
const summary = scales.map(scale => {
  const rows = results.filter(row => row.scale === scale);
  return {
    scale,
    checks: rows.length,
    failures: rows.filter(row => row.errors.length).length,
    clippingCandidates: rows.filter(row => row.metrics.clipped.length).length,
    failedPages: rows.filter(row => row.errors.length).slice(0, 20).map(row => ({
      viewport: row.viewport, number: row.number, file: row.file, errors: row.errors, rect: row.metrics.rect,
    })),
  };
});
fs.writeFileSync(path.join(out, "report.json"), JSON.stringify({ summary, results }, null, 2));
console.log(JSON.stringify(summary, null, 2));
