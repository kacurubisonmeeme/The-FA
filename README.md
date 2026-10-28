# The FA - Automated Football Short-Form Video Pipeline

A Python and FFmpeg-driven video processing and rendering pipeline designed for automated production of high-engagement, short-form football compilations (TikTok, Instagram Reels, YouTube Shorts).

## 🚀 Overview

This repository contains automated pipelines for downloading raw football footage and audio, inspecting clips, generating custom typography hook overlays, and compiling vertical (9:16, 1080x1920) beat-matched edits.

### Key Features
- **Dynamic Typography & Hook Overlays**: Automated Pillow-based rendering of stylized typography, drop shadows, and branding overlays directly onto 1080x1920 video frames.
- **Audio Trimming & Beat Synchronization**: Automated trimming, fading, and synchronization of trending soundtracks (Viva La Vida, Memory Reboot, Montagem Diamante, Fein, After Dark, etc.).
- **Batch Video Rendering**: Modular rendering pipelines (Parts 1–5, Campaign Edits, Ballon d'Or specials, Titan compilations) with crossfades, motion effects, and color grading via FFmpeg.
- **Footage Ingestion & Inspection**: Scripts for downloading and parsing target player clips (Kane, Yamal, Mbappé, Rodri, Haaland, Vini Jr., Ronaldo, etc.) and analyzing video durations and frame rates.

## 📁 Repository Structure

- `render_part_*.py` - Core multi-part video assembly pipelines with overlay synthesis and audio stitching.
- `render_batch_*.py` - Specialized batch compilation scripts (Titans, Anthems, Trending, Fresh, etc.).
- `render_*_edit.py` - Player-specific cinematic and pace-matched edits (Haaland UCL, Vini Jr., Ronaldo, etc.).
- `download_*.py` - Downloader utilities for sourcing raw player packs, footage, and audio tracks.
- `inspect_*.py` / `check_*.py` - Diagnostic and inspection utilities for validating video streams, durations, and FFmpeg installations.

## 🛠️ Requirements

- **Python 3.10+**
- **FFmpeg**: Required for video processing and audio filtering.
- **Python Libraries**:
  - `Pillow`
  - `imageio-ffmpeg` (or system FFmpeg)

Install dependencies via:
```bash
pip install pillow imageio-ffmpeg
```

## ⚙️ Usage

### 1. Ingestion & Pre-processing
Run player download and inspection scripts to populate source material:
```bash
python download_kane_yamal_mbappe.py
python inspect_clips_ffmpeg.py
```

### 2. Rendering Short-Form Edits
Execute batch or modular render scripts:
```bash
python render_part_1.py
# or specific campaign renders
python render_ballon_dor_2026_kane.py
```

Rendered videos are saved to the `exports/` directory.

---
*Note: Large media assets (`assets/` and `exports/`) are excluded from version control.*
