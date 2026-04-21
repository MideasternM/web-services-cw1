const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");
const deckContent = require("./content/deck-content");

const PPTX = new PptxGenJS();
const PROJECT_ROOT = path.resolve(__dirname, "..", "..");
const OUT_DIR = path.join(PROJECT_ROOT, "slides");
const ASSET_DIR = path.join(__dirname, "assets");

const COLORS = {
  navy: "132238",
  teal: "137C8B",
  sky: "D9EEF2",
  mist: "F4F7F8",
  white: "FFFFFF",
  ink: "18212B",
  slate: "516173",
  border: "D7DEE3",
  mint: "DDF3E8",
  amber: "F7E6C7",
  rose: "F5DBD8",
};

function ensureDirs() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(ASSET_DIR, { recursive: true });
}

function hasAsset(name) {
  return fs.existsSync(path.join(ASSET_DIR, name));
}

function assetPath(name) {
  return path.join(ASSET_DIR, name);
}

function setMetadata() {
  PPTX.layout = "LAYOUT_16x9";
  PPTX.author = "Shuyu Cao";
  PPTX.company = "University Coursework";
  PPTX.subject = "XJCO3011 Oral Presentation";
  PPTX.title = "Nutrition and Recipe Analytics API";
  PPTX.lang = "en-GB";
  PPTX.theme = {
    headFontFace: "Aptos Display",
    bodyFontFace: "Aptos",
    lang: "en-GB",
  };
}

function addPageNumber(slide, number) {
  slide.addText(String(number), {
    x: 9.2, y: 5.15, w: 0.3, h: 0.18,
    fontFace: "Aptos", fontSize: 9, color: COLORS.slate,
    align: "right", margin: 0,
  });
}

function addSectionHeader(slide, title, label) {
  slide.addText(title, {
    x: 0.55, y: 0.38, w: 6.8, h: 0.4,
    fontFace: "Aptos Display", fontSize: 24, bold: true,
    color: COLORS.ink, margin: 0,
  });
  if (label) {
    slide.addShape(PPTX.ShapeType.rect, {
      x: 8.05, y: 0.36, w: 1.25, h: 0.28,
      fill: { color: COLORS.teal },
      line: { color: COLORS.teal, width: 1 },
    });
    slide.addText(label, {
      x: 8.13, y: 0.42, w: 1.08, h: 0.12,
      fontFace: "Aptos", fontSize: 9.5, bold: true,
      color: COLORS.white, align: "center", margin: 0,
    });
  }
}

function addFooterRule(slide) {
  slide.addShape(PPTX.ShapeType.line, {
    x: 0.55, y: 4.94, w: 8.85, h: 0,
    line: { color: COLORS.border, width: 1.2 },
  });
}

function addBulletList(slide, bullets, opts = {}) {
  const runs = [];
  bullets.forEach((bullet, index) => {
    runs.push({
      text: bullet,
      options: {
        bullet: true,
        breakLine: index < bullets.length - 1,
        paraSpaceAfterPt: 12,
      },
    });
  });
  slide.addText(runs, {
    x: opts.x ?? 0.85,
    y: opts.y ?? 1.55,
    w: opts.w ?? 3.75,
    h: opts.h ?? 2.4,
    fontFace: "Aptos",
    fontSize: opts.fontSize ?? 17,
    color: COLORS.ink,
    margin: 0,
    valign: "top",
  });
}

function addCard(slide, x, y, w, h, fill = COLORS.white) {
  slide.addShape(PPTX.ShapeType.rect, {
    x, y, w, h,
    fill: { color: fill },
    line: { color: COLORS.border, width: 1.1 },
    shadow: {
      type: "outer",
      color: "000000",
      blur: 1,
      offset: 1,
      angle: 45,
      opacity: 0.08,
    },
  });
}

