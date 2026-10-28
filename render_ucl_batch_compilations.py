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

AUDIO_SRC = "assets/ronaldo_audio.mp3"

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

# 3 Master UCL Videos:
VIDEOS = [
    {
        "name": "Fancy_Footwork_UCL_Megamix.mp4",
        "hook": "UCL goals that shook the world.",
        "overlay_file": "ucl_megamix_hook.png",
        "inputs": [
            "assets/raw_footage/ronaldo_juve_goal.mp4",      # 0
            "assets/raw_footage/vini_goal_vs_bayern.mp4",     # 1
            "assets/raw_footage/haaland_ucl.mp4",             # 2
            "assets/raw_footage/bellingham_arms.mp4"          # 3
        ],
        "filter": (
            "[0:v]trim=start=1.0:end=3.857,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=3.5:end=6.357,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=34.5:end=38.31,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[3:v]trim=start=17.5:end=22.262,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][5:v]overlay=0:0[v_final]"
        ),
        "audio_index": 4,
        "overlay_index": 5
    },
    {
        "name": "Fancy_Footwork_Real_Madrid_UCL_Kings.mp4",
        "hook": "15 times Champions of Europe.",
        "overlay_file": "ucl_kings_hook.png",
        "inputs": [
            "assets/raw_footage/vini_goal_vs_bayern.mp4",     # 0
            "assets/raw_footage/vini_dortmund.mp4",           # 1
            "assets/raw_footage/bellingham_arms.mp4"          # 2
        ],
        "filter": (
            "[0:v]trim=start=2.0:end=5.81,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=38.81:end=40.714,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[1:v]trim=start=40.714:end=43.571,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[2:v]trim=start=17.5:end=23.214,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][4:v]overlay=0:0[v_final]"
        ),
        "audio_index": 3,
        "overlay_index": 4
    },
    {
        "name": "Fancy_Footwork_UCL_Coldest_Finishers.mp4",
        "hook": "Champions League cheat codes.",
        "overlay_file": "ucl_finishers_hook.png",
        "inputs": [
            "assets/raw_footage/ronaldo_juve_goal.mp4",      # 0
            "assets/raw_footage/haaland_ucl.mp4"              # 1
        ],
        "filter": (
            "[0:v]trim=start=0.5:end=4.31,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=6.5:end=8.404,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[1:v]trim=start=34.704:end=37.561,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=18.0:end=23.714,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_index": 2,
        "overlay_index": 3
    }
]

print("🚀 Starting UCL Goals & Celebrations Batch Production...")

for idx, v in enumerate(VIDEOS, 1):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/3]: {v['name']}")
    print(f"=======================================================")
    
    overlay_path = create_hook_overlay(v["overlay_file"], v["hook"])
    output_path = os.path.join(EXPORTS, v["name"])
    
    cmd = [FFMPEG]
    for inp in v["inputs"]:
        cmd.extend(["-i", inp])
    cmd.extend(["-i", AUDIO_SRC])
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

print("\n🎉 ALL 3 UCL MASTER COMPILATIONS SUCCESSFULLY CREATED!")
