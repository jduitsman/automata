/* print.js — HTML naar PDF via de systeem-Chrome, zoals de bestaande PDF's gemaakt zijn */
const path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--font-render-hinting=none'],
  });
  for (const src of process.argv.slice(2)) {
    const out = src.replace(/\.html$/, '.pdf');
    const page = await browser.newPage();
    await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle0', timeout: 90000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise((r) => setTimeout(r, 500));
    await page.pdf({
      path: out,
      printBackground: true,
      preferCSSPageSize: true,
      format: 'A4',
      margin: { top: '13mm', right: '13mm', bottom: '13mm', left: '13mm' },
    });
    console.log('  ✓ ' + path.basename(out));
    await page.close();
  }
  await browser.close();
})();
