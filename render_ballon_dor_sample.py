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

# 1. Prepare Audio
print("🎵 Preparing Ballon d'Or Audio (After Dark Slowed)...")
audio_cut = os.path.join(ASSETS, "ballon_dor_after_dark_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "10.0", "-t", "14.5", "-i", "assets/audio/after_dark.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Audio cut prepared.")

# 2. Create Typography Hook
def create_ballon_dor_hook(filename):
    path = os.path.join(ASSETS, filename)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 54)
        font_sub = ImageFont.truetype("arialbd.ttf", 38)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 215, 0, 255), shadow_color=(0, 0, 0, 240)):
        for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
            draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # Title 1: Gold
    t1 = "WHY HE WON IT 🏆"
    bbox1 = draw.textbbox((0, 0), t1, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    draw_text_with_shadow(draw, t1, (1080 - w1) // 2, 240, font_main, fill_color=(255, 220, 80, 255))

    # Title 2: White
    t2 = "RODRI x VINI JR: THE TRUTH"
    bbox2 = draw.textbbox((0, 0), t2, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    draw_text_with_shadow(draw, t2, (1080 - w2) // 2, 315, font_sub, fill_color=(255, 255, 255, 255))

    img.save(path)
    return path

hook_overlay = create_ballon_dor_hook("ballon_dor_sample_hook.png")

# 3. Filter Complex for 4-Part Edit
output_video = os.path.join(EXPORTS, "Ballon_dOr_2024_Rodri_vs_Vini_The_Story.mp4")

# Inputs:
# 0: rodri_ucl_final_goal.mp4
# 1: vini_goal_vs_bayern.mp4
# 2: vini_dortmund.mp4
# 3: audio_cut
# 4: hook_overlay

filter_complex = (
    "[0:v]trim=start=4.0:end=8.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
    "[0:v]trim=start=10.5:end=14.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
    "[1:v]trim=start=3.0:end=6.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
    "[2:v]trim=start=82.5:end=85.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
    "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
    "[v_cat]split[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
    "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
    "[v_base][4:v]overlay=0:0[v_final]"
)

cmd = [
    FFMPEG,
    "-i", "assets/raw_footage/rodri_ucl_final_goal.mp4",
    "-i", "assets/raw_footage/vini_goal_vs_bayern.mp4",
    "-i", "assets/raw_footage/vini_dortmund.mp4",
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

print("🚀 Rendering Ballon d'Or Master Sample Video...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    size = os.path.getsize(output_video) / (1024 * 1024)
    print(f"✅ SUCCESS: {output_video} exported ({size:.2f} MB)")
else:
    print("❌ ERROR rendering video:")
    print(res.stderr[-500:])
