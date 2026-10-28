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

# 1. Prepare Audio Trims for Part 2
print("🎵 Preparing Part 2 Audio Cuts...")

audio_map = {
    "viva": os.path.join(ASSETS, "part2_viva.mp3"),
    "memory": os.path.join(ASSETS, "part2_memory.mp3"),
    "montagem": os.path.join(ASSETS, "part2_montagem.mp3"),
    "fein": os.path.join(ASSETS, "part2_fein.mp3"),
    "after_dark": os.path.join(ASSETS, "part2_after_dark.mp3"),
    "fancy": os.path.join(ASSETS, "part2_fancy.mp3"),
    "stereo": os.path.join(ASSETS, "part2_stereo.mp3"),
    "love": os.path.join(ASSETS, "part2_love.mp3")
}

subprocess.run([FFMPEG, "-ss", "0.2", "-t", "14.5", "-i", "assets/audio/viva_la_vida.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["viva"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "0.5", "-t", "14.5", "-i", "assets/audio/memory_reboot.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["memory"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "2.0", "-t", "14.5", "-i", "assets/audio/montagem_diamante.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["montagem"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/fein_slowed.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fein"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "10.0", "-t", "14.5", "-i", "assets/audio/after_dark.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["after_dark"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "15.0", "-t", "14.5", "-i", "assets/audio/fancy_footwork.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["fancy"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.0", "-t", "14.5", "-i", "assets/audio/stereo_love.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["stereo"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([FFMPEG, "-ss", "1.5", "-t", "14.5", "-i", "assets/audio/love_me_again.mp3", "-af", "afade=t=out:st=13.5:d=1.0", "-y", audio_map["love"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Part 2 Audio cuts prepared.")

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
        "filename": "Gala_Part2_11_10_Seconds_Before_Envelope.mp4",
        "title": "10 SECONDS BEFORE HISTORY ⏳",
        "subtitle": "THE ENVELOPE IS OPENED IN LONDON",
        "overlay": "gala_p2_11.png",
        "audio": audio_map["after_dark"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/mbappe_raw.mp4", "assets/raw_footage/yamal_euro_goal.mp4"],
        "filter": (
            "[0:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=1.5:end=5.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=1.0:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
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
        "filename": "Gala_Part2_12_Tears_On_Stage_Speech.mp4",
        "title": "TEARS ON STAGE 🥹",
        "subtitle": "20 YEARS OF WORK IN ONE SPEECH",
        "overlay": "gala_p2_12.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=19.5:end=24.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[0:v]trim=start=13.0:end=17.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
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
        "filename": "Gala_Part2_13_Mbappe_Yamal_Reaction.mp4",
        "title": "THE PODIUM REACTION 👑",
        "subtitle": "MBAPPE & YAMAL APPLAUD THE KING",
        "overlay": "gala_p2_13.png",
        "audio": audio_map["fein"],
        "inputs": ["assets/raw_footage/mbappe_raw.mp4", "assets/raw_footage/yamal_skills.mp4", "assets/raw_footage/kane_screamer.mp4"],
        "filter": (
            "[0:v]trim=start=27.0:end=31.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=12.0:end=15.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[2:v]trim=start=5.0:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[2:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Gala_Part2_14_Lifting_The_Golden_Ball.mp4",
        "title": "ENGLAND'S 25-YEAR DROUGHT OVER 🏆",
        "subtitle": "HARRY KANE LIFTS THE GOLD",
        "overlay": "gala_p2_14.png",
        "audio": audio_map["viva"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/kane_england_goals.mp4"],
        "filter": (
            "[0:v]trim=start=19.5:end=24.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=4.5:end=8.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=18.0:end=20.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Gala_Part2_15_Three_Lions_Celebration.mp4",
        "title": "THREE LIONS REACT 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "subtitle": "BELLINGHAM, FODEN & SAKA CELEBRATE",
        "overlay": "gala_p2_15.png",
        "audio": audio_map["fancy"],
        "inputs": ["assets/raw_footage/bellingham_arms.mp4", "assets/raw_footage/kane_england_goals.mp4"],
        "filter": (
            "[0:v]trim=start=2.0:end=6.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=8.0:end=11.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=12.0:end=15.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Gala_Part2_16_Bayern_Locker_Room_Party.mp4",
        "title": "BAYERN MUNICH PARTY 🎉",
        "subtitle": "THE LOCKER ROOM GOES WILD FOR KANE",
        "overlay": "gala_p2_16.png",
        "audio": audio_map["montagem"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/kane_screamer.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=5.0:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
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
        "filename": "Gala_Part2_17_London_Red_Carpet_Royalty.mp4",
        "title": "LONDON RED CARPET 💎",
        "subtitle": "THE KING RETURNS HOME",
        "overlay": "gala_p2_17.png",
        "audio": audio_map["stereo"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=1.0:end=5.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=0.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=10.0:end=13.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
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
        "filename": "Gala_Part2_18_Legends_Handing_The_Torch.mp4",
        "title": "PASSING THE TORCH 🤝",
        "subtitle": "FOOTBALL LEGENDS CROWN HARRY KANE",
        "overlay": "gala_p2_18.png",
        "audio": audio_map["love"],
        "inputs": ["assets/raw_footage/kane_bayern_goal.mp4", "assets/raw_footage/haaland_ucl.mp4"],
        "filter": (
            "[0:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=10.0:end=13.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=19.5:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
            "[1:v]trim=start=20.0:end=23.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c4];"
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
        "filename": "Gala_Part2_19_Most_Humble_Speech.mp4",
        "title": "CLASS OVER HYPE 🗣️",
        "subtitle": "THE MOST HUMBLE SPEECH IN FOOTBALL",
        "overlay": "gala_p2_19.png",
        "audio": audio_map["memory"],
        "inputs": ["assets/raw_footage/kane_england_goals.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=0.5:end=4.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=13.0:end=17.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
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
        "filename": "Gala_Part2_20_London_Midnight_Aura.mp4",
        "title": "MIDNIGHT IN LONDON 🌃",
        "subtitle": "THE BALLON D'OR SHINES OVER BIG BEN",
        "overlay": "gala_p2_20.png",
        "audio": audio_map["after_dark"],
        "inputs": ["assets/raw_footage/kane_screamer.mp4", "assets/raw_footage/kane_bayern_goal.mp4"],
        "filter": (
            "[0:v]trim=start=5.0:end=9.0,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c1];"
            "[1:v]trim=start=4.5:end=8.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c2];"
            "[0:v]trim=start=14.0:end=17.5,setpts=PTS-STARTPTS,scale=1920:1080,setsar=1[c3];"
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
    }
]

print("🚀 Starting Batch Render for Part 2 (Videos #11 - #20)...")

for idx, v in enumerate(VIDEOS, 11):
    print(f"\n=======================================================")
    print(f"🎬 Processing [{idx}/20]: {v['filename']}")
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

print("\n🎉 ALL 10 VIDEOS FOR PART 2 COMPLETED!")
