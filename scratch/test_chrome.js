const { spawn } = require('child_process');
const http = require('http');

async function run() {
    console.log('Testing native Chrome launch...');
    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const chrome = spawn(chromePath, [
        '--headless=new',
        '--remote-debugging-port=9222',
        '--disable-gpu',
        '--no-sandbox',
        '--user-data-dir=' + require('os').tmpdir() + '/chrome_perf_profile'
    ]);

    await new Promise(r => setTimeout(r, 2000));

    http.get('http://127.0.0.1:9222/json', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
            console.log('CDP endpoints:', data);
            chrome.kill();
        });
    }).on('error', err => {
        console.error('CDP error:', err);
        chrome.kill();
    });
}

run();
