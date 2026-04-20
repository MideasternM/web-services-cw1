const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");

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

  const slide = pptx.addSlide();
  slide.background = { color: "1E2761" };
  slide.addText("Nutrition and Recipe Analytics API", {
    x: 0.6,
    y: 1.7,
    w: 8.8,
    h: 0.7,
    fontFace: "Aptos Display",
    fontSize: 24,
    bold: true,
    color: "FFFFFF",
    margin: 0
  });
  slide.addText("A FastAPI and SQLite data-driven web service with CRUD and nutrition analytics", {
    x: 0.6,
    y: 2.55,
    w: 8.5,
    h: 0.45,
    fontFace: "Aptos",
    fontSize: 14,
    color: "D6E4FF",
    margin: 0
  });

  await pptx.writeFile({ fileName: path.join(outDir, "nutrition-api-deck.pptx") });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
