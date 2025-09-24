#!/usr/bin/env python3
"""
Data Collection Script for Barkoni Voice Cloning
Downloads and preprocesses audio from specified sources
"""

import yt_dlp
import os
from pathlib import Path

def download_youtube_audio(channel_url, output_dir):
    """Download audio from YouTube channel"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])

if __name__ == "__main__":
    output_dir = Path("data/raw_audio")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Download from Barkoni's channel
    channel_url = "https://youtube.com/@barkuni"
    print(f"Downloading audio from: {channel_url}")
    download_youtube_audio(channel_url, output_dir)
