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

# 1. Prepare Cut Audios
print("🎵 Trimming Batch 6 Trending Audio Tracks...")
fein_cut = os.path.join(ASSETS, "fein_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "14.0", "-t", "14.5", "-i", "assets/audio/fein_slowed.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", fein_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

stereo_cut = os.path.join(ASSETS, "stereo_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "14.5", "-t", "14.5", "-i", "assets/audio/stereo_love.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", stereo_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

love_cut = os.path.join(ASSETS, "love_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "13.5", "-t", "14.5", "-i", "assets/audio/love_me_again.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", love_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Batch 6 Audio tracks trimmed.")

def create_hook_overlay(filename, hook_text, font_size=52):
    path = os.path.join(ASSETS, filename)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
    
    def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 255, 255, 255), shadow_color=(0, 0, 0, 240)):
        for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
            draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=fill_color)
    
    bbox = draw.textbbox((0, 0), hook_text, font=font)
    w = bbox[2] - bbox[0]
    draw_text_with_shadow(draw, hook_text, (1080 - w) // 2, 260, font)
    img.save(path)
    return path

VIDEOS = [
    {
        "name": "FEIN_Haaland_Bellingham_Titans.mp4",
        "hook": "The next era has arrived.",
        "overlay_file": "fein_titans_hook.png",
        "audio": fein_cut,
        "inputs": [
            "assets/raw_footage/bellingham_arms.mp4",        # 0
            "assets/raw_footage/haaland_ucl.mp4"             # 1
        ],
        "filter": (
            "[0:v]trim=start=13.5:end=16.7,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=25.5:end=27.8,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=17.5:end=21.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=40.0:end=43.67,setpts=1.5*(PTS-STARTPTS),scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_index": 2,
        "overlay_index": 3
    },
    {
        "name": "Stereo_Love_Ronaldinho_Neymar.mp4",
        "hook": "They played for the love of the game.",
        "overlay_file": "stereo_samba_hook.png",
        "audio": stereo_cut,
        "inputs": [
            "assets/raw_footage/ronaldinho_samba.mp4",       # 0
            "assets/raw_footage/neymar_fresh.mp4"            # 1
        ],
        "filter": (
            "[0:v]trim=start=1.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=11.2:end=13.2,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=18.5:end=22.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=30.0:end=33.67,setpts=1.5*(PTS-STARTPTS),scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_index": 2,
        "overlay_index": 3
    },
    {
        "name": "Love_Me_Again_Messi_Ronaldo_GOATs.mp4",
        "hook": "We will never see another era like this.",
        "overlay_file": "love_goats_hook.png",
        "audio": love_cut,
        "inputs": [
            "assets/raw_footage/ronaldo_juve_goal.mp4",      # 0
            "assets/raw_footage/ronaldo_siuuu.mp4",          # 1
            "assets/raw_footage/messi_fresh.mp4"             # 2
        ],
        "filter": (
            "[0:v]trim=start=0.5:end=3.7,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=3.8:end=6.1,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[1:v]trim=start=5.6:end=9.3,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[2:v]trim=start=0.0:end=3.53,setpts=1.5*(PTS-STARTPTS),scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][4:v]overlay=0:0[v_final]"
        ),
        "audio_index": 3,
        "overlay_index": 4
    }
]

print("🚀 Starting Batch 6 Production with Trending Anthems...")

for idx, v in enumerate(VIDEOS, 1):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/3]: {v['name']}")
    print(f"=======================================================")
    
    overlay_path = create_hook_overlay(v["overlay_file"], v["hook"])
    output_path = os.path.join(EXPORTS, v["name"])
    
    cmd = [FFMPEG]
    for inp in v["inputs"]:
        cmd.extend(["-i", inp])
    cmd.extend(["-i", v["audio"]])
    cmd.extend(["-i", overlay_path])
    
    cmd.extend([
        "-filter_complex", v["filter"],
        "-map", "[v_final]",
        "-map", f"{v['audio_index']}:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-r", "60",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y", output_path
    ])
    
    print(f"⚡ Rendering {v['name']}...")
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Error rendering {v['name']}:", res.stderr[-600:])
        sys.exit(1)
    
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ EXPORT COMPLETE: {output_path} ({size_mb:.2f} MB)")

print("\n🎉 ALL 3 BATCH 6 MASTER VIDEOS SUCCESSFULLY CREATED!")
