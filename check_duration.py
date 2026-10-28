import subprocess
import json

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
FFPROBE = FFMPEG.replace("ffmpeg-win", "ffprobe-win")

cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "assets/raw_footage/mbappe_raw.mp4"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Mbappe Raw Duration:", res.stdout.strip())
