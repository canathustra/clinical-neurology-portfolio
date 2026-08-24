import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const root = "C:\\Users\\uugur\\OneDrive\\Desktop\\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu";
const out = "C:\\Users\\uugur\\OneDrive\\Desktop\\animations_ncs_emg\\qa_fullscreen_hospital";
const manifest = JSON.parse(fs.readFileSync(path.join(root, "nonfizyolojik_69_sayfa_manifest.json"), "utf8"));
const viewports = [
  { name: "1366x768", width: 1366, height: 768 },
  { name: "1600x900", width: 1600, height: 900 },
  { name: "1920x1080", width: 1920, height: 1080 },
];
const representativePages = new Set([1, 2, 19, 43, 46, 50, 76, 78, 79, 82, 83]);
fs.mkdirSync(out, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  args: ["--disable-gpu", "--no-first-run"],
});

const rows = [];
for (const viewport of viewports) {
  const page = await browser.newPage({ viewport });
  let runtimeErrors = [];
  page.on("pageerror", error => runtimeErrors.push(`pageerror: ${error.message}`));
  page.on("console", message => {
    if (message.type() === "error") runtimeErrors.push(`console: ${message.text()}`);
  });

  for (const item of manifest.sequence) {
    runtimeErrors = [];
    await page.goto(pathToFileURL(path.join(root, item.file)).href, {
      waitUntil: "load",
      timeout: 20000,
    });
    await page.waitForTimeout(80);
    const metrics = await page.evaluate(({ expectedWidth, expectedHeight }) => {
      const shell = [...document.body.children]
        .map(element => ({ element, rect: element.getBoundingClientRect() }))
        .sort((a, b) => b.rect.width * b.rect.height - a.rect.width * a.rect.height)[0];
      const shellRect = shell.rect;
      const navRect = document.querySelector(".bottom-bar")?.getBoundingClientRect();
      const clippedText = [...document.body.querySelectorAll("*")]
        .filter(element => element.childElementCount === 0)
        .filter(element => (element.textContent || "").trim().length > 0)
        .filter(element => {
          const style = getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          return style.display !== "none" && style.visibility !== "hidden"
            && Number(style.opacity || 1) > 0 && rect.width > 0 && rect.height > 0;
        })
        .filter(element => element.scrollWidth > element.clientWidth + 2
          || element.scrollHeight > element.clientHeight + 2)
        .map(element => ({
          tag: element.tagName,
          className: String(element.className || ""),
          text: (element.textContent || "").trim().slice(0, 90),
          client: [element.clientWidth, element.clientHeight],
          scroll: [element.scrollWidth, element.scrollHeight],
        }));
      return {
        shellRect: {
          x: Math.round(shellRect.x),
          y: Math.round(shellRect.y),
          width: Math.round(shellRect.width),
          height: Math.round(shellRect.height),
          right: Math.round(shellRect.right),
          bottom: Math.round(shellRect.bottom),
        },
        exactViewport: Math.abs(shellRect.x) <= 1 && Math.abs(shellRect.y) <= 1
          && Math.abs(shellRect.width - expectedWidth) <= 1
          && Math.abs(shellRect.height - expectedHeight) <= 1,
        bodyOverflowX: document.documentElement.scrollWidth > expectedWidth + 1,
        bodyOverflowY: document.documentElement.scrollHeight > expectedHeight + 1,
        shellOverflowX: shell.element.scrollWidth > shell.element.clientWidth + 1,
        shellOverflowY: shell.element.scrollHeight > shell.element.clientHeight + 1,
        navCount: document.querySelectorAll(".bottom-bar .fkey").length,
        navBottom: navRect ? Math.round(navRect.bottom) : null,
        imagesFailed: [...document.images]
          .filter(image => !image.complete || image.naturalWidth === 0)
          .map(image => image.getAttribute("src")),
        clippedText,
      };
    }, { expectedWidth: viewport.width, expectedHeight: viewport.height });

    const errors = [...runtimeErrors];
    if (!metrics.exactViewport) errors.push("shell does not fill viewport");
    if (metrics.bodyOverflowX || metrics.bodyOverflowY || metrics.shellOverflowX || metrics.shellOverflowY) {
      errors.push("page overflow");
    }
    if (metrics.navCount !== 3 || metrics.navBottom === null
      || Math.abs(metrics.navBottom - viewport.height) > 1) {
      errors.push("navigation does not terminate at viewport bottom");
    }
    if (metrics.imagesFailed.length) errors.push(`failed images: ${metrics.imagesFailed.join(", ")}`);
    rows.push({ viewport: viewport.name, ...item, errors, metrics });

    if (viewport.name === "1600x900" && representativePages.has(item.number)) {
      const filename = `${String(item.number).padStart(2, "0")}-${item.type}-${item.file.replace(/[\\/]/g, "__")}.png`;
      await page.screenshot({ path: path.join(out, filename) });
    }
  }
  await page.close();
}
await browser.close();

const failures = rows.filter(row => row.errors.length);
const clipping = rows.filter(row => row.metrics.clippedText.length).map(row => ({
  viewport: row.viewport,
  number: row.number,
  file: row.file,
  clippedText: row.metrics.clippedText,
}));
const summary = {
  pagesPerViewport: manifest.sequence.length,
  viewports: viewports.map(viewport => viewport.name),
  checks: rows.length,
  failures: failures.map(row => ({
    viewport: row.viewport,
    number: row.number,
    file: row.file,
    errors: row.errors,
  })),
  leafTextClippingCandidates: clipping,
  representativeScreenshots: representativePages.size,
};
fs.writeFileSync(path.join(out, "report.json"), JSON.stringify({ summary, rows }, null, 2));
console.log(JSON.stringify(summary, null, 2));
if (failures.length) process.exit(1);
