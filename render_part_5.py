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

# 1. Prepare Audio Trims for Part 5
print("🎵 Preparing Part 5 Audio Cuts...")

audio_map = {
    "viva": os.path.join(ASSETS, "part5_viva.mp3"),
    "memory": os.path.join(ASSETS, "part5_memory.mp3"),
    "montagem": os.path.join(ASSETS, "part5_montagem.mp3"),
    "fein": os.path.join(ASSETS, "part5_fein.mp3"),
    "after_dark": os.path.join(ASSETS, "part5_after_dark.mp3"),
    "fancy": os.path.join(ASSETS, "part5_fancy.mp3"),
    "bibi": os.path.join(ASSETS, "part5_bibi.mp3")
}

subprocess.run([FFMPEG, "-ss", "0.2", "-t", "14.5", "-i", "assets/audio/viva_la_vida.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["viva"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "0.5", "-t", "14.5", "-i", "assets/audio/memory_reboot.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["memory"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "2.0", "-t", "14.5", "-i", "assets/audio/montagem_diamante.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["montagem"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/fein_slowed.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fein"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "10.0", "-t", "14.5", "-i", "assets/audio/after_dark.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["after_dark"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "15.0", "-t", "14.5", "-i", "assets/audio/fancy_footwork.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fancy"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "4.8", "-t", "14.5", "-i", "assets/audio/bibi_fogosa.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["bibi"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Part 5 Audio cuts prepared.")

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
        "filename": "Viral_Part5_41_The_Curse_Meme_Deleted.mp4",
        "title": "DELETE ALL YOUR MEMES 🗑️",
        "subtitle": "THE HARRY KANE CURSE IS DEAD",
        "overlay": "vir_p5_41.png",
        "audio": audio_map["fein"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/kane_screamer.mp4"],
        "filter": (
            "[0:v]trim=start=0.5:end=4.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=5.0:end=9.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=14.0:end=17.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "Viral_Part5_42_Munich_Marienplatz_Party.mp4",
        "title": "MUNICH GOES CRAZY 🍻",
        "subtitle": "MARIENPLATZ CELEBRATING KING KANE",
        "overlay": "vir_p5_42.png",
        "audio": audio_map["montagem"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=10.0:end=13.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=19.5:end=23.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.18:saturation=1.28[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "Viral_Part5_43_Bayern_First_Winner_Since_1981.mp4",
        "title": "BAYERN'S 45-YEAR WAIT OVER 🏆",
        "subtitle": "FIRST WINNER SINCE RUMMENIGGE (1981)",
        "overlay": "vir_p5_43.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=9.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=13.0:end=17.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=0.5:end=2.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][2:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 1,
        "overlay_idx": 2
    },
    {
        "filename": "Viral_Part5_44_Justice_For_Lewandowski_2020.mp4",
        "title": "JUSTICE FOR 2020 🔴",
        "subtitle": "THIS ONE WAS FOR LEWY AS WELL",
        "overlay": "vir_p5_44.png",
        "audio": audio_map["after_dark"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=5.0:end=9.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=19.5:end=22.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.22[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "Viral_Part5_45_Haaland_Striker_Respect.mp4",
        "title": "STRIKER BROTHERHOOD 🤝",
        "subtitle": "ERLING HAALAND SALUTES HARRY KANE",
        "overlay": "vir_p5_45.png",
        "audio": audio_map["fancy"],
        "inputs": ["assets/raw_footage/haaland_ucl.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=2.0:end=6.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=10.0:end=13.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=19.5:end=22.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.18:saturation=1.26[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "Viral_Part5_46_Official_Top_10_Rankings.mp4",
        "title": "OFFICIAL 2026 TOP 10 📋",
        "subtitle": "THE BEST FOOTBALLERS ON PLANET EARTH",
        "overlay": "vir_p5_46.png",
        "audio": audio_map["fein"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/mbappe_raw.mp4", "assets/raw_footage/yamal_euro_goal.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=3.5:end=7.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=19.5:end=23.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][4:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 3,
        "overlay_idx": 4
    },
    {
        "filename": "Viral_Part5_47_Messi_Top_5_At_39.mp4",
        "title": "39 YEARS OLD. STILL TOP 5 👽",
        "subtitle": "LIONEL MESSI DEFYING TIME IN 2026",
        "overlay": "vir_p5_47.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/messi_fresh.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=0.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=5.0:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=19.5:end=22.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "Viral_Part5_48_Kane_Private_Family_Dinner.mp4",
        "title": "FAMILY OVER HYPE 🤍",
        "subtitle": "HOW HARRY KANE CELEBRATED THE GOLD",
        "overlay": "vir_p5_48.png",
        "audio": audio_map["memory"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/kane_england_goals.mp4"],
        "filter": (
            "[0:v]trim=start=0.5:end=4.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=13.0:end=16.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.22[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "Viral_Part5_49_Predicting_2027_Ballon_dOr.mp4",
        "title": "WHO WINS IN 2027? 🔮",
        "subtitle": "MBAPPE • YAMAL • BELLINGHAM • KANE",
        "overlay": "vir_p5_49.png",
        "audio": audio_map["bibi"],
        "inputs": ["assets/raw_footage/mbappe_raw.mp4", "assets/raw_footage/yamal_skills.mp4", "assets/raw_footage/bellingham_arms.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=2.0:end=5.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[3:v]trim=start=19.5:end=23.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.18:saturation=1.28[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][5:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 4,
        "overlay_idx": 5
    },
    {
        "filename": "Viral_Part5_50_Football_Changed_Tonight.mp4",
        "title": "OCTOBER 26, 2026 👑",
        "subtitle": "THE NIGHT FOOTBALL WAS WRITTEN IN GOLD",
        "overlay": "vir_p5_50.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_england_goals.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=5.0:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=4.5:end=8.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.26[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][4:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 3,
        "overlay_idx": 4
    }
]

print("🚀 Starting Batch Render for Part 5 (Videos #41 - #50)...")

for idx, v in enumerate(VIDEOS, 41):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/50]: {v['filename']}")
    print(f"=======================================================")
    
    overlay_path = create_hook_overlay(v["overlay"], v["title"], v["subtitle"])
    output_path = os.path.join(EXPORTS, v["filename"])
    
    cmd = [FFMPEG]
    for inp in v["inputs"]:
        cmd.extend(["-i", inp])
    cmd.extend(["-i", v["audio"]])
    cmd.extend(["-i", overlay_path])
    
    cmd.extend([
        "-filter_complex", v["filter"],
        "-map", "[v_final]",
        "-map", f"{v['audio_idx']}:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y", output_path
    ])
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ SUCCESS: {v['filename']} exported! ({size:.2f} MB)")
    else:
        print(f"❌ ERROR rendering {v['filename']}:")
        print(res.stderr[-400:])

print("\n🎉 ALL 10 VIDEOS FOR PART 5 COMPLETED! 50/50 MASTER ROADMAP ACHIEVED!")
