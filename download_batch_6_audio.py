import os
import subprocess

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
os.makedirs("assets/audio", exist_ok=True)

# 1. Download FE!N
print("Downloading FE!N...")
subprocess.run([
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:20-00:50",
    "-o", "assets/audio/fein_slowed.%(ext)s",
    "https://www.youtube.com/watch?v=8Ok8pJ-cFXo"
], stderr=subprocess.DEVNULL)

# 2. Download Stereo Love
print("Downloading Stereo Love...")
subprocess.run([
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:30-01:05",
    "-o", "assets/audio/stereo_love.%(ext)s",
    "https://www.youtube.com/watch?v=qw6ee8jIxxc"
], stderr=subprocess.DEVNULL)

# 3. Download Love Me Again
print("Downloading Love Me Again...")
subprocess.run([
    "python", "-m", "yt_dlp",
    "--ffmpeg-location", FFMPEG,
    "-x", "--audio-format", "mp3",
    "--download-sections", "*00:40-01:15",
    "-o", "assets/audio/love_me_again.%(ext)s",
    "https://www.youtube.com/watch?v=MmmRjwgVVOw"
], stderr=subprocess.DEVNULL)

print("Audio downloads complete!")
