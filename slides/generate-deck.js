const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");
const deckContent = require("./content/deck-content");

async function main() {
  const outDir = path.join(__dirname, "output");
  fs.mkdirSync(outDir, { recursive: true });

  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "Shuyu Cao";
  pptx.company = "University Coursework";
  pptx.subject = "XJCO3011 Oral Presentation";
  pptx.title = "Nutrition and Recipe Analytics API";
  pptx.lang = "en-GB";
  pptx.theme = {
    headFontFace: "Aptos Display",
    bodyFontFace: "Aptos",
    lang: "en-GB"
  };

  const colors = {
    navy: "1E2761",
    slate: "36454F",
    offWhite: "F7F8FA",
    darkText: "1F2937",
    muted: "64748B",
    accent: "0E7490",
    border: "D8DEE9"
  };

  const addHeader = (slide, title) => {
    slide.addText(title, {
      x: 0.55, y: 0.35, w: 8.5, h: 0.5,
      fontFace: "Aptos Display", fontSize: 24, bold: true,
      color: colors.darkText, margin: 0
    });
  };

  const addBulletCard = (slide, bullets, options = {}) => {
    const x = options.x ?? 0.6;
    const y = options.y ?? 1.1;
    const w = options.w ?? 8.8;
    const h = options.h ?? 3.9;

    slide.addShape(pptx.ShapeType.rect, {
      x, y, w, h,
      fill: { color: "FFFFFF" },
      line: { color: colors.border, width: 1.2 },
      radius: 0.08,
      shadow: { type: "outer", color: "000000", blur: 1, offset: 1, angle: 45, opacity: 0.08 }
    });

    const runs = [];
    bullets.forEach((bullet, index) => {
      runs.push({
        text: bullet,
        options: {
          bullet: true,
          breakLine: index < bullets.length - 1,
          paraSpaceAfterPt: 10
        }
      });
    });

    slide.addText(runs, {
      x: x + 0.28, y: y + 0.3, w: w - 0.55, h: h - 0.55,
      fontFace: "Aptos", fontSize: 18, color: colors.darkText,
      margin: 0, valign: "top"
    });
  };

  const addAccentTag = (slide, text, options = {}) => {
    const x = options.x ?? 0.6;
    const y = options.y ?? 0.95;
    slide.addShape(pptx.ShapeType.rect, {
      x, y, w: 1.55, h: 0.28,
      fill: { color: colors.accent },
      line: { color: colors.accent, width: 1 }
    });
    slide.addText(text, {
      x: x + 0.08, y: y + 0.02, w: 1.35, h: 0.2,
      fontFace: "Aptos", fontSize: 10, bold: true, color: "FFFFFF", margin: 0
    });
  };

  deckContent.forEach((item, index) => {
    const slide = pptx.addSlide();

    if (index === 0 || index === deckContent.length - 1) {
      slide.background = { color: colors.navy };
    } else {
      slide.background = { color: colors.offWhite };
    }

    if (item.key === "title") {
      slide.addText(item.title, {
        x: 0.7, y: 1.4, w: 7.8, h: 0.9,
        fontFace: "Aptos Display", fontSize: 26, bold: true,
        color: "FFFFFF", margin: 0
      });
      slide.addText(item.subtitle, {
        x: 0.7, y: 2.45, w: 6.7, h: 0.55,
        fontFace: "Aptos", fontSize: 15,
        color: "D6E4FF", margin: 0
      });
      slide.addShape(pptx.ShapeType.rect, {
        x: 7.5, y: 1.2, w: 1.8, h: 2.8,
        fill: { color: "0E7490", transparency: 12 },
        line: { color: "0E7490", width: 1 }
      });
      slide.addText("XJCO3011\nWeb Services\nand Web Data", {
        x: 7.75, y: 1.8, w: 1.3, h: 1.5,
        align: "center", valign: "mid", margin: 0,
        fontFace: "Aptos", fontSize: 16, bold: true, color: "FFFFFF"
      });
      return;
    }

    if (item.key === "conclusion") {
      slide.addText(item.title, {
        x: 0.65, y: 0.45, w: 7.2, h: 0.55,
        fontFace: "Aptos Display", fontSize: 24, bold: true,
        color: "FFFFFF", margin: 0
      });
      slide.addShape(pptx.ShapeType.rect, {
        x: 0.65, y: 1.25, w: 4.35, h: 2.7,
        fill: { color: "FFFFFF", transparency: 6 },
        line: { color: "D6E4FF", width: 1.1 }
      });
      slide.addText("Key outcome", {
        x: 0.9, y: 1.48, w: 1.8, h: 0.25,
        fontFace: "Aptos", fontSize: 11, bold: true, color: "D6E4FF", margin: 0
      });
      slide.addText(item.bullets[0], {
        x: 0.9, y: 1.8, w: 3.7, h: 1.4,
        fontFace: "Aptos", fontSize: 18, color: "FFFFFF", margin: 0
      });
      slide.addShape(pptx.ShapeType.rect, {
        x: 5.3, y: 1.25, w: 4.0, h: 2.7,
        fill: { color: "0E7490", transparency: 8 },
        line: { color: "0E7490", width: 1.1 }
      });
      slide.addText("Next steps", {
        x: 5.55, y: 1.48, w: 1.7, h: 0.25,
        fontFace: "Aptos", fontSize: 11, bold: true, color: "D6E4FF", margin: 0
      });
      slide.addText([
        { text: item.bullets[1], options: { breakLine: true, paraSpaceAfterPt: 10 } },
        { text: item.bullets[2] }
      ], {
        x: 5.55, y: 1.82, w: 3.35, h: 1.65,
        fontFace: "Aptos", fontSize: 16, color: "FFFFFF", margin: 0
      });
      return;
    }

    addHeader(slide, item.title);
    addAccentTag(slide, item.key.replace("_", " ").toUpperCase());
    addBulletCard(slide, item.bullets);

    if (item.key === "stack_architecture") {
      slide.addShape(pptx.ShapeType.line, {
        x: 5.9, y: 1.55, w: 3.0, h: 0,
        line: { color: colors.accent, width: 2 }
      });
      ["Client", "Routers", "Services", "SQLite"].forEach((label, idx) => {
        slide.addShape(pptx.ShapeType.rect, {
          x: 5.95 + idx * 0.72, y: 1.34, w: 0.62, h: 0.38,
          fill: { color: idx % 2 === 0 ? "E2F3F5" : "D8E6F6" },
          line: { color: colors.border, width: 1 }
        });
        slide.addText(label, {
          x: 6.0 + idx * 0.72, y: 1.44, w: 0.52, h: 0.12,
          fontFace: "Aptos", fontSize: 8.5, bold: true, align: "center",
          color: colors.darkText, margin: 0
        });
      });
    }

    if (item.key === "quality") {
      slide.addShape(pptx.ShapeType.rect, {
        x: 6.5, y: 2.8, w: 2.2, h: 0.95,
        fill: { color: "1F2937" },
        line: { color: "1F2937", width: 1 }
      });
      slide.addText("15 passed", {
        x: 6.65, y: 3.0, w: 1.9, h: 0.28,
        fontFace: "Consolas", fontSize: 24, bold: true,
        color: "86EFAC", align: "center", margin: 0
      });
      slide.addText("pytest verification", {
        x: 6.8, y: 3.36, w: 1.6, h: 0.16,
        fontFace: "Aptos", fontSize: 9.5, color: "D1D5DB", align: "center", margin: 0
      });
    }
  });

  await pptx.writeFile({ fileName: path.join(outDir, "nutrition-api-deck.pptx") });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
