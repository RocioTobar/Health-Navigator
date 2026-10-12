// Renders each overlay clip from overlays.html.
// Transparent clips -> <name>.mov (ProRes 4444 with alpha) + <name>-verde.mp4 (green screen for CapCut chroma key).
// Opaque clips (full-screen cards, phone screen) -> <name>.mp4.
// Usage: node render-overlays.mjs <out-dir> [clip,clip]   stills: node render-overlays.mjs <out-dir> clip --stills 1,2
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const out = process.argv[2];
const ALL = ['recepcion', 'nombre', 'dato-400k', 'toma-2', 'beneficios', 'competencia', 'modelo', 'cierre', 'app-movil'];
const OPAQUE = new Set(['toma-2', 'cierre', 'app-movil']);
const clips = process.argv[3] ? process.argv[3].split(',') : ALL;
const stills = process.argv[4] === '--stills' ? process.argv[5].split(',').map(Number) : null;
const FPS = 30;

const browser = await chromium.launch();
for (const clip of clips) {
  const page = await browser.newPage();
  await page.goto(`file://${path.join(dir, 'overlays.html')}?render=1&clip=${clip}`);
  await page.evaluate(() => document.fonts.ready);
  const [w, h] = await page.evaluate(() => window.SIZE);
  const dur = await page.evaluate(() => window.DURATION);
  await page.setViewportSize({ width: w, height: h });
  if (stills) {
    for (const t of stills) {
      await page.evaluate(t => window.render(t), t);
      await page.screenshot({ path: path.join(out, `still-${clip}-${t}.png`), omitBackground: !OPAQUE.has(clip) });
    }
    await page.close(); continue;
  }
  const tmp = mkdtempSync(path.join(os.tmpdir(), 'ov-'));
  for (let f = 0; f < Math.round(dur * FPS); f++) {
    await page.evaluate(t => window.render(t), f / FPS);
    writeFileSync(path.join(tmp, `f${String(f).padStart(5, '0')}.png`), await page.screenshot({ omitBackground: !OPAQUE.has(clip) }));
  }
  const input = ['-y', '-v', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.png')];
  if (OPAQUE.has(clip)) {
    spawnSync('ffmpeg', [...input, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', path.join(out, `${clip}.mp4`)], { stdio: 'inherit' });
  } else {
    spawnSync('ffmpeg', [...input, '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', path.join(out, `${clip}.mov`)], { stdio: 'inherit' });
    spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', `color=c=0x00B140:s=${w}x${h}:r=${FPS}`, '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.png'),
      '-filter_complex', '[0][1]overlay=shortest=1', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', path.join(out, `${clip}-verde.mp4`)], { stdio: 'inherit' });
  }
  rmSync(tmp, { recursive: true });
  console.log('done', clip);
  await page.close();
}
await browser.close();
