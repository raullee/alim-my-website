import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
import { execSync } from 'child_process';
import { mkdirSync, existsSync, readdirSync, unlinkSync, rmSync } from 'fs';
import { join, basename } from 'path';

const REELS_DIR = '/Users/raullee/Desktop/VIBECODING/web/alim-my-site/reels';
const FPS = 30;
const FRAME_MS = Math.round(1000 / FPS);

const reels = [
  { file: 'contracts-red-flags.html', duration: 27 },
  { file: 'contracts-anatomy.html', duration: 25 },
  { file: 'copyright-myths.html', duration: 32 },
  { file: 'copyright-fair-dealing.html', duration: 30 },
  { file: 'performer-pay.html', duration: 27 },
  { file: 'performer-checklist.html', duration: 27 },
  { file: 'freelancer-invoice.html', duration: 30 },
  { file: 'freelancer-scope-creep.html', duration: 27 },
];

async function recordReel(browser, reel) {
  const name = reel.file.replace('.html', '');
  const framesDir = join(REELS_DIR, `_frames_${name}`);
  const outputMp4 = join(REELS_DIR, `${name}.mp4`);

  // Clean up any previous frames
  if (existsSync(framesDir)) rmSync(framesDir, { recursive: true });
  mkdirSync(framesDir, { recursive: true });

  console.log(`\n Recording: ${name} (${reel.duration}s @ ${FPS}fps)...`);

  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  // Load the reel
  const fileUrl = `file://${join(REELS_DIR, reel.file)}`;
  await page.goto(fileUrl);

  // Override the reel's transform so it renders at full 1080x1920
  await page.addStyleTag({
    content: `
      .reel {
        transform: none !important;
        transform-origin: top left !important;
      }
      body {
        margin: 0 !important;
        padding: 0 !important;
        display: block !important;
        min-height: auto !important;
      }
    `
  });

  // Wait a beat for styles to apply
  await page.waitForTimeout(200);

  const totalFrames = reel.duration * FPS;

  // Capture frames
  for (let i = 0; i < totalFrames; i++) {
    const frameNum = String(i).padStart(5, '0');
    await page.screenshot({
      path: join(framesDir, `frame_${frameNum}.png`),
      clip: { x: 0, y: 0, width: 1080, height: 1920 },
    });

    if (i < totalFrames - 1) {
      await page.waitForTimeout(FRAME_MS);
    }

    if (i % (FPS * 2) === 0) {
      process.stdout.write(`  ${Math.round((i / totalFrames) * 100)}%`);
    }
  }
  console.log('  100% - captured');

  await context.close();

  // Assemble MP4 with ffmpeg
  console.log(`  Encoding ${name}.mp4...`);
  execSync(
    `ffmpeg -y -framerate ${FPS} -i "${framesDir}/frame_%05d.png" ` +
    `-c:v libx264 -pix_fmt yuv420p -crf 18 -preset fast ` +
    `-vf "scale=1080:1920" ` +
    `"${outputMp4}"`,
    { stdio: 'pipe' }
  );
  console.log(`  Done: ${name}.mp4`);

  // Cleanup frames
  rmSync(framesDir, { recursive: true });
}

async function main() {
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: true });

  for (const reel of reels) {
    await recordReel(browser, reel);
  }

  await browser.close();

  console.log('\n All reels recorded!');
  console.log('Output directory:', REELS_DIR);
}

main().catch(err => { console.error(err); process.exit(1); });
