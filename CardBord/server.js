const { createServer } = require('node:http');
const { readFileSync } = require('node:fs');

const hostname = '127.0.0.1';
const port = 8080;

const server = createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');

    const html = readFileSync('./index.html');
    res.end(html);
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
