# Pitch video (Start-up Center Wuppertal, 60 s)

Animated graphics for the 60-second application video.

- `pitch.html`: the animation. Open it in a browser for a live preview (`pitch.html?lang=de` for German). Team, city, price and contact live in the `CONFIG` block at the top of the script.
- `render.mjs`: renders the animation to MP4, frame by frame (needs Node, Playwright and ffmpeg).
  `node render.mjs en` or `node render.mjs de`; stills: `node render.mjs en --stills 3,20,40`
- `make_srt.py`: writes EN/DE subtitle files from the voice-over script: `python3 make_srt.py <out-dir>`
