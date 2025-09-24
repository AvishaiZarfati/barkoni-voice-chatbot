#!/usr/bin/env python3
"""
Simple Data Collection Script for Barkoni Voice Cloning
Downloads audio from Barkuni's YouTube channel without conversion
"""

import yt_dlp
import os
from pathlib import Path

def download_barkuni_audio_simple(output_dir, max_videos=None):
    """Download audio from Barkuni's channel without FFmpeg conversion"""

    # Simple download options - no conversion
    ydl_opts = {
        'format': 'bestaudio',  # Download best audio quality available
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'noplaylist': False,  # Allow playlist downloads
    }

    if max_videos:
        ydl_opts['max_downloads'] = max_videos

    channel_url = "https://youtube.com/@barkuni"

    if max_videos:
        print(f"Downloading {max_videos} audio files from: {channel_url}")
    else:
        print(f"Downloading ALL audio files from: {channel_url}")
    print("Note: Files will be in original format (webm/m4a), not converted to WAV")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([channel_url])
        print("[OK] Download completed successfully!")
        print(f"Files saved to: {output_dir}")

    except Exception as e:
        print(f"[ERROR] Download error: {e}")

def list_downloaded_files(directory):
    """List all downloaded audio files"""
    audio_files = []
    for file in Path(directory).glob("*"):
        if file.suffix.lower() in ['.webm', '.m4a', '.mp3', '.wav']:
            audio_files.append(file)

    if audio_files:
        print(f"\nFound {len(audio_files)} audio files:")
        for i, file in enumerate(audio_files, 1):
            print(f"  {i}. {file.name}")
    else:
        print("\n[WARN] No audio files found")

    return audio_files

def main():
    """Main collection function"""
    print("Simple Barkuni Audio Collection")
    print("=" * 40)

    # Setup output directory
    output_dir = Path("data/raw_audio")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Ask user how many files to download
    try:
        choice = input("Download all 49 videos? (y/n, default=n): ").strip().lower()
        if choice == 'y':
            download_barkuni_audio_simple(output_dir)  # Download all
        else:
            download_barkuni_audio_simple(output_dir, max_videos=5)  # Download 5 for testing
    except (EOFError, KeyboardInterrupt):
        download_barkuni_audio_simple(output_dir, max_videos=5)  # Default to 5

    # List what we got
    audio_files = list_downloaded_files(output_dir)

    if audio_files:
        print(f"\nYou can now use these files in the GUI:")
        print(f"   Browse to: {output_dir.absolute()}")
        print(f"   Select any of the downloaded files")
        print(f"\nNote: For voice cloning, you'll need to convert to WAV format later")
    else:
        print(f"\n[ERROR] No files downloaded. Check your internet connection.")

if __name__ == "__main__":
    main()