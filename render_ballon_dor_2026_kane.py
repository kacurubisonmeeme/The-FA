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

# 1. Prepare Audio (Viva La Vida - Orchestral Coronation)
print("🎵 Preparing 2026 Coronation Audio...")
audio_cut = os.path.join(ASSETS, "viva_kane_2026_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "0.2", "-t", "15.0", "-i", "assets/audio/viva_la_vida.mp3",
    "-af", "afade=t=out:st=14.0:d=1.0", "-y", audio_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Audio prepared.")

# 2. Typography Hook Overlay
def create_2026_hook(filename):
    path = os.path.join(ASSETS, filename)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 54)
        font_sub = ImageFont.truetype("arialbd.ttf", 36)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 215, 0, 255), shadow_color=(0, 0, 0, 240)):
        for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
            draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # Title 1: Gold
    t1 = "BALLON D'OR 2026 🏆"
    bbox1 = draw.textbbox((0, 0), t1, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    draw_text_with_shadow(draw, t1, (1080 - w1) // 2, 230, font_main, fill_color=(255, 220, 80, 255))

    # Title 2: White
    t2 = "HARRY KANE: CROWNED KING OF FOOTBALL"
    bbox2 = draw.textbbox((0, 0), t2, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    draw_text_with_shadow(draw, t2, (1080 - w2) // 2, 305, font_sub, fill_color=(255, 255, 255, 255))

    img.save(path)
    return path

hook_overlay = create_2026_hook("kane_2026_hook.png")

# 3. Filter Complex for 2026 Coronation Video
output_video = os.path.join(EXPORTS, "Ballon_dOr_2026_Harry_Kane_Crowned_King.mp4")

# Inputs:
# 0: kane_bayern_goal.mp4
# 1: mbappe_raw.mp4
# 2: yamal_euro_goal.mp4
# 3: audio_cut
# 4: hook_overlay

filter_complex = (
    # Kane: 60-Goal Season clinical strike (0.0s - 4.5s)
    "[0:v]trim=start=4.5:end=9.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
    # Kane: The Iconic Jump-Punch & Broken Curse (4.5s - 8.5s)
    "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
    # Mbappé: 2nd Place Runner-Up Pace & Folded Arms (8.5s - 11.5s)
    "[1:v]trim=start=16.5:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
    # Yamal: 3rd Place Wonderkid at 19 Curler & 304 (11.5s - 15.0s)
    "[2:v]trim=start=3.5:end=7.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
    "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
    "[v_cat]split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
    "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.26[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
    "[v_base][4:v]overlay=0:0[v_final]"
)

cmd = [
    FFMPEG,
    "-i", "assets/raw_footage/kane_bayern_goal.mp4",
    "-i", "assets/raw_footage/mbappe_raw.mp4",
    "-i", "assets/raw_footage/yamal_euro_goal.mp4",
    "-i", audio_cut,
    "-i", hook_overlay,
    "-filter_complex", filter_complex,
    "-map", "[v_final]",
    "-map", "3:a",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-y", output_video
]

print("🚀 Rendering Ballon d'Or 2026 Master Coronation Video...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    size = os.path.getsize(output_video) / (1024 * 1024)
    print(f"✅ SUCCESS: {output_video} exported ({size:.2f} MB)")
else:
    print("❌ ERROR rendering video:")
    print(res.stderr[-500:])
