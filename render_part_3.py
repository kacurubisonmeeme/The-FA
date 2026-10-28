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

# 1. Prepare Audio Trims for Part 3
print("🎵 Preparing Part 3 Audio Cuts...")

audio_map = {
    "viva": os.path.join(ASSETS, "part3_viva.mp3"),
    "memory": os.path.join(ASSETS, "part3_memory.mp3"),
    "montagem": os.path.join(ASSETS, "part3_montagem.mp3"),
    "fein": os.path.join(ASSETS, "part3_fein.mp3"),
    "after_dark": os.path.join(ASSETS, "part3_after_dark.mp3"),
    "fancy": os.path.join(ASSETS, "part3_fancy.mp3"),
    "stereo": os.path.join(ASSETS, "part3_stereo.mp3"),
    "love": os.path.join(ASSETS, "part3_love.mp3"),
    "bibi": os.path.join(ASSETS, "part3_bibi.mp3")
}

subprocess.run([FFMPEG, "-ss", "0.2", "-t", "14.5", "-i", "assets/audio/viva_la_vida.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["viva"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "0.5", "-t", "14.5", "-i", "assets/audio/memory_reboot.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["memory"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "2.0", "-t", "14.5", "-i", "assets/audio/montagem_diamante.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["montagem"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/fein_slowed.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fein"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "10.0", "-t", "14.5", "-i", "assets/audio/after_dark.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["after_dark"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "15.0", "-t", "14.5", "-i", "assets/audio/fancy_footwork.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fancy"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/stereo_love.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["stereo"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.5", "-t", "14.5", "-i", "assets/audio/love_me_again.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["love"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "4.8", "-t", "14.5", "-i", "assets/audio/bibi_fogosa.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["bibi"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Part 3 Audio cuts prepared.")

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
        "filename": "Podium_Part3_21_Mbappe_Most_Dangerous_Runner_Up.mp4",
        "title": "MOST DANGEROUS RUNNER-UP ⚡",
        "subtitle": "MBAPPE IS TAKING 2027 PERSONALLY",
        "overlay": "podium_p3_21.png",
        "audio": audio_map["fein"],
        "inputs": ["assets/raw_footage/mbappe_raw.mp4"],
        "filter": (
            "[0:v]trim=start=1.5:end=5.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=7.0:end=10.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=27.0:end=31.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.18:saturation=1.26[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][2:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 1,
        "overlay_idx": 2
    },
    {
        "filename": "Podium_Part3_22_Yamal_On_Podium_At_19.mp4",
        "title": "WORLD PODIUM AT 19 YEARS OLD 🪄",
        "subtitle": "LAMINE YAMAL IS NOT NORMAL",
        "overlay": "podium_p3_22.png",
        "audio": audio_map["montagem"],
        "inputs": ["assets/raw_footage/yamal_skills.mp4", "assets/raw_footage/yamal_euro_goal.mp4"],
        "filter": (
            "[0:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=3.5:end=7.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=12.0:end=15.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=13.0:end=16.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Podium_Part3_23_Mbappe_The_Villain_Arc.mp4",
        "title": "THE VILLAIN ARC BEGINS 😈",
        "subtitle": "THAT LOOK MEANS 50 GOALS NEXT YEAR",
        "overlay": "podium_p3_23.png",
        "audio": audio_map["after_dark"],
        "inputs": ["assets/raw_footage/mbappe_raw.mp4"],
        "filter": (
            "[0:v]trim=start=27.5:end=31.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=1.5:end=5.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=7.0:end=10.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.22[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.22[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][2:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 1,
        "overlay_idx": 2
    },
    {
        "filename": "Podium_Part3_24_3_Generations_One_Stage.mp4",
        "title": "3 GENERATIONS ON ONE PODIUM 👑",
        "subtitle": "KANE (33) • MBAPPE (27) • YAMAL (19)",
        "overlay": "podium_p3_24.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/mbappe_raw.mp4", "assets/raw_footage/yamal_euro_goal.mp4"],
        "filter": (
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=27.5:end=31.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=13.0:end=17.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=5.0:end=7.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.26[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][4:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 3,
        "overlay_idx": 4
    },
    {
        "filename": "Podium_Part3_25_Did_Mbappe_Deserve_It.mp4",
        "title": "TROPHIES VS MOMENTS 📊",
        "subtitle": "WHO ACTUALLY HAD YOUR VOTE?",
        "overlay": "podium_p3_25.png",
        "audio": audio_map["fancy"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/mbappe_raw.mp4"],
        "filter": (
            "[0:v]trim=start=5.0:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=27.0:end=30.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Podium_Part3_26_Yamal_Youngest_Since_R9.mp4",
        "title": "YOUNGEST SINCE R9 IN 1996 🛸",
        "subtitle": "LAMINE YAMAL SHATTERS THE MATRIX",
        "overlay": "podium_p3_26.png",
        "audio": audio_map["stereo"],
        "inputs": ["assets/raw_footage/yamal_euro_goal.mp4", "assets/raw_footage/yamal_skills.mp4"],
        "filter": (
            "[0:v]trim=start=3.5:end=7.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=13.0:end=16.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=12.0:end=15.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Podium_Part3_27_Kane_Mbappe_Handshake.mp4",
        "title": "REAL RECOGNIZE REAL 🤝",
        "subtitle": "THE RESPECT BETWEEN TWO CAPTAINS",
        "overlay": "podium_p3_27.png",
        "audio": audio_map["love"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/mbappe_raw.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=27.5:end=30.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Podium_Part3_28_Yamal_London_Swagger.mp4",
        "title": "19-YEAR-OLD AURA 🔥",
        "subtitle": "LAMINE YAMAL'S LONDON SWAGGER",
        "overlay": "podium_p3_28.png",
        "audio": audio_map["bibi"],
        "inputs": ["assets/raw_footage/yamal_skills.mp4", "assets/raw_footage/yamal_euro_goal.mp4"],
        "filter": (
            "[0:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=3.5:end=7.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=13.0:end=16.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Podium_Part3_29_Mbappe_vs_Yamal_Next_Decade.mp4",
        "title": "THE NEXT 10 YEARS ⚔️",
        "subtitle": "MBAPPE VS YAMAL HAS BEGUN",
        "overlay": "podium_p3_29.png",
        "audio": audio_map["fein"],
        "inputs": ["assets/raw_footage/mbappe_raw.mp4", "assets/raw_footage/yamal_skills.mp4"],
        "filter": (
            "[0:v]trim=start=1.5:end=5.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.26[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "Podium_Part3_30_The_French_Media_Reaction.mp4",
        "title": "FRANCE FOOTBALL'S TOUGHEST CALL 🇫🇷",
        "subtitle": "CROWNING AN ENGLISHMAN OVER MBAPPE",
        "overlay": "podium_p3_30.png",
        "audio": audio_map["after_dark"],
        "inputs": ["assets/raw_footage/mbappe_raw.mp4", "assets/raw_footage/kane_screamer.mp4"],
        "filter": (
            "[0:v]trim=start=27.5:end=31.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=5.0:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=16.0:end=19.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.20[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    }
]

print("🚀 Starting Batch Render for Part 3 (Videos #21 - #30)...")

for idx, v in enumerate(VIDEOS, 21):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/30]: {v['filename']}")
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

print("\n🎉 ALL 10 VIDEOS FOR PART 3 COMPLETED!")
