import subprocess

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

# Extract 4 sample thumbnails to check scenes: 2s, 8s, 15s, 22s
for sec in [3, 8, 14, 20]:
    subprocess.run([
        FFMPEG, "-ss", str(sec), "-i", "assets/raw_footage/rodri_ucl_final_goal.mp4",
        "-vframes", "1", "-q:v", "2", "-y", f"assets/rodri_{sec}s.jpg"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Extracted test frames.")
