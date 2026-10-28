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

print("🎨 Step 1: Generating Ultra-Clean Text Overlay...")
overlay_path = os.path.join(ASSETS_DIR, "text_overlay.png")

# Create 1080x1920 RGBA transparent canvas
img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Try loading standard bold fonts
try:
    font_badge = ImageFont.truetype("arialbd.ttf", 36)
    font_main = ImageFont.truetype("arialbd.ttf", 52)
    font_sub = ImageFont.truetype("arialbd.ttf", 38)
except Exception:
    font_badge = ImageFont.load_default()
    font_main = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# 1. Badge Pill (Top)
badge_text = "UEFA CHAMPIONS LEAGUE"
badge_bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
badge_w = badge_bbox[2] - badge_bbox[0] + 50
badge_x = (1080 - badge_w) // 2
badge_y = 210

# Draw Badge Background Pill
draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + 55], radius=25, fill=(10, 25, 75, 230), outline=(0, 200, 255, 255), width=3)
draw.text((badge_x + 25, badge_y + 7), badge_text, font=font_badge, fill=(255, 255, 255, 255))

# 2. Main Viral Hook
line1 = "ICONIC UCL CELEBRATIONS"
line2 = "WHEN THE FOOTWORK IS TOO FANCY"

def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 255, 255, 255), shadow_color=(0, 0, 0, 240)):
    for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4)]:
        draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill_color)

l1_bbox = draw.textbbox((0, 0), line1, font=font_main)
l1_x = (1080 - (l1_bbox[2] - l1_bbox[0])) // 2
draw_text_with_shadow(draw, line1, l1_x, 285, font_main)

l2_bbox = draw.textbbox((0, 0), line2, font=font_main)
l2_x = (1080 - (l2_bbox[2] - l2_bbox[0])) // 2
draw_text_with_shadow(draw, line2, l2_x, 350, font_main, fill_color=(255, 220, 50, 255))

# 3. Call to Action / Bottom Text
cta_text = "WHO HAD THE COLDEST CELEBRATION?"
cta_bbox = draw.textbbox((0, 0), cta_text, font=font_sub)
cta_x = (1080 - (cta_bbox[2] - cta_bbox[0])) // 2
draw_text_with_shadow(draw, cta_text, cta_x, 1580, font_sub)

img.save(overlay_path)
print(f"✅ Text hook overlay created: {overlay_path}")

print("🎵 Step 2: Preparing Beat-Synced Audio (Fancy Footwork)...")
# Extract 14.5s clip (from 10.0s to 24.5s)
cut_audio_path = os.path.join(ASSETS_DIR, "cut_audio.mp3")
cmd_audio = [
    FFMPEG_PATH,
    "-ss", "10.0",
    "-t", "14.5",
    "-i", "assets/audio/fancy_footwork.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0",
    "-y", cut_audio_path
]
subprocess.run(cmd_audio, check=True, stderr=subprocess.DEVNULL)
print(f"✅ Beat-synced audio trimmed: {cut_audio_path}")

print("🎬 Step 3: Formatting & Beat-Cutting Video Clips with Verified Timestamps...")

# Segment 1: Bellingham Open Arms (0.0 to 4.8s - Vocal Build-up)
# Starts at 17.5s in bellingham_arms.mp4
seg1_path = os.path.join(ASSETS_DIR, "seg1.mp4")
vf_seg1 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
    "[fg]scale=1080:-1[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.12:saturation=1.18"
)
cmd_seg1 = [
    FFMPEG_PATH,
    "-ss", "17.5",
    "-t", "4.8",
    "-i", "assets/raw_footage/bellingham_arms.mp4",
    "-vf", vf_seg1,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg1_path
]
subprocess.run(cmd_seg1, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 1 (Bellingham Iconic Open Arms) rendered.")

# Segment 2: Ronaldinho Samba Celebration (4.8s to 9.6s - Drop Part 1)
# Starts at 18.5s in ronaldinho_samba.mp4
seg2_path = os.path.join(ASSETS_DIR, "seg2.mp4")
vf_seg2 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
    "[fg]scale=1080:-1[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.15:saturation=1.20"
)
cmd_seg2 = [
    FFMPEG_PATH,
    "-ss", "18.5",
    "-t", "4.85",
    "-i", "assets/raw_footage/ronaldinho_samba.mp4",
    "-vf", vf_seg2,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg2_path
]
subprocess.run(cmd_seg2, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 2 (Ronaldinho Iconic Celebration) rendered.")

# Segment 3: Vini Jr Dance (9.65s to 14.5s - Drop Part 2)
# Starts at 0.0s in vini_chelsea.mp4
seg3_path = os.path.join(ASSETS_DIR, "seg3.mp4")
vf_seg3 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
    "[fg]scale=1080:-1[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.12:saturation=1.18"
)
cmd_seg3 = [
    FFMPEG_PATH,
    "-ss", "0.0",
    "-t", "4.85",
    "-i", "assets/raw_footage/vini_chelsea.mp4",
    "-vf", vf_seg3,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg3_path
]
subprocess.run(cmd_seg3, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 3 (Vini Jr Dance Celebration) rendered.")

print("🚀 Step 4: Concatenating Segments and Layering Overlay + Audio...")
concat_list_path = os.path.join(ASSETS_DIR, "concat.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    f.write(f"file '{os.path.abspath(seg1_path)}'\n")
    f.write(f"file '{os.path.abspath(seg2_path)}'\n")
    f.write(f"file '{os.path.abspath(seg3_path)}'\n")

final_output = os.path.join(EXPORTS_DIR, "Fancy_Footwork_UCL_Edit_01.mp4")

# Concatenate, overlay branding/hook, and attach the beat-synced audio
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
    "-crf", "18",
    "-c:a", "aac",
    "-b:a", "256k",
    "-shortest",
    "-y", final_output
]

subprocess.run(cmd_final, check=True)

# Generate updated preview frames
prev_dir = os.path.join(EXPORTS_DIR, "preview")
os.makedirs(prev_dir, exist_ok=True)
subprocess.run([FFMPEG_PATH, "-ss", "2.5", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "frame_bellingham.jpg"), "-y"], stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG_PATH, "-ss", "7.0", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "frame_ronaldinho.jpg"), "-y"], stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG_PATH, "-ss", "12.0", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "frame_vini.jpg"), "-y"], stderr=subprocess.DEVNULL)

file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
print(f"\n🎉 MASTER EDIT READY: {final_output}")
print(f"📊 Size: {file_size_mb:.2f} MB | Resolution: 1080x1920 | 60 FPS | Length: 14.5s")
