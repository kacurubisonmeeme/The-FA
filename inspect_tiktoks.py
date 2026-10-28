import urllib.request
import re
import json

urls = [
    'https://www.tiktok.com/@mgg7x_/video/7687800476473101588',
    'https://www.tiktok.com/@kenniyofficial064/video/7699193882415762710',
    'https://www.tiktok.com/@psv/video/7683543150731873568',
    'https://www.tiktok.com/@championsleague/video/7687916592478375200',
    'https://www.tiktok.com/@championsleague/video/7677965539834121505'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            title = re.search(r'<title>(.*?)</title>', html)
            desc = re.search(r'<meta name="description" content="([^"]*)"', html)
            print('URL:', u)
            print('  Title:', title.group(1) if title else 'No title')
            print('  Desc:', desc.group(1) if desc else 'No desc')
    except Exception as e:
        print('URL:', u, 'Error:', e)
