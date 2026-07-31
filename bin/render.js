/*
 * render.js — rendert een HTML-werkblad twee keer met exact dezelfde layout:
 *   pass A: elk invulveld krijgt een unieke "magic" achtergrondkleur  -> geometrie meten
 *   pass B: schoon, zonder die kleuren                                -> de echte PDF
 * Schrijft <out>/<naam>.marked.pdf, <out>/<naam>.clean.pdf en <out>/<naam>.fields.json
 */
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const MAGIC_R = 254; // rood-kanaal = herkenningsteken, groen+blauw = veldindex

const [, , srcDir, outDir] = process.argv;
if (!srcDir || !outDir) {
  console.error('usage: node render.js <srcDir> <outDir>');
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });

// ── in de browser uitgevoerd: velden inventariseren en uniformeren ────────────
function collectFields(magicR) {
  const SKIP = new Set(['hidden', 'file', 'submit', 'button', 'image', 'reset']);
  const out = [];

  const labelFor = (el) => {
    let t = '';
    if (el.id) {
      const l = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
      if (l) t = l.textContent;
    }
    if (!t) {
      const l = el.closest('label');
      if (l) t = l.textContent;
    }
    if (!t) {
      const wrap = el.closest('.vraag, .idcel, td, li, p, div');
      if (wrap) {
        const l = wrap.querySelector('label');
        if (l) t = l.textContent;
      }
    }
    return t.replace(/\s+/g, ' ').trim().slice(0, 120);
  };

  const els = document.querySelectorAll('input, textarea, select');
  const dropped = [];
  els.forEach((el) => {
    const tag = el.tagName.toLowerCase();
    const type = tag === 'textarea' ? 'textarea'
      : tag === 'select' ? 'select'
        : (el.getAttribute('type') || 'text').toLowerCase();
    if (SKIP.has(type)) return;

    // print-media is al geëmuleerd: wat hier geen doos heeft, staat niet in de PDF
    let target = el;
    let proxy = false;
    let rect = el.getBoundingClientRect();
    if (!el.getClientRects().length || rect.width < 6 || rect.height < 6) {
      // veelgebruikt patroon: een onzichtbare radio/checkbox achter een label
      // dat als knop is opgemaakt — dán is dat label het aanklikbare vlak
      let lab = el.closest('label');
      if (!lab && el.id) lab = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
      const lr = lab && lab.getBoundingClientRect();
      if (lab && lab.getClientRects().length && lr.width >= 6 && lr.height >= 6) {
        target = lab;
        rect = lr;
        proxy = true;
      } else {
        dropped.push((el.dataset.key || el.id || el.name || tag) + ' [' + type + ']');
        return;
      }
    }

    const idx = out.length;
    if (idx > 0xffff) return;

    // checkbox/radio: native rendering vervangen door een simpel vierkant,
    // exact even groot, zodat de layout in beide passes identiek blijft
    if (!proxy && (type === 'checkbox' || type === 'radio')) {
      const cs = getComputedStyle(el);
      const hasBorder = parseFloat(cs.borderTopWidth) > 0;
      el.style.setProperty('-webkit-appearance', 'none', 'important');
      el.style.setProperty('appearance', 'none', 'important');
      el.style.setProperty('width', rect.width + 'px', 'important');
      el.style.setProperty('height', rect.height + 'px', 'important');
      el.style.setProperty('flex', '0 0 auto', 'important');
      if (!hasBorder) el.style.setProperty('border', '1px solid #333', 'important');
      if (type === 'radio') el.style.setProperty('border-radius', '50%', 'important');
    }

    // de placeholder wordt door Chrome méé-geprint en zou onder de ingevulde
    // waarde blijven staan; hij verhuist naar het PDF-veld zelf
    const placeholder = el.getAttribute('placeholder') || '';
    if (placeholder) el.removeAttribute('placeholder');

    target.dataset.pdfIdx = String(idx);
    out.push({
      idx,
      kind: type === 'textarea' ? 'textarea' : type,
      key: el.dataset.key || el.id || el.getAttribute('name') || '',
      group: type === 'radio' ? (el.getAttribute('name') || '') : '',
      value: el.getAttribute('value') || '',
      label: proxy ? (target.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120)
        : labelFor(el),
      placeholder,
      proxy,
      rows: tag === 'textarea' ? (parseInt(el.getAttribute('rows'), 10) || 0) : 0,
      color: [magicR, idx >> 8, idx & 255],
    });
  });
  return { fields: out, dropped };
}

function paint(magicR, on) {
  document.querySelectorAll('[data-pdf-idx]').forEach((el) => {
    const idx = parseInt(el.dataset.pdfIdx, 10);
    if (!on) {
      el.style.removeProperty('background-color');
      el.style.removeProperty('background-image');
      return;
    }
    const c = 'rgb(' + magicR + ',' + (idx >> 8) + ',' + (idx & 255) + ')';
    el.style.setProperty('background-color', c, 'important');
    el.style.setProperty('background-image', 'none', 'important');
    el.style.setProperty('-webkit-print-color-adjust', 'exact', 'important');
    el.style.setProperty('print-color-adjust', 'exact', 'important');
  });
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--font-render-hinting=none'],
  });

  const files = fs.readdirSync(srcDir).filter((f) => f.endsWith('.html')).sort();
  const summary = [];

  for (const file of files) {
    const base = path.basename(file, '.html');
    const page = await browser.newPage();
    page.on('pageerror', (e) => console.warn(`  ! js-fout in ${file}: ${e.message}`));

    await page.goto('file://' + path.resolve(srcDir, file), {
      waitUntil: 'networkidle0',
      timeout: 90000,
    });
    await page.evaluate(() => document.fonts.ready);
    await new Promise((r) => setTimeout(r, 600)); // ruimte voor JS-opgebouwde velden

    await page.emulateMediaType('print');
    const { fields, dropped } = await page.evaluate(collectFields, MAGIC_R);
    if (dropped.length) console.warn(`  ! ${base}: niet in de PDF — ${dropped.join(', ')}`);

    const pdfOpts = {
      printBackground: true,
      preferCSSPageSize: true,
      format: 'A4',
      margin: { top: '13mm', right: '13mm', bottom: '13mm', left: '13mm' },
    };

    await page.evaluate(paint, MAGIC_R, true);
    await page.pdf({ ...pdfOpts, path: path.join(outDir, base + '.marked.pdf') });

    await page.evaluate(paint, MAGIC_R, false);
    await page.pdf({ ...pdfOpts, path: path.join(outDir, base + '.clean.pdf') });

    fs.writeFileSync(
      path.join(outDir, base + '.fields.json'),
      JSON.stringify({ base, title: await page.title(), fields }, null, 1)
    );
    summary.push(`${base}: ${fields.length} velden`);
    console.log(`  ✓ ${base} — ${fields.length} velden`);
    await page.close();
  }

  await browser.close();
  console.log('\n' + summary.join('\n'));
})();
