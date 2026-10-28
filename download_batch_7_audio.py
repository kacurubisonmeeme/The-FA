import os
import subprocess

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
os.makedirs("assets/audio", exist_ok=True)

# 1. Download After Dark
print("Downloading After Dark...")
subprocess.run([
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:25-01:00",
    "-o", "assets/audio/after_dark.%(ext)s",
    "https://www.youtube.com/watch?v=nXOyLFTy6eU"
], stderr=subprocess.DEVNULL)

# 2. Download Viva La Vida
print("Downloading Viva La Vida...")
subprocess.run([
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:30-01:05",
    "-o", "assets/audio/viva_la_vida.%(ext)s",
    "https://www.youtube.com/watch?v=jqGg3sJFbKo"
], stderr=subprocess.DEVNULL)

# 3. Download Bibi Fogosa
print("Downloading Bibi Fogosa...")
subprocess.run([
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:15-00:50",
    "-o", "assets/audio/bibi_fogosa.%(ext)s",
    "https://www.youtube.com/watch?v=A7Oe7HI9Ovc"
], stderr=subprocess.DEVNULL)

print("Batch 7 audio downloads complete!")
