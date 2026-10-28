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

print("🎨 Step 1: Generating Minimalist Beat-Locked One-Line Hook...")
overlay_path = os.path.join(ASSETS_DIR, "pace_hook_overlay.png")

img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font_main = ImageFont.truetype("arialbd.ttf", 46)
except Exception:
    font_main = ImageFont.load_default()

hook_line = "When the footwork matches the beat."

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
cut_audio_path = os.path.join(ASSETS_DIR, "pace_audio.mp3")
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

print("🎬 Step 3: Generating Beat-Matched Video Segments with Dynamic Pace...")

# Part 1: Slow-Mo Tension Build-up (0.0s to 4.76s)
# 4.76s is exactly 10 beats at 126 BPM!
# In vini_dortmund.mp4, from 28.5s to 33.26s
seg1_path = os.path.join(ASSETS_DIR, "pace_seg1.mp4")
vf_seg1 = (
    "split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
    "[fg]scale=1080:-2[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.3:5:5:0.0,eq=contrast=1.15:saturation=1.20"
)
cmd_seg1 = [
    FFMPEG_PATH,
    "-ss", "28.5",
    "-t", "4.76",
    "-i", "assets/raw_footage/vini_dortmund.mp4",
    "-vf", vf_seg1,
    "-r", "60",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-an",
    "-y", seg1_path
]
subprocess.run(cmd_seg1, check=True, stderr=subprocess.DEVNULL)
print("✅ Part 1 (Tension Build-up) rendered.")

# Part 2: The Beat Drop - 126 BPM Rhythm Sync (4.76s to 14.5s = 9.74s)
# At 126 BPM, 1 bar (2 beats) = 0.952 seconds.
# We alternate between a punch-in zoom (scale=1300:-2) and regular scale (scale=1080:-2) on every 2 beats!
dance_clips = []
src_time = 83.5
bar_dur = 0.952

for bar_idx in range(10): # 10 bars = 9.52 seconds
    is_zoom = (bar_idx % 2 == 0)
    bar_path = os.path.join(ASSETS_DIR, f"bar_{bar_idx}.mp4")
    
    fg_scale = "scale=1300:-2" if is_zoom else "scale=1080:-2"
    contrast_val = "1.20" if is_zoom else "1.16"
        
    vf_bar = (
        "split[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.22[bg_blur];"
        f"[fg]{fg_scale}[fg_scaled];"
        f"[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2,unsharp=5:5:1.4:5:5:0.0,eq=contrast={contrast_val}:saturation=1.25"
    )
    
    cmd_bar = [
        FFMPEG_PATH,
        "-ss", str(src_time + (bar_idx * bar_dur)),
        "-t", str(bar_dur),
        "-i", "assets/raw_footage/vini_dortmund.mp4",
        "-vf", vf_bar,
        "-r", "60",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-an",
        "-y", bar_path
    ]
    subprocess.run(cmd_bar, check=True)
    dance_clips.append(bar_path)

print(f"✅ Rendered {len(dance_clips)} beat-pulsed bars matching 126 BPM!")

print("🚀 Step 4: Concatenating and Finalizing Master Edit...")
concat_list_path = os.path.join(ASSETS_DIR, "concat_pace.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    f.write(f"file '{os.path.abspath(seg1_path)}'\n")
    for b_path in dance_clips:
        f.write(f"file '{os.path.abspath(b_path)}'\n")

final_output = os.path.join(EXPORTS_DIR, "Fancy_Footwork_Beat_Paced_Vini.mp4")

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
subprocess.run([FFMPEG_PATH, "-ss", "3.0", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "pace_buildup.jpg"), "-y"], stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG_PATH, "-ss", "5.2", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "pace_drop_hit.jpg"), "-y"], stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG_PATH, "-ss", "8.0", "-i", final_output, "-vframes", "1", os.path.join(prev_dir, "pace_beat_pulse.jpg"), "-y"], stderr=subprocess.DEVNULL)

size_mb = os.path.getsize(final_output) / (1024 * 1024)
print(f"\n🎉 BEAT-PACED MASTER EDIT READY: {final_output}")
print(f"📊 Size: {size_mb:.2f} MB | 1080x1920 | 60 FPS | Length: 14.3s")
