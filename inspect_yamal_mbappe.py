import subprocess
import glob

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
FFPROBE = FFMPEG.replace("ffmpeg-win", "ffprobe-win")

for f in ["assets/raw_footage/yamal_euro_goal.mp4", "assets/raw_footage/yamal_skills.mp4", "assets/raw_footage/mbappe_raw.mp4"]:
    cmd = [FFPROBE, "-v", "error", "-show_entries", "stream=width,height,r_frame_rate,duration", "-of", "csv=p=0", f]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f, res.stdout.strip())
