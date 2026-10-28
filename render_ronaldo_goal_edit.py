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

print("🎨 Step 1: Generating Minimalist One-Line Hook Overlay...")
overlay_path = os.path.join(ASSETS_DIR, "ronaldo_hook_overlay.png")

img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font_main = ImageFont.truetype("arialbd.ttf", 44)
except Exception:
    font_main = ImageFont.load_default()

hook_line = "The greatest goal in Champions League history."

def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 255, 255, 255), shadow_color=(0, 0, 0, 240)):
    for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
        draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill_color)

l_bbox = draw.textbbox((0, 0), hook_line, font=font_main)
l_w = l_bbox[2] - l_bbox[0]
l_x = (1080 - l_w) // 2
l_y = 260

draw_text_with_shadow(draw, hook_line, l_x, l_y, font_main, fill_color=(255, 255, 255, 255))
img.save(overlay_path)
print(f"✅ Overlay created: {overlay_path}")

print("🎵 Step 2: Slicing Audio Track...")
cut_audio_path = os.path.join(ASSETS_DIR, "ronaldo_audio.mp3")
cmd_audio = [
    FFMPEG_PATH,
    "-ss", "10.0",
    "-t", "14.3",
    "-i", "assets/audio/fancy_footwork.mp3",
    "-af", "afade=t=out:st=13.3:d=1.0",
    "-y", cut_audio_path
]
subprocess.run(cmd_audio, check=True, stderr=subprocess.DEVNULL)
print("✅ Audio prepped.")

print("🎬 Step 3: Rendering Narrative Goal Segments...")
RAW_VIDEO = "assets/raw_footage/ronaldo_juve_goal.mp4"

# Segment 1: The Cross (0.0s to 3.81s) - 3.810s
# In raw: 0.0s to 2.4s. setpts = (3.81 / 2.4) = 1.5875
seg1_path = os.path.join(ASSETS_DIR, "ronaldo_seg1.mp4")
vf_seg1 = (
    "setpts=1.5875*PTS,"
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1080:-2[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.15:saturation=1.20"
)
cmd_seg1 = [
    FFMPEG_PATH,
    "-ss", "0.0",
    "-t", "2.4",
    "-i", RAW_VIDEO,
    "-vf", vf_seg1,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg1_path
]
subprocess.run(cmd_seg1, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 1 (The Cross) rendered.")

# Segment 2: Slow-Motion Mid-Air Rise (3.81s to 5.714s) - 1.904s
# In raw: 8.3s to 9.56s (1.26s). setpts = 1.904 / 1.26 = 1.5111
seg2_path = os.path.join(ASSETS_DIR, "ronaldo_seg2.mp4")
vf_seg2 = (
    "setpts=1.5111*PTS,"
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1150:-2[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.18:saturation=1.22"
)
cmd_seg2 = [
    FFMPEG_PATH,
    "-ss", "8.3",
    "-t", "1.26",
    "-i", RAW_VIDEO,
    "-vf", vf_seg2,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg2_path
]
subprocess.run(cmd_seg2, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 2 (The Mid-Air Rise) rendered.")

# Segment 3: THE DROP & BICYCLE STRIKE (5.714s to 7.619s) - 1.905s
# In raw: 9.56s to 10.35s (0.79s). setpts = 1.905 / 0.79 = 2.4114
# Punch-in zoom (scale=1260:-2) to maximize drop impact!
seg3_path = os.path.join(ASSETS_DIR, "ronaldo_seg3.mp4")
vf_seg3 = (
    "setpts=2.4114*PTS,"
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1260:-2[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.4:5:5:0.0,eq=contrast=1.22:saturation=1.25"
)
cmd_seg3 = [
    FFMPEG_PATH,
    "-ss", "9.56",
    "-t", "0.79",
    "-i", RAW_VIDEO,
    "-vf", vf_seg3,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg3_path
]
subprocess.run(cmd_seg3, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 3 (The Beat Drop Strike) rendered.")

# Segment 4: Zinedine Zidane Shock Reaction (7.619s to 9.524s) - 1.905s
# In raw: 10.8s to 12.705s (1.905s).
seg4_path = os.path.join(ASSETS_DIR, "ronaldo_seg4.mp4")
vf_seg4 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1120:-2[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.16:saturation=1.20"
)
cmd_seg4 = [
    FFMPEG_PATH,
    "-ss", "10.8",
    "-t", "1.905",
    "-i", RAW_VIDEO,
    "-vf", vf_seg4,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg4_path
]
subprocess.run(cmd_seg4, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 4 (Zidane Shock Reaction) rendered.")

# Segment 5: Gianluigi Buffon Defeat Reaction (9.524s to 11.429s) - 1.905s
# In raw: 15.2s to 17.105s (1.905s).
seg5_path = os.path.join(ASSETS_DIR, "ronaldo_seg5.mp4")
vf_seg5 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1100:-2[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.16:saturation=1.20"
)
cmd_seg5 = [
    FFMPEG_PATH,
    "-ss", "15.2",
    "-t", "1.905",
    "-i", RAW_VIDEO,
    "-vf", vf_seg5,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg5_path
]
subprocess.run(cmd_seg5, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 5 (Buffon Defeat Reaction) rendered.")

# Segment 6: Cristiano Ronaldo Standing Ovation Celebration (11.429s to 14.30s) - 2.871s
# In raw: 13.0s to 15.871s (2.871s).
seg6_path = os.path.join(ASSETS_DIR, "ronaldo_seg6.mp4")
vf_seg6 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1180:-2[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.18:saturation=1.22"
)
cmd_seg6 = [
    FFMPEG_PATH,
    "-ss", "13.0",
    "-t", "2.871",
    "-i", RAW_VIDEO,
    "-vf", vf_seg6,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg6_path
]
subprocess.run(cmd_seg6, check=True, stderr=subprocess.DEVNULL)
print("✅ Segment 6 (Ronaldo Standing Ovation) rendered.")

print("🔗 Step 4: Concatenating Segments...")
concat_list_path = os.path.join(ASSETS_DIR, "ronaldo_concat_list.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    for seg in [seg1_path, seg2_path, seg3_path, seg4_path, seg5_path, seg6_path]:
        f.write(f"file '{os.path.abspath(seg)}'\n")

video_raw_path = os.path.join(ASSETS_DIR, "ronaldo_raw_concatenated.mp4")
cmd_concat = [
    FFMPEG_PATH,
    "-f", "concat",
    "-safe", "0",
    "-i", concat_list_path,
    "-c", "copy",
    "-y", video_raw_path
]
subprocess.run(cmd_concat, check=True, stderr=subprocess.DEVNULL)
print("✅ Video stream concatenated.")

print("🚀 Step 5: Final Mastering with Text Hook & Audio...")
final_output = os.path.join(EXPORTS_DIR, "Fancy_Footwork_Ronaldo_UCL_Goal.mp4")

cmd_final = [
    FFMPEG_PATH,
    "-i", video_raw_path,
    "-i", cut_audio_path,
    "-i", overlay_path,
    "-filter_complex", "[0:v][2:v]overlay=0:0[v_out]",
    "-map", "[v_out]",
    "-map", "1:a",
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-y", final_output
]
subprocess.run(cmd_final, check=True, stderr=subprocess.DEVNULL)

size_mb = os.path.getsize(final_output) / (1024 * 1024)
print(f"🎉 MASTER EXPORT COMPLETE: {final_output} ({size_mb:.2f} MB)")
