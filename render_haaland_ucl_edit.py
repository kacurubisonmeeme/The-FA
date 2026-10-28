import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

FFMPEG = r"C:\Users\SmartKid\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
EXPORTS = "exports"
ASSETS = "assets"
os.makedirs(EXPORTS, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

print("⚡ Step 1: Creating Minimalist Hook Overlay...")
overlay_path = os.path.join(ASSETS, "haaland_hook.png")
img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arialbd.ttf", 52)
except Exception:
    font = ImageFont.load_default()

hook = "The Champions League cheat code."

def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 255, 255, 255), shadow_color=(0, 0, 0, 240)):
    for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
        draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill_color)

bbox = draw.textbbox((0, 0), hook, font=font)
w = bbox[2] - bbox[0]
draw_text_with_shadow(draw, hook, (1080 - w) // 2, 260, font)
img.save(overlay_path)
print("✅ Hook overlay created.")

print("⚡ Step 2: One-Pass Ultra-Fast FFmpeg Render for Haaland UCL...")
final_output = os.path.join(EXPORTS, "Fancy_Footwork_Haaland_UCL.mp4")
raw_video = "assets/raw_footage/haaland_ucl.mp4"
audio_src = "assets/ronaldo_audio.mp3"

# Cut points:
# Segment 1: 0.0s to 3.810s (3.810s) -> Goal finish & explosive sprint (25.5s to 29.31s)
# Segment 2: 3.810s to 5.714s (1.904s) -> Vocal riser jump in air (32.8s to 34.704s)
# Segment 3: 5.714s to 8.571s (2.857s) -> Beat drop hit: iconic finger-to-ear celebration (34.704s to 37.561s)
# Segment 4: 8.571s to 14.286s (5.715s) -> Slow-mo floodlight celebration continuation (35.0s to 38.5s stretched)

filter_complex = (
    "[0:v]trim=start=25.5:end=29.31,setpts=PTS-STARTPTS[c1];"
    "[0:v]trim=start=32.8:end=34.704,setpts=PTS-STARTPTS[c2];"
    "[0:v]trim=start=34.704:end=37.561,setpts=PTS-STARTPTS[c3];"
    "[0:v]trim=start=35.0:end=38.5,setpts=1.632857*(PTS-STARTPTS)[c4];"
    "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
    "[v_cat]split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
    "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
    "[v_base][2:v]overlay=0:0[v_final]"
)

cmd = [
    FFMPEG,
    "-i", raw_video,
    "-i", audio_src,
    "-i", overlay_path,
    "-filter_complex", filter_complex,
    "-map", "[v_final]",
    "-map", "1:a",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    "-r", "60",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-y", final_output
]

print("Rendering video...")
res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
if res.returncode != 0:
    print("Error:", res.stderr[-500:])
    sys.exit(1)

size_mb = os.path.getsize(final_output) / (1024 * 1024)
print(f"🚀 MASTER EXPORT COMPLETE: {final_output} ({size_mb:.2f} MB)")
