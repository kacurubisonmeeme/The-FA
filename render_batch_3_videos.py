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

VIDEOS = [
    {
        "name": "Fancy_Footwork_Vini_Wembley_Goal.mp4",
        "raw": "assets/raw_footage/vini_dortmund.mp4",
        "hook": "Sealed the 15th UCL at Wembley.",
        "overlay_file": "vini_wembley_goal_hook.png",
        "cuts": [
            ("35.0", "38.81", "c1"),
            ("38.81", "40.714", "c2"),
            ("40.714", "43.571", "c3"),
            ("46.5", "50.0", "c4_raw")
        ],
        "c4_filter": "[c4_raw]setpts=1.632857*(PTS-STARTPTS)[c4];"
    },
    {
        "name": "Fancy_Footwork_Haaland_Monster.mp4",
        "raw": "assets/raw_footage/haaland_ucl.mp4",
        "hook": "Pure power. Pure instinct.",
        "overlay_file": "haaland_monster_hook.png",
        "cuts": [
            ("1.0", "4.81", "c1"),
            ("4.81", "6.714", "c2"),
            ("6.714", "9.571", "c3"),
            ("18.0", "21.5", "c4_raw")
        ],
        "c4_filter": "[c4_raw]setpts=1.632857*(PTS-STARTPTS)[c4];"
    },
    {
        "name": "Fancy_Footwork_Ronaldinho_Magic.mp4",
        "raw": "assets/raw_footage/ronaldinho_samba.mp4",
        "hook": "He made football look like art.",
        "overlay_file": "ronaldinho_magic_hook.png",
        "cuts": [
            ("1.5", "5.31", "c1"),
            ("5.31", "7.214", "c2"),
            ("25.5", "28.357", "c3"),
            ("28.357", "31.857", "c4_raw")
        ],
        "c4_filter": "[c4_raw]setpts=1.632857*(PTS-STARTPTS)[c4];"
    },
    {
        "name": "Fancy_Footwork_Mbappe_World_Cup.mp4",
        "raw": "assets/raw_footage/mbappe_raw.mp4",
        "hook": "36 km/h. Good luck catching him.",
        "overlay_file": "mbappe_wc_hook.png",
        "cuts": [
            ("11.5", "15.31", "c1"),
            ("15.31", "17.214", "c2"),
            ("17.214", "20.071", "c3"),
            ("21.0", "24.5", "c4_raw")
        ],
        "c4_filter": "[c4_raw]setpts=1.632857*(PTS-STARTPTS)[c4];"
    }
]

print("🚀 Starting Batch 3 Production for 4 Master Videos...")

for idx, v in enumerate(VIDEOS, 1):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/4]: {v['name']}")
    print(f"=======================================================")
    
    overlay_path = create_hook_overlay(v["overlay_file"], v["hook"])
    output_path = os.path.join(EXPORTS, v["name"])
    
    trim_lines = "".join([f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[{tag}];" for start, end, tag in v["cuts"]])
    c4_line = v["c4_filter"]
    
    filter_complex = (
        f"{trim_lines}"
        f"{c4_line}"
        "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
        "[v_cat]split[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
        "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.22[fg_scaled];"
        "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
        "[v_base][2:v]overlay=0:0[v_final]"
    )
    
    cmd = [
        FFMPEG,
        "-i", v["raw"],
        "-i", AUDIO_SRC,
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
        "-y", output_path
    ]
    
    print(f"⚡ Rendering {v['name']}...")
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Error rendering {v['name']}:", res.stderr[-500:])
        sys.exit(1)
    
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ EXPORT COMPLETE: {output_path} ({size_mb:.2f} MB)")

print("\n🎉 ALL 4 MASTER VIDEOS SUCCESSFULLY CREATED!")