function addMiniStat(slide, x, y, value, caption, fill) {
  addCard(slide, x, y, 1.72, 1.05, fill);
  slide.addText(value, {
    x: x + 0.15, y: y + 0.14, w: 1.42, h: 0.34,
    fontFace: "Aptos Display", fontSize: 28, bold: true,
    color: COLORS.ink, align: "center", margin: 0,
  });
  slide.addText(caption, {
    x: x + 0.12, y: y + 0.62, w: 1.48, h: 0.18,
    fontFace: "Aptos", fontSize: 9.5, color: COLORS.slate,
    align: "center", margin: 0,
  });
}

function addFlowBoxes(slide, items, x, y, totalW) {
  const width = totalW / items.length - 0.1;
  items.forEach((item, index) => {
    const left = x + index * (width + 0.1);
    addCard(slide, left, y, width, 0.82, index % 2 === 0 ? "EAF4F6" : "EEF3F7");
    slide.addText(item, {
      x: left + 0.06, y: y + 0.28, w: width - 0.12, h: 0.16,
      fontFace: "Aptos", fontSize: 10.5, bold: true,
      color: COLORS.ink, align: "center", margin: 0,
    });
    if (index < items.length - 1) {
      slide.addText(">", {
        x: left + width - 0.02, y: y + 0.23, w: 0.14, h: 0.14,
        fontFace: "Aptos Display", fontSize: 15, bold: true,
        color: COLORS.teal, align: "center", margin: 0,
      });
    }
  });
}

function addEntityCard(slide, x, y, title, desc, fill) {
  addCard(slide, x, y, 2.58, 1.02, fill);
  slide.addText(title, {
    x: x + 0.12, y: y + 0.12, w: 2.1, h: 0.18,
    fontFace: "Consolas", fontSize: 12.5, bold: true,
    color: COLORS.ink, margin: 0,
  });
  slide.addText(desc, {
    x: x + 0.12, y: y + 0.38, w: 2.24, h: 0.42,
    fontFace: "Aptos", fontSize: 9.5, color: COLORS.slate,
    margin: 0,
  });
}

function addEndpointList(slide, endpoints, opts = {}) {
  const x = opts.x ?? 6.88;
  const y = opts.y ?? 1.2;
  const w = opts.w ?? 2.42;
  const h = opts.h ?? 3.05;
  addCard(slide, x, y, w, h, COLORS.white);
  slide.addText("Representative endpoints", {
    x: x + 0.18, y: y + 0.18, w: w - 0.36, h: 0.18,
    fontFace: "Aptos", fontSize: 10.5, bold: true,
    color: COLORS.slate, margin: 0,
  });
  slide.addText(
    endpoints.map((endpoint, idx) => ({
      text: endpoint,
      options: {
        bullet: true,
        breakLine: idx < endpoints.length - 1,
        paraSpaceAfterPt: 8,
      },
    })),
    {
      x: x + 0.22, y: y + 0.56, w: w - 0.42, h: h - 0.82,
      fontFace: "Consolas", fontSize: opts.fontSize ?? 9.4, color: COLORS.ink, margin: 0,
    }
  );
}

function addCommitTimeline(slide, commits) {
  slide.addShape(PPTX.ShapeType.line, {
    x: 0.95, y: 1.72, w: 0, h: 2.1,
    line: { color: COLORS.teal, width: 2 },
  });
  commits.forEach((commit, index) => {
    const top = 1.52 + index * 0.58;
    slide.addShape(PPTX.ShapeType.ellipse, {
      x: 0.86, y: top, w: 0.18, h: 0.18,
      fill: { color: COLORS.teal },
      line: { color: COLORS.teal, width: 1 },
    });
    slide.addText(commit, {
      x: 1.18, y: top - 0.03, w: 3.75, h: 0.22,
      fontFace: "Consolas", fontSize: 10.4, color: COLORS.ink, margin: 0,
    });
  });
}

function addDeliverableGrid(slide, deliverables) {
  const fills = [COLORS.sky, COLORS.mint, COLORS.amber];
  deliverables.forEach((item, index) => {
    const left = 5.5 + (index % 2) * 1.9;
    const top = 1.3 + Math.floor(index / 2) * 1.1;
    addCard(slide, left, top, 1.65, 0.92, fills[index % fills.length]);
    slide.addText(item, {
      x: left + 0.12, y: top + 0.15, w: 1.38, h: 0.5,
      fontFace: "Aptos", fontSize: 10.2, bold: true,
      color: COLORS.ink, margin: 0, valign: "mid", align: "center",
    });
  });
}

