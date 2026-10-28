import os
import glob
import subprocess
import sys

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

# Clean up Kane part files
for p in glob.glob("assets/raw_footage/*kane*part*"):
    try:
        os.remove(p)
        print("Removed partial:", p)
    except Exception:
        pass

out_path = os.path.join("assets", "raw_footage", "kane_bayern_goal.mp4")

cmd = [
    sys.executable, "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
    "--download-sections", "*00:00-00:35",
    "--force-keyframes-at-cuts",
    "-o", out_path,
    "ytsearch1:Harry Kane Bayern Munich 4k clips short"
]

print("Downloading Kane clip...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print("Success Kane downloaded!")
else:
    print("Error:", res.stderr[:300])
