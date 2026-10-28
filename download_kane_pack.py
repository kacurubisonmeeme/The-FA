import os
import subprocess
import sys

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

targets = [
    {
        "name": "kane_england_goals.mp4",
        "query": "ytsearch1:Harry Kane England goals 4k clips short",
        "sections": "*00:00-00:35"
    },
    {
        "name": "kane_screamer.mp4",
        "query": "ytsearch1:Harry Kane long range goals bayern 4k short",
        "sections": "*00:00-00:35"
    }
]

for t in targets:
    out_path = os.path.join("assets", "raw_footage", t["name"])
    if os.path.exists(out_path) and os.path.getsize(out_path) > 500000:
        print(f"Skipping {t['name']}, already exists.")
        continue
    
    print(f"Downloading {t['name']}...")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--ffmpeg-location", FFMPEG,
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
        "--download-sections", t["sections"],
        "--force-keyframes-at-cuts",
        "-o", out_path,
        t["query"]
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Successfully saved {t['name']}")
    else:
        print(f"Failed {t['name']}: {res.stderr[:200]}")