function addNumberedSteps(slide, steps, x, y, w) {
  steps.forEach((step, index) => {
    const top = y + index * 0.67;
    slide.addShape(PPTX.ShapeType.ellipse, {
      x, y: top, w: 0.28, h: 0.28,
      fill: { color: COLORS.teal },
      line: { color: COLORS.teal, width: 1 },
    });
    slide.addText(String(index + 1), {
      x: x + 0.03, y: top + 0.04, w: 0.22, h: 0.12,
      fontFace: "Aptos", fontSize: 9.5, bold: true,
      color: COLORS.white, align: "center", margin: 0,
    });
    slide.addText(step, {
      x: x + 0.42, y: top - 0.01, w, h: 0.28,
      fontFace: "Aptos", fontSize: 11.4, color: COLORS.ink, margin: 0,
    });
  });
}

function addCoverSlide(slide, item) {
  slide.background = { color: COLORS.navy };
  slide.addShape(PPTX.ShapeType.rect, {
    x: 0, y: 0, w: 10, h: 5.625,
    fill: { color: "0F1B2B", transparency: 10 },
    line: { color: "0F1B2B", transparency: 100 },
  });
  if (hasAsset("hero-cover.png")) {
    slide.addImage({
      path: assetPath("hero-cover.png"),
      x: 6.2, y: 0.45, w: 3.2, h: 4.4,
      sizing: { type: "cover", x: 6.2, y: 0.45, w: 3.2, h: 4.4 },
    });
    slide.addShape(PPTX.ShapeType.rect, {
      x: 6.2, y: 0.45, w: 3.2, h: 4.4,
      fill: { color: COLORS.navy, transparency: 34 },
      line: { color: COLORS.white, transparency: 100 },
    });
  } else {
    slide.addShape(PPTX.ShapeType.ellipse, {
      x: 6.35, y: 0.85, w: 2.3, h: 2.3,
      fill: { color: COLORS.teal, transparency: 20 },
      line: { color: "61C0BF", width: 3 },
    });
    slide.addShape(PPTX.ShapeType.rect, {
      x: 7.12, y: 1.65, w: 0.82, h: 1.72,
      fill: { color: COLORS.teal, transparency: 12 },
      line: { color: COLORS.teal, width: 1 },
      rotate: 45,
    });
  }
  slide.addText(item.kicker, {
    x: 0.72, y: 0.88, w: 3.0, h: 0.2,
    fontFace: "Aptos", fontSize: 12, bold: true,
    color: "C8E4EA", margin: 0,
  });
  slide.addText(item.title, {
    x: 0.72, y: 1.46, w: 4.9, h: 0.95,
    fontFace: "Aptos Display", fontSize: 28, bold: true,
    color: COLORS.white, margin: 0,
  });
  slide.addText(item.subtitle, {
    x: 0.72, y: 2.58, w: 4.95, h: 0.8,
    fontFace: "Aptos", fontSize: 15,
    color: "D9EEF2", margin: 0,
  });
  addCard(slide, 0.72, 4.02, 3.32, 0.64, "1E3849");
  slide.addText(`${item.presenter}  |  5-minute oral presentation`, {
    x: 0.9, y: 4.24, w: 2.95, h: 0.15,
    fontFace: "Aptos", fontSize: 11, color: COLORS.white, margin: 0,
  });
}

