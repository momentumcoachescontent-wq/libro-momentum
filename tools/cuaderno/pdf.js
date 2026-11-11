const { chromium } = require('playwright');
const fs = require('fs');
const dir = __dirname;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + dir + '/portada.html');
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: dir + '/portada.pdf', width: '5.5in', height: '8.5in', printBackground: true, preferCSSPageSize: true });
  await p.goto('file://' + dir + '/cuaderno.html');
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({
    path: dir + '/cuerpo.pdf', width: '5.5in', height: '8.5in', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: fs.readFileSync(dir + '/pie.html', 'utf8'),
  });
  await b.close();
})();
