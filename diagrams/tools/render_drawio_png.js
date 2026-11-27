// draw.io 공식 viewer(viewer-static.min.js)로 .drawio를 PNG로 내보낸다. 서버 없이 페이지에 스크립트를 직접 넣는다.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [inDir, outDir, viewerJs] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2600, height: 2200 }, deviceScaleFactor: 2 });
  for (const f of fs.readdirSync(inDir).filter(x => x.endsWith('.drawio'))) {
    await page.setContent('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}</style></head><body><div id="c"></div></body></html>');
    await page.addScriptTag({ content: "window.DRAWIO_BASE_URL='.';window.DRAWIO_LIGHTBOX_URL='.';" });
    await page.addScriptTag({ path: viewerJs });
    const xml = fs.readFileSync(path.join(inDir, f), 'utf8');
    await page.evaluate((xml) => {
      const div = document.createElement('div');
      div.className = 'mxgraph';
      div.setAttribute('data-mxgraph', JSON.stringify({ xml, highlight: 'none', nav: false, resize: true, toolbar: null, border: 20 }));
      document.getElementById('c').appendChild(div);
      GraphViewer.processElements();
    }, xml);
    await page.waitForTimeout(1200);
    const el = await page.$('.mxgraph svg');
    if (!el) { console.log('no svg', f); continue; }
    await el.screenshot({ path: path.join(outDir, f.replace('.drawio', '.png')) });
    console.log('ok', f);
  }
  await browser.close();
})();
