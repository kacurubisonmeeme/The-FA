import os
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

FFMPEG_PATH = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
CLIPS_DIR = "assets/raw_footage"
os.makedirs(CLIPS_DIR, exist_ok=True)

TARGETS = [
    {"name": "vini_chelsea", "id": "yZE2_c3I724"},
    {"name": "ronaldinho_samba", "id": "kux97XJDoI4"},
    {"name": "bellingham_arms", "id": "t-yHv05I56k"}
]

print("Sourcing 4K/1080p Scenepacks...")

for target in TARGETS:
    out_path = os.path.join(CLIPS_DIR, f"{target['name']}.mp4")
    if os.path.exists(out_path):
        print(f"Already exists: {out_path}")
        continue
    
    url = f"https://www.youtube.com/watch?v={target['id']}"
    print(f"Downloading {target['name']} from {url}...")
    cmd = [
        "python", "-m", "yt_dlp",
        url,
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
        "--merge-output-format", "mp4",
        "--ffmpeg-location", FFMPEG_PATH,
        "-o", out_path,
        "--quiet",
        "--no-playlist"
    ]
    subprocess.run(cmd, check=True)
    print(f"Downloaded: {out_path} ({os.path.getsize(out_path)} bytes)")

print("All raw scenepack clips downloaded successfully!")
