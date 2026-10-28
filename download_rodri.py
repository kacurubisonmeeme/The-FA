import subprocess
import os
import sys

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

out_path = os.path.join("assets", "raw_footage", "rodri_ucl_final_goal.mp4")

cmd = [
    sys.executable, "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
    "--download-sections", "*00:00-00:35",
    "--force-keyframes-at-cuts",
    "-o", out_path,
    "ytsearch1:Rodri goal vs Inter Milan Champions League final 4k short"
]

print("Downloading Rodri UCL Final Goal...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print("Success Rodri downloaded!")
else:
    print("Error:", res.stderr[:300])
