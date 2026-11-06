import { spawn } from 'child_process';
import http from 'http';
import os from 'os';
import path from 'path';
import fs from 'fs';

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const URL_TO_TEST = process.argv[2] || 'https://hosseinykala.ir/';

async function getJson(url) {
    return new Promise((resolve, reject) => {
        http.get(url, res => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => resolve(JSON.parse(data)));
        }).on('error', reject);
    });
}

async function measurePage(targetUrl) {
    const tmpProfile = path.join(os.tmpdir(), 'chrome_perf_' + Date.now());
    fs.mkdirSync(tmpProfile, { recursive: true });

    const port = 9334;
    const chrome = spawn(CHROME_PATH, [
        '--headless=new',
        `--remote-debugging-port=${port}`,
        '--disable-gpu',
        '--no-sandbox',
        '--disable-extensions',
        '--window-size=1366,768',
        `--user-data-dir=${tmpProfile}`
    ]);

    await new Promise(r => setTimeout(r, 2000));

    try {
        const pages = await getJson(`http://127.0.0.1:${port}/json`);
        const page = pages.find(p => p.type === 'page');
        if (!page) throw new Error('No page target found');

        const ws = new WebSocket(page.webSocketDebuggerUrl);
        await new Promise(r => ws.onopen = r);

        let id = 1;
        const pending = new Map();
        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.id && pending.has(msg.id)) {
                pending.get(msg.id)(msg);
                pending.delete(msg.id);
            }
        };

        function send(method, params = {}) {
            return new Promise((resolve) => {
                const reqId = id++;
                pending.set(reqId, resolve);
                ws.send(JSON.stringify({ id: reqId, method, params }));
            });
        }

        await send('Network.enable');
        await send('Page.enable');
        await send('Performance.enable');

        const networkRequests = [];
        let totalTransferred = 0;

        ws.addEventListener('message', (event) => {
            const msg = JSON.parse(event.data);
            if (msg.method === 'Network.responseReceived') {
                networkRequests.push({
                    url: msg.params.response.url,
                    mimeType: msg.params.response.mimeType,
                    status: msg.params.response.status
                });
            } else if (msg.method === 'Network.loadingFinished') {
                totalTransferred += msg.params.encodedDataLength || 0;
            }
        });

        console.log(`Navigating in headless Chrome to ${targetUrl}...`);
        await send('Page.navigate', { url: targetUrl });

        await new Promise((resolve) => {
            const listener = (event) => {
                const msg = JSON.parse(event.data);
                if (msg.method === 'Page.loadEventFired') {
                    ws.removeEventListener('message', listener);
                    resolve();
                }
            };
            ws.addEventListener('message', listener);
            setTimeout(resolve, 25000);
        });

        await new Promise(r => setTimeout(r, 3000));

        const evalMetrics = await send('Runtime.evaluate', {
            expression: `(() => {
                const t = window.performance.timing;
                const p = window.performance.getEntriesByType('paint');
                const fcpEntry = p.find(x => x.name === 'first-contentful-paint');
                
                return {
                    navigationStart: t.navigationStart,
                    responseStart: t.responseStart,
                    ttfb: t.responseStart - t.navigationStart,
                    domInteractive: t.domInteractive - t.navigationStart,
                    domContentLoaded: t.domContentLoadedEventEnd - t.navigationStart,
                    loadEvent: t.loadEventEnd - t.navigationStart,
                    fcp: fcpEntry ? fcpEntry.startTime : null
                };
            })()`,
            returnByValue: true
        });

        const perfMetricsRaw = await send('Performance.getMetrics');
        const perfMetrics = {};
        for (const m of perfMetricsRaw.result.metrics) {
            perfMetrics[m.name] = m.value;
        }

        const m = evalMetrics.result.value || {};
        console.log('\n=============================================');
        console.log(`Results for ${targetUrl}`);
        console.log('=============================================');
        console.log(`- Browser TTFB: ${m.ttfb} ms`);
        console.log(`- First Contentful Paint (FCP): ${m.fcp ? m.fcp.toFixed(1) : 'N/A'} ms`);
        console.log(`- DOM Interactive: ${m.domInteractive} ms`);
        console.log(`- DOM Content Loaded: ${m.domContentLoaded} ms`);
        console.log(`- Page Load Complete: ${m.loadEvent} ms`);
        console.log(`- Total HTTP Requests: ${networkRequests.length}`);
        console.log(`- Total Transferred: ${(totalTransferred / 1024).toFixed(1)} KB`);
        console.log(`- JS Heap Used: ${(perfMetrics.JSHeapUsedSize / 1024 / 1024).toFixed(2)} MB`);
        console.log(`- Main Thread Task Duration: ${(perfMetrics.TaskDuration * 1000).toFixed(1)} ms`);

        ws.close();
        chrome.kill();
        setTimeout(() => {
            try { fs.rmSync(tmpProfile, { recursive: true, force: true }); } catch (e) {}
        }, 1000);

    } catch (e) {
        chrome.kill();
        setTimeout(() => {
            try { fs.rmSync(tmpProfile, { recursive: true, force: true }); } catch (e) {}
        }, 1000);
        console.error('Error:', e);
    }
}

measurePage(URL_TO_TEST);
