#!/usr/bin/env python3
"""
Download ALL Barkuni audio files (49 videos)
"""

import yt_dlp
from pathlib import Path

def download_all_barkuni():
    """Download all 49 Barkuni videos"""

    output_dir = Path("data/raw_audio")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Download options - no conversion, no limits
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'noplaylist': False,
        'ignoreerrors': True,  # Skip problematic videos
    }

    channel_url = "https://youtube.com/@barkuni"

    print("Downloading ALL 49 Barkuni audio files...")
    print("This may take 10-20 minutes depending on your connection")
    print("Files will be in original format (webm/m4a)")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([channel_url])
        print("\n[OK] All downloads completed!")

    except Exception as e:
        print(f"\n[ERROR] Download error: {e}")
        print("Some files may have been downloaded successfully")

    # Count final files
    audio_files = list(output_dir.glob("*.webm")) + list(output_dir.glob("*.m4a"))
    print(f"\nTotal audio files: {len(audio_files)}")
    print(f"Location: {output_dir.absolute()}")

if __name__ == "__main__":
    download_all_barkuni()