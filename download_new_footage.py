import subprocess
import os
import sys

def download_clip(query, output_name):
    out_path = os.path.join("assets", "raw_footage", f"{output_name}.mp4")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"File {out_path} already exists ({os.path.getsize(out_path)} bytes), skipping.")
        return True
    
    cmd = [
        sys.executable, "-m", "yt_dlp",
        f"ytsearch1:{query}",
        "--format", "best[height<=1080]/bestvideo[height<=1080]+bestaudio/best",
        "--output", out_path,
        "--no-playlist",
        "--merge-output-format", "mp4"
    ]
    print(f"Fetching: {query} -> {output_name}")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if res.returncode == 0:
            print(f"Success: {output_name} saved.")
            return True
        else:
            print(f"Error downloading {output_name}: {res.stderr[:300]}")
            return False
    except Exception as e:
        print(f"Exception for {output_name}: {e}")
        return False

if __name__ == "__main__":
    download_clip("Lamine Yamal goal vs France Euro 2024 4k short", "yamal_euro_goal")
    download_clip("Harry Kane Bayern Munich goal celebration 4k short", "kane_bayern_goal")
    download_clip("Lamine Yamal skills barcelona 4k short", "yamal_skills")
    download_clip("Harry Kane UCL goal celebration short", "kane_ucl_clutch")
