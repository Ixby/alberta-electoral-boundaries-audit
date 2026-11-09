// Renders same_votes_five_maps.html to data/maps/article/same_votes_five_maps.png at 2x.
// Usage: node findings/p338_projection/meme/render.cjs   (needs Playwright with Chromium)
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'same_votes_five_maps.html'));
  await p.screenshot({ path: path.join(__dirname, '../../../data/maps/article/same_votes_five_maps.png'),
                       clip: { x: 0, y: 0, width: 1080, height: 1350 } });
  await b.close();
})();