function addProblemSlide(slide, item) {
  slide.background = { color: COLORS.mist };
  addSectionHeader(slide, item.title, item.label);
  slide.addText(item.headline, {
    x: 0.72, y: 1.02, w: 4.35, h: 0.74,
    fontFace: "Aptos Display", fontSize: 22, bold: true,
    color: COLORS.ink, margin: 0,
  });
  addBulletList(slide, item.bullets, { x: 0.86, y: 1.95, w: 3.9, h: 2.05, fontSize: 15.5 });
  if (hasAsset("problem-visual.png")) {
    slide.addImage({
      path: assetPath("problem-visual.png"),
      x: 5.35, y: 1.05, w: 3.88, h: 3.18,
      sizing: { type: "cover", x: 5.35, y: 1.05, w: 3.88, h: 3.18 },
    });
  } else {
    addCard(slide, 5.35, 1.05, 3.88, 3.18, "E9F5F7");
  }
  slide.addText("Input data", {
    x: 5.6, y: 1.35, w: 1.15, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  slide.addText("recipes + ingredients", {
    x: 5.55, y: 1.62, w: 1.6, h: 0.2,
    fontFace: "Consolas", fontSize: 12, color: COLORS.ink, margin: 0,
  });
  slide.addText(">", {
    x: 6.58, y: 2.0, w: 0.2, h: 0.18,
    fontFace: "Aptos Display", fontSize: 16, bold: true,
    color: COLORS.teal, align: "center", margin: 0,
  });
  slide.addText("relational storage", {
    x: 6.98, y: 2.06, w: 1.3, h: 0.16,
    fontFace: "Aptos", fontSize: 10.5, bold: true, color: COLORS.ink, margin: 0,
  });
  slide.addText(">", {
    x: 7.82, y: 2.0, w: 0.2, h: 0.18,
    fontFace: "Aptos Display", fontSize: 16, bold: true,
    color: COLORS.teal, align: "center", margin: 0,
  });
  slide.addText("analytics output", {
    x: 8.22, y: 2.06, w: 0.8, h: 0.16,
    fontFace: "Aptos", fontSize: 10.5, bold: true, color: COLORS.ink, margin: 0,
  });
  addFooterRule(slide);
}

function addArchitectureSlide(slide, item) {
  slide.background = { color: COLORS.mist };
  addSectionHeader(slide, item.title, item.label);
  addCard(slide, 0.68, 1.06, 2.1, 3.48, "FFFFFF");
  slide.addText("Technology stack", {
    x: 0.88, y: 1.28, w: 1.5, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  item.stack.forEach((stackItem, index) => {
    const top = 1.62 + index * 0.52;
    addCard(slide, 0.9, top, 1.62, 0.34, index % 2 === 0 ? "EAF4F6" : "F0F4F7");
    slide.addText(stackItem, {
      x: 1.02, y: top + 0.1, w: 1.35, h: 0.11,
      fontFace: "Aptos", fontSize: 10.4, bold: true, color: COLORS.ink, align: "center", margin: 0,
    });
  });
  addCard(slide, 3.05, 1.06, 6.2, 2.15, "FFFFFF");
  slide.addText("Request flow", {
    x: 3.28, y: 1.28, w: 1.3, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  addFlowBoxes(slide, item.flow, 3.28, 1.68, 5.5);
  slide.addText(item.notes.join("\n"), {
    x: 3.28, y: 2.68, w: 5.35, h: 0.8,
    fontFace: "Aptos", fontSize: 13.2, color: COLORS.ink, margin: 0,
  });
  addCard(slide, 3.05, 3.45, 6.2, 1.09, "EAF4F6");
  slide.addText("This structure helps in the oral exam because each layer has a clear responsibility: routers for HTTP, schemas for validation, services for derived logic, and models for persistence.", {
    x: 3.28, y: 3.76, w: 5.62, h: 0.45,
    fontFace: "Aptos", fontSize: 12.8, color: COLORS.ink, margin: 0, align: "left",
  });
  addFooterRule(slide);
}

function addDataApiSlide(slide, item) {
  slide.background = { color: COLORS.mist };
  addSectionHeader(slide, item.title, item.label);
  addCard(slide, 0.7, 1.08, 5.85, 3.12, "FFFFFF");
  slide.addText("ER view of the core SQL model", {
    x: 0.93, y: 1.28, w: 1.95, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  if (hasAsset("er-diagram.png")) {
    slide.addImage({
      path: assetPath("er-diagram.png"),
      x: 0.94, y: 1.6, w: 5.35, h: 2.3,
      sizing: { type: "contain", x: 0.94, y: 1.6, w: 5.35, h: 2.3 },
    });
  } else {
    item.entities.forEach((entity, index) => {
      addEntityCard(slide, 0.86, 1.56 + index * 0.72, entity.name, entity.desc, index === 1 ? "E9F5F7" : "FFFFFF");
    });
  }
  addCard(slide, 6.82, 1.08, 2.48, 3.12, "FDFEFE");
  slide.addText("Why this matters", {
    x: 7.05, y: 1.28, w: 1.4, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  slide.addText(
    "The join table stores quantity_g, so nutrition can be calculated from linked ingredient data instead of hardcoded recipe totals.",
    {
      x: 7.05, y: 1.58, w: 1.98, h: 0.82,
      fontFace: "Aptos", fontSize: 11.3, color: COLORS.ink, margin: 0,
    }
  );
  if (hasAsset("category-analytics-chart.png")) {
    slide.addImage({
      path: assetPath("category-analytics-chart.png"),
      x: 7.02, y: 2.45, w: 2.06, h: 1.18,
      sizing: { type: "contain", x: 7.02, y: 2.45, w: 2.06, h: 1.18 },
    });
  }
  slide.addText("Representative endpoints", {
    x: 7.05, y: 3.72, w: 1.4, h: 0.15,
    fontFace: "Aptos", fontSize: 9.4, bold: true, color: COLORS.slate, margin: 0,
  });
  slide.addText(item.endpoints.slice(0, 4).join("\n"), {
    x: 7.05, y: 3.92, w: 1.98, h: 0.56,
    fontFace: "Consolas", fontSize: 8.7, color: COLORS.ink, margin: 0,
  });
  addFooterRule(slide);
}

function addQualitySlide(slide, item) {
  slide.background = { color: COLORS.mist };
  addSectionHeader(slide, item.title, item.label);
  addMiniStat(slide, 0.78, 1.2, item.stats[0].value, item.stats[0].caption, COLORS.mint);
  addMiniStat(slide, 2.72, 1.2, item.stats[1].value, item.stats[1].caption, COLORS.sky);
  addCard(slide, 0.78, 2.55, 4.9, 1.78, "FFFFFF");
  slide.addText("Controls and validation", {
    x: 1.0, y: 2.8, w: 1.8, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  addBulletList(slide, item.bullets.slice(0, 2), { x: 1.0, y: 3.08, w: 2.55, h: 0.95, fontSize: 13.2 });
  addCard(slide, 3.64, 2.9, 1.72, 1.04, COLORS.amber);
  slide.addText(item.stats[2].value, {
    x: 3.84, y: 3.04, w: 1.3, h: 0.28,
    fontFace: "Aptos Display", fontSize: 24, bold: true,
    color: COLORS.ink, align: "center", margin: 0,
  });
  slide.addText("schema validation\nresponses", {
    x: 3.8, y: 3.42, w: 1.38, h: 0.3,
    fontFace: "Aptos", fontSize: 9.4, color: COLORS.slate,
    align: "center", margin: 0,
  });
  slide.addText("Rejected before service logic runs", {
    x: 3.78, y: 3.78, w: 1.42, h: 0.18,
    fontFace: "Aptos", fontSize: 8.5, color: COLORS.ink,
    align: "center", margin: 0,
  });
  addCard(slide, 5.95, 1.2, 3.28, 3.13, "132238");
  slide.addText("Automated verification", {
    x: 6.18, y: 1.48, w: 1.7, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: "D7EEF2", margin: 0,
  });
  slide.addText("15 passed", {
    x: 6.18, y: 1.92, w: 2.1, h: 0.42,
    fontFace: "Consolas", fontSize: 28, bold: true, color: "86EFAC", margin: 0,
  });
  slide.addText("health | CRUD | search | analytics | nutrition | relationship removal", {
    x: 6.18, y: 2.48, w: 2.55, h: 0.62,
    fontFace: "Aptos", fontSize: 11.4, color: COLORS.white, margin: 0,
  });
  slide.addText(item.bullets[2], {
    x: 6.18, y: 3.28, w: 2.62, h: 0.52,
    fontFace: "Aptos", fontSize: 10.8, color: "D9EEF2", margin: 0,
  });
  addFooterRule(slide);
}

function addApiDocsSlide(slide, item) {
  slide.background = { color: COLORS.mist };
  addSectionHeader(slide, item.title, item.label);
  addCard(slide, 0.72, 1.08, 5.18, 3.2, "FFFFFF");
  slide.addText("Real Swagger UI browser capture", {
    x: 0.96, y: 1.32, w: 2.05, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  if (hasAsset("swagger-ui-screenshot.png")) {
    slide.addImage({
      path: assetPath("swagger-ui-screenshot.png"),
      x: 0.98, y: 1.66, w: 4.68, h: 2.42,
      sizing: { type: "contain", x: 0.98, y: 1.66, w: 4.68, h: 2.42 },
    });
  } else {
    slide.addShape(PPTX.ShapeType.rect, {
      x: 0.98, y: 1.7, w: 4.68, h: 2.18,
      fill: { color: "F8FBFC" },
      line: { color: COLORS.border, width: 1 },
    });
    slide.addText("/docs", {
      x: 1.18, y: 1.9, w: 0.6, h: 0.18,
      fontFace: "Consolas", fontSize: 15, bold: true, color: COLORS.teal, margin: 0,
    });
    slide.addText("GET /recipes\nPOST /recipes\nGET /recipes/{id}/nutrition\nGET /analytics/recipes/by-category", {
      x: 1.18, y: 2.28, w: 1.95, h: 1.2,
      fontFace: "Consolas", fontSize: 10.6, color: COLORS.ink, margin: 0,
    });
  }
  addCard(slide, 6.12, 1.08, 3.12, 3.2, "EAF4F6");
  slide.addText("Response evidence and pack", {
    x: 6.36, y: 1.32, w: 1.8, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  if (hasAsset("api-response-examples.png")) {
    slide.addImage({
      path: assetPath("api-response-examples.png"),
      x: 6.34, y: 1.68, w: 2.67, h: 1.8,
      sizing: { type: "contain", x: 6.34, y: 1.68, w: 2.67, h: 1.8 },
    });
  }
  slide.addText(item.callouts.join(" | "), {
    x: 6.38, y: 3.64, w: 2.56, h: 0.3,
    fontFace: "Aptos", fontSize: 10.2, bold: true, color: COLORS.ink, align: "center", margin: 0,
  });
  slide.addText(item.highlights[1], {
    x: 6.38, y: 3.98, w: 2.54, h: 0.32,
    fontFace: "Aptos", fontSize: 9.4, color: COLORS.slate, align: "center", margin: 0,
  });
  addFooterRule(slide);
}

function addVersionControlSlide(slide, item) {
  slide.background = { color: COLORS.mist };
  addSectionHeader(slide, item.title, item.label);
  addCard(slide, 0.72, 1.08, 4.3, 3.22, "FFFFFF");
  slide.addText("Commit history evidence", {
    x: 0.98, y: 1.32, w: 1.7, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  addCommitTimeline(slide, item.commits);
  addCard(slide, 5.25, 1.08, 3.98, 3.22, "FFFFFF");
  slide.addText("Submission deliverables", {
    x: 5.5, y: 1.32, w: 1.6, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  addDeliverableGrid(slide, item.deliverables);
  addFooterRule(slide);
}

function addDemoReportSlide(slide, item) {
  slide.background = { color: COLORS.mist };
  addSectionHeader(slide, item.title, item.label);
  addCard(slide, 0.7, 1.08, 4.15, 3.18, "FFFFFF");
  slide.addText("Live presentation path", {
    x: 0.95, y: 1.32, w: 1.5, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  addNumberedSteps(slide, item.demoSteps, 0.98, 1.7, 3.35);
  addCard(slide, 5.08, 1.08, 4.15, 3.18, "EAF4F6");
  slide.addText("Technical report highlights", {
    x: 5.35, y: 1.32, w: 1.7, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.slate, margin: 0,
  });
  addBulletList(slide, item.reportPoints, { x: 5.34, y: 1.7, w: 3.25, h: 1.7, fontSize: 13.4 });
  addCard(slide, 5.35, 3.5, 3.35, 0.58, COLORS.white);
  slide.addText("This gives examiners a clean path from repository evidence to working endpoints and supporting documents.", {
    x: 5.56, y: 3.68, w: 2.95, h: 0.16,
    fontFace: "Aptos", fontSize: 10.8, color: COLORS.ink, align: "center", margin: 0,
  });
  addFooterRule(slide);
}

function addConclusionSlide(slide, item) {
  slide.background = { color: COLORS.navy };
  slide.addText(item.title, {
    x: 0.7, y: 0.48, w: 5.8, h: 0.42,
    fontFace: "Aptos Display", fontSize: 24, bold: true,
    color: COLORS.white, margin: 0,
  });
  slide.addShape(PPTX.ShapeType.rect, {
    x: 0.72, y: 1.15, w: 4.3, h: 2.6,
    fill: { color: COLORS.white, transparency: 5 },
    line: { color: "D8E8EE", width: 1 },
  });
  slide.addText("Key outcome", {
    x: 0.96, y: 1.42, w: 1.2, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: COLORS.teal, margin: 0,
  });
  slide.addText(item.outcome, {
    x: 0.96, y: 1.78, w: 3.7, h: 1.1,
    fontFace: "Aptos", fontSize: 15.2, color: COLORS.ink, margin: 0,
  });
  slide.addText("Future work", {
    x: 5.42, y: 1.42, w: 1.1, h: 0.18,
    fontFace: "Aptos", fontSize: 11, bold: true, color: "D6EEF2", margin: 0,
  });
  slide.addText(
    item.future.map((text, index) => ({
      text,
      options: { bullet: true, breakLine: index < item.future.length - 1, paraSpaceAfterPt: 10 },
    })),
    {
      x: 5.42, y: 1.78, w: 3.1, h: 1.25,
      fontFace: "Aptos", fontSize: 13.2, color: COLORS.white, margin: 0,
    }
  );
  slide.addShape(PPTX.ShapeType.rect, {
    x: 5.18, y: 3.34, w: 4.05, h: 0.92,
    fill: { color: COLORS.teal, transparency: 8 },
    line: { color: COLORS.teal, width: 1 },
  });
  slide.addText("GenAI declaration", {
    x: 5.45, y: 3.56, w: 1.35, h: 0.16,
    fontFace: "Aptos", fontSize: 10.5, bold: true, color: "D6EEF2", margin: 0,
  });
  slide.addText(item.genai, {
    x: 5.45, y: 3.83, w: 3.35, h: 0.28,
    fontFace: "Aptos", fontSize: 10.6, color: COLORS.white, margin: 0,
  });
  slide.addText("Q&A ready: architecture choices, testing evidence, route design, and submission deliverables", {
    x: 0.75, y: 4.58, w: 8.0, h: 0.18,
    fontFace: "Aptos", fontSize: 12, bold: true, color: "CFE7EC", margin: 0,
  });
}

function renderSlides() {
  deckContent.forEach((item, index) => {
    const slide = PPTX.addSlide();
    switch (item.key) {
      case "title":
        addCoverSlide(slide, item);
        break;
      case "problem_context":
        addProblemSlide(slide, item);
        break;
      case "architecture":
        addArchitectureSlide(slide, item);
        break;
      case "data_api":
        addDataApiSlide(slide, item);
        break;
      case "quality":
        addQualitySlide(slide, item);
        break;
      case "api_docs":
        addApiDocsSlide(slide, item);
        break;
      case "version_control":
        addVersionControlSlide(slide, item);
        break;
      case "demo_report":
        addDemoReportSlide(slide, item);
        break;
      case "conclusion":
        addConclusionSlide(slide, item);
        break;
      default:
        slide.background = { color: COLORS.mist };
    }
    addPageNumber(slide, index + 1);
  });
}

async function main() {
  ensureDirs();
  setMetadata();
  renderSlides();
  const outputName = process.env.PPTX_OUT_NAME || "nutrition-api-deck.pptx";
  await PPTX.writeFile({ fileName: path.join(OUT_DIR, outputName) });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
