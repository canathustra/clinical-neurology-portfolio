import { chromium } from "file:///C:/Users/uugur/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import { pathToFileURL, fileURLToPath } from "url";
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
  const file = path.join(root, item.file);
  const source = fs.readFileSync(file, "utf8");
  const runtimeErrors = [];
  const onPageError = error => runtimeErrors.push(`pageerror: ${error.message}`);
  const onConsole = message => {
    if (message.type() === "error") runtimeErrors.push(`console: ${message.text()}`);
  };
  page.on("pageerror", onPageError);
  page.on("console", onConsole);
  await page.goto(pathToFileURL(file).href, { waitUntil: "load", timeout: 20000 });
  await page.waitForTimeout(90);

  const dom = await page.evaluate(() => {
    const ids = [...document.querySelectorAll("[id]")].map(element => element.id);
    const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
    const links = [...document.querySelectorAll("a[href]")].map(anchor => anchor.href);
    const resources = [
      ...[...document.querySelectorAll("img[src]")].map(image => image.src),
      ...[...document.querySelectorAll("script[src]")].map(script => script.src),
      ...[...document.querySelectorAll("link[href]")].map(link => link.href),
    ];
    const emptyButtons = [...document.querySelectorAll("button")]
      .filter(button => !button.textContent.trim() && !button.getAttribute("aria-label"))
      .length;
    const missingAlt = [...document.images].filter(image => !image.hasAttribute("alt")).length;
    const nav = [...document.querySelectorAll(".bottom-bar .fkey")].map(link => ({
      text: link.textContent.trim().replace(/\s+/g, " "),
      href: link.href,
    }));
    return {
      duplicateIds: duplicates,
      links,
      resources,
      emptyButtons,
      missingAlt,
      nav,
      title: document.title,
      fullscreenStyles: document.querySelectorAll("#nonphys-fullscreen-override").length,
      fontScaleStyles: document.querySelectorAll("#nonphys-font-scale").length,
      fontScaleZoom: getComputedStyle(
        document.querySelector(".app, .slide")
      ).zoom,
    };
  });

  const brokenTargets = [];
  for (const url of [...dom.links, ...dom.resources]) {
    if (!url.startsWith("file:")) continue;
    const target = fileURLToPath(url.split("#")[0].split("?")[0]);
    if (!fs.existsSync(target)) brokenTargets.push(target);
  }
  const externalRefs = [...source.matchAll(/\b(?:https?:|\/\/)[^\s"'<>)]*/gi)].map(match => match[0]);
  const errors = [...runtimeErrors];
  if (!dom.title.trim()) errors.push("missing document title");
  if (dom.duplicateIds.length) errors.push(`duplicate IDs: ${dom.duplicateIds.join(", ")}`);
  if (brokenTargets.length) errors.push(`broken local targets: ${brokenTargets.join(", ")}`);
  if (externalRefs.length) errors.push(`external references: ${externalRefs.join(", ")}`);
  if (dom.emptyButtons) errors.push(`${dom.emptyButtons} unlabeled buttons`);
  if (dom.missingAlt) errors.push(`${dom.missingAlt} images without alt`);
  if (dom.nav.length !== 3) errors.push(`navigation count ${dom.nav.length}`);
  if (dom.fullscreenStyles !== 1) errors.push(`fullscreen override count ${dom.fullscreenStyles}`);
  if (dom.fontScaleStyles !== 1) errors.push(`font scale style count ${dom.fontScaleStyles}`);
  if (Math.abs(Number(dom.fontScaleZoom) - 1.15) > 0.001) errors.push(`computed zoom ${dom.fontScaleZoom}`);
  if (source.includes("<<style") || source.includes("<</head>") || source.includes("</style>>")) {
    errors.push("malformed style/head marker");
  }
  if ((source.match(/<style\b/gi) || []).length !== (source.match(/<\/style>/gi) || []).length) {
    errors.push("unbalanced style tags");
  }
  if ((source.match(/<script\b/gi) || []).length !== (source.match(/<\/script>/gi) || []).length) {
    errors.push("unbalanced script tags");
  }
  rows.push({ ...item, errors, dom: { ...dom, links: undefined, resources: undefined }, brokenTargets, externalRefs });
  page.removeListener("pageerror", onPageError);
  page.removeListener("console", onConsole);
}

await browser.close();
const failures = rows.filter(row => row.errors.length);
const summary = {
  pages: rows.length,
  failures: failures.map(row => ({
    number: row.number,
    file: row.file,
    errors: row.errors,
  })),
};
fs.writeFileSync("deep-independent-nonphys-report.json", JSON.stringify({ summary, rows }, null, 2));
console.log(JSON.stringify(summary, null, 2));
if (failures.length) process.exit(1);
