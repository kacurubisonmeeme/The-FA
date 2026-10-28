import os
import glob

files = glob.glob("assets/raw_footage/*")
for f in sorted(files):
    size = os.path.getsize(f)
    print(f"{f}: {size / 1024 / 1024:.2f} MB")
