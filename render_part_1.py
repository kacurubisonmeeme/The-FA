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

# 1. Prepare Audio Trims for Part 1
print("🎵 Preparing Part 1 Audio Cuts...")

audio_map = {
    "viva": os.path.join(ASSETS, "part1_viva.mp3"),
    "memory": os.path.join(ASSETS, "part1_memory.mp3"),
    "montagem": os.path.join(ASSETS, "part1_montagem.mp3"),
    "fein": os.path.join(ASSETS, "part1_fein.mp3"),
    "after_dark": os.path.join(ASSETS, "part1_after_dark.mp3"),
    "fancy": os.path.join(ASSETS, "part1_fancy.mp3")
}

subprocess.run([FFMPEG, "-ss", "0.2", "-t", "14.5", "-i", "assets/audio/viva_la_vida.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["viva"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "0.5", "-t", "14.5", "-i", "assets/audio/memory_reboot.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["memory"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "2.0", "-t", "14.5", "-i", "assets/audio/montagem_diamante.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["montagem"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/fein_slowed.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fein"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "10.0", "-t", "14.5", "-i", "assets/audio/after_dark.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["after_dark"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "15.0", "-t", "14.5", "-i", "assets/audio/fancy_footwork.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fancy"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Part 1 Audio cuts prepared.")

# 2. Typography Overlay Generator
def create_hook_overlay(filename, title, subtitle):
    path = os.path.join(ASSETS, filename)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 52)
        font_sub = ImageFont.truetype("arialbd.ttf", 36)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    def draw_text_with_shadow(draw, text, x, y, font, fill_color=(255, 215, 0, 255), shadow_color=(0, 0, 0, 240)):
        for ox, oy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0), (0, -4), (-4, 0)]:
            draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # Title (Gold)
    bbox1 = draw.textbbox((0, 0), title, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    draw_text_with_shadow(draw, title, (1080 - w1) // 2, 230, font_main, fill_color=(255, 220, 80, 255))

    # Subtitle (White)
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    draw_text_with_shadow(draw, subtitle, (1080 - w2) // 2, 305, font_sub, fill_color=(255, 255, 255, 255))

    img.save(path)
    return path

VIDEOS = [
    {
        "filename": "Kane_Part1_01_60_Goal_Masterpiece.mp4",
        "title": "60 GOALS IN ONE SEASON 👑",
        "subtitle": "HARRY KANE CONQUERED THE WORLD",
        "overlay": "kane_p1_01.png",
        "audio": audio_map["viva"],
        "footage": "assets/raw_footage/kane_bayern_goal.mp4",
        "cuts": [
            ("0.5", "4.0"),
            ("4.5", "8.5"),
            ("13.0", "16.5"),
            ("19.5", "23.0")
        ]
    },
    {
        "filename": "Kane_Part1_02_The_Curse_Is_Dead.mp4",
        "title": "THE TROPHY CURSE IS DEAD 🏆",
        "subtitle": "FROM HEARTBREAK TO IMMORTAL",
        "overlay": "kane_p1_02.png",
        "audio": audio_map["memory"],
        "footage": "assets/raw_footage/kane_bayern_goal.mp4",
        "cuts": [
            ("5.0", "8.5"),
            ("12.5", "16.0"),
            ("19.5", "23.5"),
            ("0.5", "4.0")
        ]
    },
    {
        "filename": "Kane_Part1_03_Halfway_Line_Screamer.mp4",
        "title": "THE GOAL THAT WON IT 🚀",
        "subtitle": "HARRY KANE FROM 50 YARDS",
        "overlay": "kane_p1_03.png",
        "audio": audio_map["montagem"],
        "footage": "assets/raw_footage/kane_screamer.mp4",
        "cuts": [
            ("1.0", "4.5"),
            ("5.0", "8.5"),
            ("10.0", "13.5"),
            ("14.0", "17.5")
        ]
    },
    {
        "filename": "Kane_Part1_04_World_Cup_Leader.mp4",
        "title": "WORLD CUP 2026 HERO 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "subtitle": "CAPTAIN. LEADER. BALLON D'OR.",
        "overlay": "kane_p1_04.png",
        "audio": audio_map["fein"],
        "footage": "assets/raw_footage/kane_england_goals.mp4",
        "cuts": [
            ("0.5", "4.0"),
            ("4.5", "8.5"),
            ("12.0", "15.5"),
            ("18.0", "21.5")
        ]
    },
    {
        "filename": "Kane_Part1_05_Most_Complete_Striker.mp4",
        "title": "STRIKER + PLAYMAKER 🪄",
        "subtitle": "THE MOST COMPLETE #9 ON EARTH",
        "overlay": "kane_p1_05.png",
        "audio": audio_map["after_dark"],
        "footage": "assets/raw_footage/kane_bayern_goal.mp4",
        "cuts": [
            ("1.0", "4.5"),
            ("5.0", "9.0"),
            ("13.0", "16.5"),
            ("20.0", "23.5")
        ]
    },
    {
        "filename": "Kane_Part1_06_UCL_Demolition_Job.mp4",
        "title": "UCL MASTERCLASS 🌪️",
        "subtitle": "4 GOALS IN ONE NIGHT",
        "overlay": "kane_p1_06.png",
        "audio": audio_map["fancy"],
        "footage": "assets/raw_footage/kane_screamer.mp4",
        "cuts": [
            ("2.0", "5.5"),
            ("6.0", "9.5"),
            ("11.0", "14.5"),
            ("15.0", "18.5")
        ]
    },
    {
        "filename": "Kane_Part1_07_Ice_In_His_Veins_Penalty.mp4",
        "title": "ICE IN THE VEINS ❄️",
        "subtitle": "100% UNSTOPPABLE FROM THE SPOT",
        "overlay": "kane_p1_07.png",
        "audio": audio_map["memory"],
        "footage": "assets/raw_footage/kane_england_goals.mp4",
        "cuts": [
            ("3.0", "6.5"),
            ("7.0", "10.5"),
            ("14.0", "17.5"),
            ("19.0", "22.5")
        ]
    },
    {
        "filename": "Kane_Part1_08_From_Doubted_To_King.mp4",
        "title": "THEY DOUBTED HIM 🤫",
        "subtitle": "NOW HE OWNS WORLD FOOTBALL",
        "overlay": "kane_p1_08.png",
        "audio": audio_map["viva"],
        "footage": "assets/raw_footage/kane_bayern_goal.mp4",
        "cuts": [
            ("0.5", "4.0"),
            ("19.5", "23.5"),
            ("5.0", "8.5"),
            ("13.0", "16.5")
        ]
    },
    {
        "filename": "Kane_Part1_09_Historic_Stats_Comparison.mp4",
        "title": "CHECK THE NUMBERS 📊",
        "subtitle": "62 GOALS • 16 ASSISTS • 1 TROPHY",
        "overlay": "kane_p1_09.png",
        "audio": audio_map["after_dark"],
        "footage": "assets/raw_footage/kane_screamer.mp4",
        "cuts": [
            ("0.5", "4.0"),
            ("5.0", "8.5"),
            ("9.5", "13.0"),
            ("14.0", "17.5")
        ]
    },
    {
        "filename": "Kane_Part1_10_Silent_Assassin_Strike.mp4",
        "title": "SILENCING 80,000 FANS 🤫",
        "subtitle": "ONE TOUCH IS ALL HE NEEDED",
        "overlay": "kane_p1_10.png",
        "audio": audio_map["fein"],
        "footage": "assets/raw_footage/kane_bayern_goal.mp4",
        "cuts": [
            ("4.5", "8.5"),
            ("12.5", "16.0"),
            ("19.5", "23.5"),
            ("1.0", "4.5")
        ]
    }
]

print("🚀 Starting Batch Render for Part 1 (10 Videos)...")

for idx, v in enumerate(VIDEOS, 1):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/10]: {v['filename']}")
    print(f"=======================================================")
    
    overlay_path = create_hook_overlay(v["overlay"], v["title"], v["subtitle"])
    output_path = os.path.join(EXPORTS, v["filename"])
    
    # Build filter segments
    seg_filters = []
    concat_inputs = []
    for s_idx, (st, en) in enumerate(v["cuts"]):
        label = f"c{s_idx+1}"
        seg_filters.append(f"[0:v]trim=start={st}:end={en},setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[{label}];")
        concat_inputs.append(f"[{label}]")
    
    concat_str = "".join(concat_inputs) + f"concat=n={len(v['cuts'])}:v=1:a=0[v_cat];"
    
    fx_filter = (
        "[v_cat]split[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
        "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
        "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
        "[v_base][2:v]overlay=0:0[v_final]"
    )
    
    full_filter = "".join(seg_filters) + concat_str + fx_filter
    
    cmd = [
        FFMPEG,
        "-i", v["footage"],
        "-i", v["audio"],
        "-i", overlay_path,
        "-filter_complex", full_filter,
        "-map", "[v_final]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y", output_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ SUCCESS: {v['filename']} exported! ({size:.2f} MB)")
    else:
        print(f"❌ ERROR rendering {v['filename']}:")
        print(res.stderr[-400:])

print("\n🎉 ALL 10 VIDEOS FOR PART 1 COMPLETED!")
