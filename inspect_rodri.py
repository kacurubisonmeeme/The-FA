import subprocess

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

cmd = [FFMPEG, "-i", "assets/raw_footage/rodri_ucl_final_goal.mp4"]
res = subprocess.run(cmd, capture_output=True, text=True)
for line in res.stderr.splitlines():
    if "Duration:" in line or "Video:" in line:
        print(line.strip())
