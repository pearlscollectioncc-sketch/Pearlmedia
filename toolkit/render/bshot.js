// Render brand pages (sizes.json in SRC) with local copies of the Google fonts. Usage: node bshot.js SRC OUT
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const SRC = process.argv[2], OUT = process.argv[3];
const sizes = JSON.parse(fs.readFileSync(SRC + '/sizes.json'));
const R = __dirname + '/node_modules/@fontsource';
const F = {}; const faces = [];
const add = (fam, key, file, w) => { F[key] = file; faces.push(`@font-face{font-family:'${fam}';font-weight:${w};src:url(http://s.test/__f/${key})}`); };
[400, 500, 600].forEach(w => add('Jost', 'j' + w, `${R}/jost/files/jost-latin-${w}-normal.woff2`, w));
[400, 500, 600, 700].forEach(w => add('Cinzel', 'c' + w, `${R}/cinzel/files/cinzel-latin-${w}-normal.woff2`, w));
[500, 600, 700].forEach(w => add('Cormorant Garamond', 'g' + w, `${R}/cormorant-garamond/files/cormorant-garamond-latin-${w}-normal.woff2`, w));
add('Sacramento', 's400', `${R}/sacramento/files/sacramento-latin-400-normal.woff2`, 400);
add('Allura', 'a400', `${R}/allura/files/allura-latin-400-normal.woff2`, 400);
add('Jost', 'j300', `${R}/jost/files/jost-latin-300-normal.woff2`, 300);
[300, 400, 500].forEach(w => add('Tajawal', 't' + w, `${R}/tajawal/files/tajawal-arabic-${w}-normal.woff2`, w));
const css = faces.join('\n');
const types = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
(async () => {
  const b = await chromium.launch({ executablePath: require('fs').existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined });
  for (const [name, [w, h, transparent, scale]] of Object.entries(sizes)) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale || 1 });
    await p.route('**/*', r => { const u = new URL(r.request().url());
      if (u.host === 's.test') {
        if (u.pathname.startsWith('/__f/')) return r.fulfill({ body: fs.readFileSync(F[u.pathname.slice(5)]), contentType: 'font/woff2' });
        const f = path.join(SRC, decodeURIComponent(u.pathname));
        return r.fulfill({ body: fs.readFileSync(f), contentType: types[path.extname(f)] || 'application/octet-stream' }); }
      if (u.host === 'fonts.googleapis.com') return r.fulfill({ body: css, contentType: 'text/css' });
      return r.abort(); });
    await p.goto('http://s.test/' + name + '.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    const ext = name.startsWith('og') ? 'jpg' : 'png';
    await p.screenshot({ path: `${OUT}/${name}.${ext}`, omitBackground: !!transparent, ...(ext === 'jpg' ? { type: 'jpeg', quality: 88 } : {}) });
    console.log(name, w + 'x' + h); await p.close();
  }
  await b.close();
})();
