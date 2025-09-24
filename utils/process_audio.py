#!/usr/bin/env python3
"""
Audio Processing Script for Barkuni Voice Cloning
Converts webm to wav, cleans audio, and segments for training
"""

import os
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_webm_to_wav(input_path, output_path):
    """Convert webm file to wav format"""
    try:
        # Use pydub to convert
        audio = AudioSegment.from_file(input_path, format="webm")
        audio = audio.set_frame_rate(22050)  # Standard rate for voice cloning
        audio = audio.set_channels(1)  # Mono
        audio.export(output_path, format="wav")
        logging.info(f"Converted: {input_path.name} -> {output_path.name}")
        return True
    except Exception as e:
        logging.error(f"Error converting {input_path}: {e}")
        return False

def clean_audio(audio_path, output_path):
    """Clean audio: noise reduction and normalization"""
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=22050)

        # Noise reduction (simple approach)
        # Remove very quiet parts (likely noise)
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)

        # Normalize volume
        y_normalized = librosa.util.normalize(y_trimmed)

        # Save cleaned audio
        sf.write(output_path, y_normalized, sr)
        logging.info(f"Cleaned: {audio_path.name}")
        return True
    except Exception as e:
        logging.error(f"Error cleaning {audio_path}: {e}")
        return False

def segment_audio(audio_path, output_dir, min_length=3000, max_length=10000):
    """Split audio into segments based on silence"""
    try:
        # Load with pydub
        audio = AudioSegment.from_wav(audio_path)

        # Split on silence
        segments = split_on_silence(
            audio,
            min_silence_len=500,    # 0.5 seconds of silence
            silence_thresh=audio.dBFS - 16,  # Adjust threshold
            keep_silence=200        # Keep 0.2s of silence
        )

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        valid_segments = 0
        base_name = audio_path.stem

        for i, segment in enumerate(segments):
            # Filter by length
            if min_length <= len(segment) <= max_length:
                segment_path = output_dir / f"{base_name}_seg_{i:03d}.wav"
                segment.export(segment_path, format="wav")
                valid_segments += 1

        logging.info(f"Created {valid_segments} segments from {audio_path.name}")
        return valid_segments
    except Exception as e:
        logging.error(f"Error segmenting {audio_path}: {e}")
        return 0

def process_all_audio():
    """Process all raw audio files"""
    raw_dir = Path("data/raw_audio")
    processed_dir = Path("data/processed_audio")
    segments_dir = Path("data/processed_audio/segments")

    processed_dir.mkdir(exist_ok=True)
    segments_dir.mkdir(exist_ok=True)

    print("Processing Barkuni Audio Files")
    print("=" * 40)

    # Find all webm files
    webm_files = list(raw_dir.glob("*.webm"))
    print(f"Found {len(webm_files)} audio files to process")

    total_segments = 0
    processed_count = 0

    for webm_file in webm_files:
        try:
            print(f"\nProcessing: {webm_file.name}")

            # Step 1: Convert to WAV
            wav_file = processed_dir / f"{webm_file.stem}.wav"
            if convert_webm_to_wav(webm_file, wav_file):

                # Step 2: Clean audio
                clean_file = processed_dir / f"{webm_file.stem}_clean.wav"
                if clean_audio(wav_file, clean_file):

                    # Step 3: Segment audio
                    segments = segment_audio(clean_file, segments_dir)
                    total_segments += segments
                    processed_count += 1

                    # Clean up intermediate files
                    wav_file.unlink()  # Remove intermediate WAV

        except Exception as e:
            logging.error(f"Failed to process {webm_file}: {e}")

    print(f"\n" + "=" * 40)
    print(f"Processing Complete!")
    print(f"Files processed: {processed_count}/{len(webm_files)}")
    print(f"Total segments created: {total_segments}")
    print(f"Clean audio: {processed_dir}")
    print(f"Training segments: {segments_dir}")

    return processed_count, total_segments

def check_audio_quality(segments_dir):
    """Check quality of processed segments"""
    segments_dir = Path(segments_dir)
    segments = list(segments_dir.glob("*.wav"))

    if not segments:
        print("No segments found to analyze")
        return

    print(f"\nAudio Quality Analysis")
    print("-" * 30)

    durations = []
    for segment in segments[:10]:  # Sample first 10
        try:
            y, sr = librosa.load(segment)
            duration = len(y) / sr
            durations.append(duration)
        except:
            continue

    if durations:
        avg_duration = np.mean(durations)
        print(f"Sample segments: {len(durations)}")
        print(f"Average duration: {avg_duration:.2f} seconds")
        print(f"Sample rate: 22050 Hz")
        print(f"Format: WAV (mono)")

        # Quality recommendations
        if avg_duration < 2:
            print("WARNING: Segments may be too short for training")
        elif avg_duration > 15:
            print("WARNING: Segments may be too long")
        else:
            print("SUCCESS: Good segment length for training")

def main():
    """Main processing function"""
    print("Barkuni Audio Processing Pipeline")
    print("This will convert, clean, and segment all raw audio")
    print("=" * 50)

    # Check if we have raw audio
    raw_dir = Path("data/raw_audio")
    if not raw_dir.exists() or not list(raw_dir.glob("*.webm")):
        print("ERROR: No raw audio files found in data/raw_audio/")
        print("Please run the data collection script first")
        return

    # Process all audio
    processed, segments = process_all_audio()

    if segments > 0:
        # Analyze quality
        check_audio_quality("data/processed_audio/segments")

        print(f"\nReady for Voice Training!")
        print(f"Use segments in: data/processed_audio/segments/")
    else:
        print("\nProcessing failed - no segments created")

if __name__ == "__main__":
    main()