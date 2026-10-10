const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const ROOT_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

function calculateCost(age, sex, bmi, num_of_children, smoker) {
  return 250 * age - 128 * sex + 370 * bmi + 425 * num_of_children + 24000 * smoker - 12500;
}

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let pathname = parsedUrl.pathname;

  // API endpoint for insurance estimation
  if (pathname === '/api/calculate' && req.method === 'GET') {
    const age = parseFloat(parsedUrl.searchParams.get('age') || 28);
    const sex = parseInt(parsedUrl.searchParams.get('sex') || 0);
    const bmi = parseFloat(parsedUrl.searchParams.get('bmi') || 26.2);
    const num_of_children = parseInt(parsedUrl.searchParams.get('children') || 3);
    const smoker = parseInt(parsedUrl.searchParams.get('smoker') || 0);

    const cost = calculateCost(age, sex, bmi, num_of_children, smoker);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      inputs: { age, sex, bmi, num_of_children, smoker },
      insurance_cost: cost,
      monthly_cost: cost / 12,
      formula: `250*${age} - 128*${sex} + 370*${bmi} + 425*${num_of_children} + 24000*${smoker} - 12500`
    }));
    return;
  }

  // Serve static files
  if (pathname === '/' || pathname === '') {
    pathname = '/index.html';
  }

  const filePath = path.join(ROOT_DIR, pathname);

  if (!filePath.startsWith(ROOT_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('403 Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log(`\n=================================================`);
  console.log(` Medical Insurance Cost Intelligence Suite Live!`);
  console.log(` Local Server: http://localhost:${PORT}`);
  console.log(` API Endpoint: http://localhost:${PORT}/api/calculate`);
  console.log(` Directory:    ${ROOT_DIR}`);
  console.log(`=================================================\n`);
});
