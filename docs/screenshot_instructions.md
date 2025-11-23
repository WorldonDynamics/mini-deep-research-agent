# How to capture and add a real demo screenshot or GIF (Windows)

This project includes a placeholder demo screenshot at `docs/demo_screenshot.svg`. To replace it with a real screenshot or a short GIF recorded from your machine, follow one of the methods below. After creating the file, name it `docs/demo_screenshot.png` (or `.gif`) and commit it — `README.md` already references `docs/demo_screenshot.svg`; you can replace the reference or overwrite the SVG filename.

Option A — Single screenshot (PNG) using built-in tools

1. Open PowerShell and run the demo to produce console output:

```powershell
python mini-deep-research-agent/src/main.py
```

2. Use the Windows Snipping Tool (Search → Snipping Tool) or press `Win+Shift+S` to capture a rectangular screenshot of the console output.

3. Save the captured image as `docs/demo_screenshot.png`.

4. Commit and push:

```powershell
git add docs/demo_screenshot.png
git commit -m "docs: add real demo screenshot"
git push origin main
```

Option B — Animated GIF (terminal recording) using ffmpeg (advanced)

1. Install `ffmpeg` (https://ffmpeg.org/download.html) and ensure it's on your PATH.
2. On Windows, you can record the terminal window using `ffmpeg` with a region capture. Example (PowerShell) — adjust `-offset_x`, `-offset_y`, `-video_size` to match your terminal window:

```powershell
ffmpeg -f gdigrab -framerate 15 -offset_x 100 -offset_y 100 -video_size 900x300 -i desktop -t 6 docs/demo_record.mp4
ffmpeg -i docs/demo_record.mp4 -vf "fps=15,scale=900:-1:flags=lanczos" -loop 0 docs/demo_screenshot.gif
```

3. Remove the intermediate MP4 if desired. Commit and push the GIF:

```powershell
git add docs/demo_screenshot.gif
git commit -m "docs: add demo GIF"
git push origin main
```

Option C — Use a GUI recorder (recommended for GIFs)

- Tools: ShareX (free), Peek (on Linux), ScreenToGif (Windows).
- Record the terminal area while running the demo, export as GIF, save to `docs/demo_screenshot.gif`, and commit.

Notes
- Keep the image reasonably small (e.g., max 800px width) so the README renders quickly.
- If you prefer, overwrite `docs/demo_screenshot.svg` with a PNG/GIF of the same name. The README will continue to reference `docs/demo_screenshot.svg` unless you update the path — make sure to update README if you use a different filename.

If you want, upload the PNG/GIF here (or tell me where to fetch it), and I will commit and replace the placeholder for you.
