/**
 * Gera o PDF do carrossel de LinkedIn a partir do HTML estático.
 * Usa Puppeteer em modo headless; aplica @media print (animações desativadas).
 *
 * Uso:
 *   node scripts/generate-pdf.js
 *
 * Saída:
 *   docs/linkedin/slides.pdf  (8 páginas 1080×1350 px)
 */

'use strict';

const puppeteer = require('puppeteer');
const http      = require('http');
const fs        = require('fs');
const path      = require('path');

const HTML_FILE  = path.resolve(__dirname, '..', 'support-ticket-insight-lab.slides.html');
const OUTPUT_PDF = path.resolve(__dirname, '..', 'docs', 'linkedin', 'slides.pdf');
const PORT       = 54321;

/* Serve o HTML via HTTP local para que o Puppeteer carregue Google Fonts */
function createServer() {
  return http.createServer((req, res) => {
    fs.readFile(HTML_FILE, (err, data) => {
      if (err) { res.writeHead(500); res.end('Erro ao ler HTML'); return; }
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(data);
    });
  }).listen(PORT);
}

async function generate() {
  const server  = createServer();
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  try {
    const page = await browser.newPage();

    /* Viewport compatível com a largura dos slides */
    await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 2 });

    await page.goto(`http://localhost:${PORT}`, { waitUntil: 'networkidle2', timeout: 30000 });

    /* Aguarda fontes e qualquer renderização pendente */
    await page.evaluateHandle('document.fonts.ready');
    await new Promise(r => setTimeout(r, 800));

    /* Garante que o @media print seja respeitado */
    await page.emulateMediaType('print');

    await page.pdf({
      path:            OUTPUT_PDF,
      width:           '1080px',
      height:          '1350px',
      printBackground: true,
      margin:          { top: 0, right: 0, bottom: 0, left: 0 },
    });

    console.log(`PDF gerado: ${OUTPUT_PDF}`);
  } finally {
    await browser.close();
    server.close();
  }
}

generate().catch(err => { console.error(err); process.exit(1); });
