import urllib.request
import re
import json

ids = [
    '7687916592478375200',
    '7677965539834121505',
    '7683543150731873568',
    '7687800476473101588',
    '7699193882415762710'
]

for vid in ids:
    url = f'https://www.tiktok.com/player/v1/{vid}?embed_from=oembed&music_info=1&description=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            content = r.read().decode('utf-8', errors='ignore')
            title_m = re.search(r'<title>(.*?)</title>', content)
            print(f'=== Video {vid} ===')
            print('Title:', title_m.group(1) if title_m else 'None')
            caps = re.findall(r'"desc":"([^"]*)"', content)
            if caps:
                print('Caption:', caps[0])
            music = re.findall(r'"music":\{.*?"title":"([^"]*)".*?"authorName":"([^"]*)"', content)
            if music:
                print('Music:', music[0])
            # search for hashtags
            tags = re.findall(r'#\w+', content)
            if tags:
                print('Tags:', list(set(tags))[:8])
    except Exception as e:
        print(f'Error for {vid}: {e}')
