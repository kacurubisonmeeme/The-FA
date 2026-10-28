import os
import subprocess

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
os.makedirs("assets/audio", exist_ok=True)
os.makedirs("assets/raw_footage", exist_ok=True)

# 1. Download Memory Reboot (Ultra slowed)
print("Downloading Memory Reboot...")
cmd_audio1 = [
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:20-00:50",
    "-o", "assets/audio/memory_reboot.%(ext)s",
    "https://www.youtube.com/watch?v=r_wjTjwyY6o"
]
subprocess.run(cmd_audio1, stderr=subprocess.DEVNULL)

# 2. Download Montagem Diamante (Brazilian Phonk)
print("Downloading Montagem Diamante...")
cmd_audio2 = [
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:15-00:45",
    "-o", "assets/audio/montagem_diamante.%(ext)s",
    "https://www.youtube.com/watch?v=03pkdhqOEdY"
]
subprocess.run(cmd_audio2, stderr=subprocess.DEVNULL)

# 3. Download Messi 4k Fresh Clips
print("Downloading Messi 4k clips...")
cmd_messi = [
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "--download-sections", "*00:00-00:40",
    "-o", "assets/raw_footage/messi_fresh.mp4",
    "https://www.youtube.com/watch?v=HM7AhxcQwpA"
]
subprocess.run(cmd_messi, stderr=subprocess.DEVNULL)

# 4. Download Neymar 4k Fresh Clips
print("Downloading Neymar 4k clips...")
cmd_neymar = [
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "--download-sections", "*00:00-00:40",
    "-o", "assets/raw_footage/neymar_fresh.mp4",
    "https://www.youtube.com/watch?v=zSPkdQZiR5U"
]
subprocess.run(cmd_neymar, stderr=subprocess.DEVNULL)

# 5. Download Ronaldo Siuuu
print("Downloading Ronaldo Siuuu...")
cmd_ronaldo = [
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "--download-sections", "*00:00-00:25",
    "-o", "assets/raw_footage/ronaldo_siuuu.mp4",
    "https://www.youtube.com/watch?v=6rIHOdckoQw"
]
subprocess.run(cmd_ronaldo, stderr=subprocess.DEVNULL)

print("✅ ALL FRESH ASSETS DOWNLOADED!")
