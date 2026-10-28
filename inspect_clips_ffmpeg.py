import subprocess
import glob

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

files = [
    "assets/raw_footage/kane_bayern_goal.mp4",
    "assets/raw_footage/yamal_euro_goal.mp4",
    "assets/raw_footage/yamal_skills.mp4",
    "assets/raw_footage/mbappe_raw.mp4"
]

for f in files:
    cmd = [FFMPEG, "-i", f]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line or "Video:" in line:
            print(f, "->", line.strip())
