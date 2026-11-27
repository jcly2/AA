const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const dir = process.argv[2];
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 4000, height: 3000 } });
  for (const f of files) {
    const svg = fs.readFileSync(dir + '/' + f, 'utf8');
    await page.setContent('<html><body style="margin:0">' + svg + '</body></html>');
    const data = await page.evaluate(() => {
      const svg = document.querySelector('svg');
      const vb = svg.viewBox.baseVal;
      svg.style.maxWidth = 'none';
      svg.setAttribute('width', vb.width);
      svg.setAttribute('height', vb.height);
      const o0 = svg.getBoundingClientRect();
      const o = { x: o0.x - vb.x, y: o0.y - vb.y };
      const rel = r => ({ x: r.x - o.x, y: r.y - o.y, w: r.width, h: r.height });
      const txt = el => el ? (el.innerText || el.textContent || '').trim() : '';
      const nodes = [...svg.querySelectorAll('g.node')].map(g => {
        const shape = g.querySelector('.label-container, rect, circle, polygon, path');
        const lab = g.querySelector('.nodeLabel') || g.querySelector('.label');
        const html = lab ? lab.innerHTML : '';
        return { id: g.id, cls: g.getAttribute('class'), shape: shape ? shape.tagName : '', box: rel((shape || g).getBoundingClientRect()), label: txt(lab), html };
      });
      const clusters = [...svg.querySelectorAll('g.cluster')].map(g => {
        const r = g.querySelector('rect');
        return { id: g.id, box: rel(r.getBoundingClientRect()), label: txt(g.querySelector('.cluster-label')) };
      });
      const edges = [...svg.querySelectorAll('path.flowchart-link')].map(p => {
        let pts = [];
        try { pts = JSON.parse(atob(p.getAttribute('data-points'))); } catch (e) {}
        const id = p.getAttribute('data-id');
        const lab = svg.querySelector('.edgeLabel .label[data-id="' + id + '"]');
        return { id, cls: p.getAttribute('class'), end: !!p.getAttribute('marker-end'), start: !!p.getAttribute('marker-start'), pts, label: txt(lab) };
      });
      // sequence diagrams: generic texts
      return { w: vb.width, h: vb.height, nodes, clusters, edges };
    });
    fs.writeFileSync(dir + '/' + f.replace('.svg', '.json'), JSON.stringify(data, null, 1));
  }
  await browser.close();
})();
