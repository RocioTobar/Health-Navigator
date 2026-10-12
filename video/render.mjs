// Renders pitch.html to MP4 (1920x1080, 30 fps) frame by frame.
// Usage: node render.mjs [en|de] [out.mp4]        stills: node render.mjs en --stills 3,8,15
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const lang = process.argv[2] || 'en';
const out = process.argv[3] || path.join(dir, `health-navigator-pitch-${lang}.mp4`);
const FPS = 30, DURATION = 60;

const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(`file://${path.join(dir, process.env.PAGE || 'pitch.html')}?render=1&lang=${lang}`);
await page.evaluate(() => document.fonts.ready);

if (process.argv[3] === '--stills') {
  for (const t of process.argv[4].split(',').map(Number)) {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: path.join(dir, `still-${lang}-${t}.png`) });
  }
} else {
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < FPS * DURATION; f++) {
    await page.evaluate(t => window.render(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('wrote', out);
}
await browser.close();
