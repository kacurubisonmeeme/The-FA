import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

FFMPEG_PATH = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
EXPORTS_DIR = "exports"
ASSETS_DIR = "assets"
os.makedirs(EXPORTS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

print("🎨 Step 1: Generating Minimalist One-Line Text Hook...")
overlay_path = os.path.join(ASSETS_DIR, "vini_single_line_overlay.png")

# Create 1080x1920 RGBA transparent canvas
img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Load bold font
try:
    font_main = ImageFont.truetype("arialbd.ttf", 46)
except Exception:
    font_main = ImageFont.load_default()

# Exactly ONE clean aesthetic line
hook_line = "Vini Jr in the Champions League is poetry."

def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 255, 255, 255), shadow_color=(0, 0, 0, 240)):
    for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
        draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill_color)

l_bbox = draw.textbbox((0, 0), hook_line, font=font_main)
l_w = l_bbox[2] - l_bbox[0]
l_x = (1080 - l_w) // 2
l_y = 260 # Clean upper third placement

draw_text_with_shadow(draw, hook_line, l_x, l_y, font_main, fill_color=(255, 255, 255, 255))

img.save(overlay_path)
print(f"✅ One-line overlay created: {overlay_path}")

print("🎵 Step 2: Preparing Audio (Fancy Footwork drop)...")
# Trim 14.5s (from 10.0s to 24.5s)
cut_audio_path = os.path.join(ASSETS_DIR, "vini_audio.mp3")
cmd_audio = [
    FFMPEG_PATH,
    "-ss", "10.0",
    "-t", "14.5",
    "-i", "assets/audio/fancy_footwork.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0",
    "-y", cut_audio_path
]
subprocess.run(cmd_audio, check=True, stderr=subprocess.DEVNULL)
print("✅ Audio prepped.")

print("🎬 Step 3: Editing Single Goal & Celebration (Vini Jr UCL Final)...")

# Part 1: Goal Knee Slide Celebration (0.0s to 4.8s - Build-up)
# In vini_dortmund.mp4, from 28.0s to 32.8s
seg1_path = os.path.join(ASSETS_DIR, "vini_seg1.mp4")
vf_seg1 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1080:-1[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.16:saturation=1.22:brightness=0.01"
)
cmd_seg1 = [
    FFMPEG_PATH,
    "-ss", "28.0",
    "-t", "4.8",
    "-i", "assets/raw_footage/vini_dortmund.mp4",
    "-vf", vf_seg1,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg1_path
]
subprocess.run(cmd_seg1, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 1 (Goal Knee Slide) rendered.")

# Part 2: The Fancy Footwork Dance Celebration (4.8s to 14.5s - The Drop!)
# In vini_dortmund.mp4, from 83.2s to 92.9s (9.7s duration)
seg2_path = os.path.join(ASSETS_DIR, "vini_seg2.mp4")
vf_seg2 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1080:-1[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.16:saturation=1.25:brightness=0.01"
)
cmd_seg2 = [
    FFMPEG_PATH,
    "-ss", "83.2",
    "-t", "9.7",
    "-i", "assets/raw_footage/vini_dortmund.mp4",
    "-vf", vf_seg2,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg2_path
]
subprocess.run(cmd_seg2, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 2 (Corner Dance Footwork) rendered.")

print("🚀 Step 4: Concatenating and Finalizing 60FPS Video Edit...")
concat_list_path = os.path.join(ASSETS_DIR, "concat_vini.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    f.write(f"file '{os.path.abspath(seg1_path)}'\n")
    f.write(f"file '{os.path.abspath(seg2_path)}'\n")

final_output = os.path.join(EXPORTS_DIR, "Fancy_Footwork_Vini_UCL_Final.mp4")

cmd_final = [
    FFMPEG_PATH,
    "-f", "concat",
    "-safe", "0",
    "-i", concat_list_path,
    "-i", overlay_path,
    "-i", cut_audio_path,
    "-filter_complex", "[0:v][1:v]overlay=0:0[v_out]",
    "-map", "[v_out]",
    "-map", "2:a",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "17",
    "-c:a", "aac",
    "-b:a", "256k",
    "-shortest",
    "-y", final_output
]

subprocess.run(cmd_final, check=True)

# Generate preview frames
prev_dir = os.path.join(EXPORTS_DIR, "preview")
subprocess.run([FFMPEG_PATH, "-ss", "3.0", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "vini_solo_slide.jpg"), "-y"], stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG_PATH, "-ss", "8.0", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "vini_solo_dance.jpg"), "-y"], stderr=subprocess.DEVNULL)

size_mb = os.path.getsize(final_output) / (1024 * 1024)
print(f"\n🎉 VINI JR SOLO EDIT READY: {final_output}")
print(f"📊 Size: {size_mb:.2f} MB | 1080x1920 | 60 FPS | Length: 14.5s")
