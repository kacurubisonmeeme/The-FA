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

# 1. Prepare Audio Trims for Part 4
print("🎵 Preparing Part 4 Audio Cuts...")

audio_map = {
    "viva": os.path.join(ASSETS, "part4_viva.mp3"),
    "memory": os.path.join(ASSETS, "part4_memory.mp3"),
    "fein": os.path.join(ASSETS, "part4_fein.mp3"),
    "after_dark": os.path.join(ASSETS, "part4_after_dark.mp3"),
    "fancy": os.path.join(ASSETS, "part4_fancy.mp3"),
    "stereo": os.path.join(ASSETS, "part4_stereo.mp3"),
    "love": os.path.join(ASSETS, "part4_love.mp3")
}

subprocess.run([FFMPEG, "-ss", "0.2", "-t", "14.5", "-i", "assets/audio/viva_la_vida.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["viva"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "0.5", "-t", "14.5", "-i", "assets/audio/memory_reboot.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["memory"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/fein_slowed.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fein"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "10.0", "-t", "14.5", "-i", "assets/audio/after_dark.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["after_dark"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "15.0", "-t", "14.5", "-i", "assets/audio/fancy_footwork.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fancy"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/stereo_love.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["stereo"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.5", "-t", "14.5", "-i", "assets/audio/love_me_again.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["love"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Part 4 Audio cuts prepared.")

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
        "filename": "History_Part4_31_First_English_Winner_Since_Owen.mp4",
        "title": "25 YEARS OF WAITING OVER 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "subtitle": "FIRST ENGLISH WINNER SINCE OWEN (2001)",
        "overlay": "hist_p4_31.png",
        "audio": audio_map["love"],
        "inputs": ["assets/raw_footage/kane_england_goals.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=0.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
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
        "filename": "History_Part4_32_The_Elite_5_English_Legends.mp4",
        "title": "THE ELITE 5 👑",
        "subtitle": "ONLY 5 ENGLISHMEN HAVE TOUCHED THIS",
        "overlay": "hist_p4_32.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=19.5:end=23.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "History_Part4_33_David_Beckham_Reaction.mp4",
        "title": "BECKHAM WATCHING FROM VIP 🥹",
        "subtitle": "AN ENGLAND CAPTAIN FINALLY WINS IT",
        "overlay": "hist_p4_33.png",
        "audio": audio_map["stereo"],
        "inputs": ["assets/raw_footage/kane_england_goals.mp4", "assets/raw_footage/bellingham_arms.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=2.0:end=5.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=8.0:end=11.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.18:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "History_Part4_34_CR7_2008_Flashback.mp4",
        "title": "2008 TO 2026 ⏳",
        "subtitle": "CRISTIANO RONALDO'S ENGLISH LEGACY",
        "overlay": "hist_p4_34.png",
        "audio": audio_map["memory"],
        "inputs": ["assets/raw_footage/ronaldo_juve_goal.mp4", "assets/raw_footage/ronaldo_siuuu.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=2.0:end=6.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=0.5:end=3.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[2:v]trim=start=19.5:end=22.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "History_Part4_35_Wayne_Rooney_Tribute.mp4",
        "title": "FROM ROONEY TO KANE 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "subtitle": "PASSING THE ALL-TIME CROWN",
        "overlay": "hist_p4_35.png",
        "audio": audio_map["after_dark"],
        "inputs": ["assets/raw_footage/kane_england_goals.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=0.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
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
        "filename": "History_Part4_36_Lampard_Gerrard_2005_Podium.mp4",
        "title": "FINISHING THE MISSION 🏆",
        "subtitle": "FOR LAMPARD & GERRARD IN 2005",
        "overlay": "hist_p4_36.png",
        "audio": audio_map["love"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=5.0:end=9.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=19.5:end=22.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
            "[c1][c2][c3][c4]concat=n=4:v=1:a=0[v_cat];"
            "[v_cat]split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.18[bg_blur];"
            "[fg]scale=1080:-2,unsharp=5:5:1.2:5:5:0.0,eq=contrast=1.20:saturation=1.24[fg_scaled];"
            "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[v_base];"
            "[v_base][3:v]overlay=0:0[v_final]"
        ),
        "audio_idx": 2,
        "overlay_idx": 3
    },
    {
        "filename": "History_Part4_37_Tottenham_Academy_To_Immortality.mp4",
        "title": "THE BOY FROM WALTHAMSTOW 📍",
        "subtitle": "FROM REJECTED TO BALLON D'OR",
        "overlay": "hist_p4_37.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/kane_england_goals.mp4"],
        "filter": (
            "[0:v]trim=start=0.5:end=4.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=13.0:end=16.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "History_Part4_38_Sir_Bobby_Charlton_Spirit.mp4",
        "title": "SIR BOBBY'S LEGACY 🕊️",
        "subtitle": "THE SPIRIT OF 1966 LIVES ON",
        "overlay": "hist_p4_38.png",
        "audio": audio_map["after_dark"],
        "inputs": ["assets/raw_footage/kane_england_goals.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=4.5:end=7.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "History_Part4_39_England_New_Golden_Generation.mp4",
        "title": "THE NEW GOLDEN GENERATION 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "subtitle": "KANE • BELLINGHAM • FODEN • SAKA",
        "overlay": "hist_p4_39.png",
        "audio": audio_map["fancy"],
        "inputs": ["assets/raw_footage/bellingham_arms.mp4", "assets/raw_footage/kane_england_goals.mp4"],
        "filter": (
            "[0:v]trim=start=2.0:end=5.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=8.0:end=11.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=18.0:end=21.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "History_Part4_40_Front_Page_Of_Every_Newspaper.mp4",
        "title": "KING KANE 📰",
        "subtitle": "ONE MAN UNITED EVERY FRONT PAGE",
        "overlay": "hist_p4_40.png",
        "audio": audio_map["fein"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=19.5:end=23.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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

print("🚀 Starting Batch Render for Part 4 (Videos #31 - #40)...")

for idx, v in enumerate(VIDEOS, 31):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/40]: {v['filename']}")
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

print("\n🎉 ALL 10 VIDEOS FOR PART 4 COMPLETED!")
