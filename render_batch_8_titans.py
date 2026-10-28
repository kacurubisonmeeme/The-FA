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

# 1. Prepare Audio Cuts
print("Trimming Batch 8 Audio Tracks...")

montagem_cut = os.path.join(ASSETS, "montagem_yamal_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "2.0", "-t", "14.5", "-i", "assets/audio/montagem_diamante.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", montagem_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

memory_cut = os.path.join(ASSETS, "memory_kane_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "0.5", "-t", "14.5", "-i", "assets/audio/memory_reboot.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", memory_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

fancy_cut = os.path.join(ASSETS, "fancy_mbappe_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "15.0", "-t", "14.5", "-i", "assets/audio/fancy_footwork.mp3",
    "-af", "afade=t=out:st=13.5:d=1.0", "-y", fancy_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

fein_cut = os.path.join(ASSETS, "fein_titans_cut.mp3")
subprocess.run([
    FFMPEG, "-ss", "1.0", "-t", "15.0", "-i", "assets/audio/fein_slowed.mp3",
    "-af", "afade=t=out:st=14.0:d=1.0", "-y", fein_cut
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Audio cuts prepared successfully.")

# 2. Text Overlay Helper
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
    
    # Calculate bounding box for center alignment
    bbox = draw.textbbox((0, 0), hook_text, font=font)
    w = bbox[2] - bbox[0]
    draw_text_with_shadow(draw, hook_text, (1080 - w) // 2, 260, font)
    img.save(path)
    return path

VIDEOS = [
    {
        "name": "Montagem_Yamal_Golden_Boy.mp4",
        "hook": "LAMINE YAMAL: THE CHOSEN ONE",
        "overlay_file": "yamal_hook.png",
        "audio": montagem_cut,
        "inputs": [
            "assets/raw_footage/yamal_skills.mp4",       # 0
            "assets/raw_footage/yamal_euro_goal.mp4"     # 1
        ],
        "filter": (
            "[0:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=3.0:end=7.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=12.0:end=15.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=13.0:end=16.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.18:saturation=1.28[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_index": 2,
        "overlay_index": 3
    },
    {
        "name": "Memory_Reboot_Kane_Cold_Marksman.mp4",
        "hook": "HARRY KANE: LETHAL PRECISION",
        "overlay_file": "kane_hook.png",
        "audio": memory_cut,
        "inputs": [
            "assets/raw_footage/kane_bayern_goal.mp4"     # 0
        ],
        "filter": (
            "[0:v]trim=start=0.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=5.0:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=13.0:end=16.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=20.0:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.22[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.12[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][2:v]overlay=0:0[v_final]"
        ),
        "audio_index": 1,
        "overlay_index": 2
    },
    {
        "name": "Fancy_Footwork_Mbappe_Speed_Demon.mp4",
        "hook": "KYLIAN MBAPPE: SPEED OF SOUND",
        "overlay_file": "mbappe_hook.png",
        "audio": fancy_cut,
        "inputs": [
            "assets/raw_footage/mbappe_raw.mp4"          # 0
        ],
        "filter": (
            "[0:v]trim=start=1.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=7.0:end=10.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=27.0:end=31.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.16:saturation=1.26[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][2:v]overlay=0:0[v_final]"
        ),
        "audio_index": 1,
        "overlay_index": 2
    },
    {
        "name": "FEIN_Titans_Kane_Mbappe_Yamal.mp4",
        "hook": "3 GENERATIONS: KANE x MBAPPE x YAMAL",
        "overlay_file": "titans_hook.png",
        "audio": fein_cut,
        "inputs": [
            "assets/raw_footage/kane_bayern_goal.mp4",    # 0
            "assets/raw_footage/mbappe_raw.mp4",         # 1
            "assets/raw_footage/yamal_euro_goal.mp4"     # 2
        ],
        "filter": (
            "[0:v]trim=start=5.0:end=7.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=20.0:end=22.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[1:v]trim=start=16.0:end=18.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=27.5:end=30.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[2:v]trim=start=3.5:end=6.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c5];"
            "[2:v]trim=start=13.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c6];"
            "[c1][c2][c3][c4][c5][c6]concat=n=6:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.18:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][4:v]overlay=0:0[v_final]"
        ),
        "audio_index": 3,
        "overlay_index": 4
    }
]

print("Starting Batch 8 (Kane, Mbappe, Yamal) Production...")

for idx, v in enumerate(VIDEOS, 1):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/4]: {v['name']}")
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
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y", output_path
    ])
    
    print(f"Executing FFmpeg render for {v['name']}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"SUCCESS: {v['name']} exported! ({size:.2f} MB)")
    else:
        print(f"ERROR rendering {v['name']}:")
        print(res.stderr[-500:])

print("\nALL BATCH 8 VIDEOS COMPLETED!")
