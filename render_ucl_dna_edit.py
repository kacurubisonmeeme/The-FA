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
overlay_path = os.path.join(ASSETS, "ucl_dna_hook.png")
img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arialbd.ttf", 50)
except Exception:
    font = ImageFont.load_default()

hook = "Champions League DNA."

def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 255, 255, 255), shadow_color=(0, 0, 0, 240)):
    for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
        draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill_color)

bbox = draw.textbbox((0, 0), hook, font=font)
w = bbox[2] - bbox[0]
draw_text_with_shadow(draw, hook, (1080 - w) // 2, 260, font)
img.save(overlay_path)
print("✅ Hook overlay created.")

print("⚡ Step 2: One-Pass Ultra-Fast FFmpeg Render...")
final_output = os.path.join(EXPORTS, "Fancy_Footwork_UCL_DNA_Vini.mp4")
raw_vini = "assets/raw_footage/vini_dortmund.mp4"
audio_src = "assets/ronaldo_audio.mp3"

# Cut points in raw_vini (1080p 50fps twixtor):
# Segment 1: 0.0s to 3.81s (3.81s) -> Wembley knee slide badge kiss (46.2s to 50.01s)
# Segment 2: 3.81s to 5.714s (1.904s) -> Vocal riser chest flex & roar (54.5s to 56.404s)
# Segment 3: 5.714s to 8.571s (2.857s) -> Beat drop piggyback pandemonium (64.5s to 67.357s)
# Segment 4: 8.571s to 14.286s (5.715s) -> Beat-pulsed corner celebration & dance (82.5s to 88.215s)

filter_complex = (
    "[0:v]trim=start=46.2:end=50.01,setpts=PTS-STARTPTS[c1];"
    "[0:v]trim=start=54.5:end=56.404,setpts=PTS-STARTPTS[c2];"
    "[0:v]trim=start=64.5:end=67.357,setpts=PTS-STARTPTS[c3];"
    "[0:v]trim=start=82.5:end=88.215,setpts=PTS-STARTPTS[c4];"
    "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
    "[v_cat]split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
    "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
    "[v_base][2:v]overlay=0:0[v_final]"
)

cmd = [
    FFMPEG,
    "-i", raw_vini,
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

res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
if res.returncode != 0:
    print("Error:", res.stderr[-500:])
    sys.exit(1)

size_mb = os.path.getsize(final_output) / (1024 * 1024)
print(f"🚀 MASTER EXPORT COMPLETE: {final_output} ({size_mb:.2f} MB)")
