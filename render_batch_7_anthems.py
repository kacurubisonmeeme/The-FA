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
print("🎵 Trimming Batch 7 Audio Tracks...")
after_dark_cut = os.path.join(ASSETS, "after_dark_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "10.2", "-t", "14.5", "-i", "assets/audio/after_dark.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", after_dark_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

viva_cut = os.path.join(ASSETS, "viva_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "0.2", "-t", "14.5", "-i", "assets/audio/viva_la_vida.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", viva_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

bibi_cut = os.path.join(ASSETS, "bibi_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "4.8", "-t", "14.5", "-i", "assets/audio/bibi_fogosa.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", bibi_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Batch 7 Audio tracks trimmed.")

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
        "name": "After_Dark_Mbappe_Vini_Aura.mp4",
        "hook": "Built for the biggest nights.",
        "overlay_file": "after_dark_hook.png",
        "audio": after_dark_cut,
        "inputs": [
            "assets/raw_footage/mbappe_raw.mp4",              # 0
            "assets/raw_footage/vini_goal_vs_bayern.mp4"      # 1
        ],
        "filter": (
            "[0:v]trim=start=1.5:end=4.7,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=3.0:end=5.4,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=27.5:end=31.1,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=7.6:end=11.13,setpts=1.5*(PTS-STARTPTS),scale=1920:1080,setsar=1[c4];"
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
        "name": "Viva_La_Vida_Messi_Ronaldinho_Royalty.mp4",
        "hook": "When football was pure cinema.",
        "overlay_file": "viva_royalty_hook.png",
        "audio": viva_cut,
        "inputs": [
            "assets/raw_footage/ronaldinho_samba.mp4",       # 0
            "assets/raw_footage/messi_fresh.mp4"             # 1
        ],
        "filter": (
            "[0:v]trim=start=1.5:end=4.7,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=5.3:end=7.7,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[1:v]trim=start=0.0:end=3.9,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=28.3:end=31.63,setpts=1.5*(PTS-STARTPTS),scale=1920:1080,setsar=1[c4];"
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
        "name": "Automotivo_Samba_Holy_Trinity.mp4",
        "hook": "Brazilian blood. Pure magic.",
        "overlay_file": "brazilian_trinity_hook.png",
        "audio": bibi_cut,
        "inputs": [
            "assets/raw_footage/ronaldinho_samba.mp4",       # 0
            "assets/raw_footage/vini_dortmund.mp4",          # 1
            "assets/raw_footage/neymar_fresh.mp4"            # 2
        ],
        "filter": (
            "[0:v]trim=start=10.0:end=12.8,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=82.5:end=84.7,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=18.0:end=21.8,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[2:v]trim=start=30.0:end=33.8,setpts=1.5*(PTS-STARTPTS),scale=1920:1080,setsar=1[c4];"
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

print("🚀 Starting Batch 7 Production with Iconic Anthems...")

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

print("\n🎉 ALL 3 BATCH 7 MASTER VIDEOS SUCCESSFULLY CREATED!")
