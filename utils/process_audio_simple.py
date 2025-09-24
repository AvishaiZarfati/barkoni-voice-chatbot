#!/usr/bin/env python3
"""
Simple Audio Processing for Barkuni Voice Cloning
Processes webm files without FFmpeg dependency
"""

import os
import shutil
from pathlib import Path
import hashlib

def rename_files_to_ascii():
    """Rename Hebrew filename files to ASCII for processing"""

    raw_dir = Path("data/raw_audio")
    renamed_files = {}

    print("Renaming Hebrew files to ASCII...")

    for webm_file in raw_dir.glob("*.webm"):
        # Create a hash-based name
        original_name = webm_file.name
        hash_name = hashlib.md5(original_name.encode('utf-8')).hexdigest()
        new_name = f"barkuni_{hash_name}.webm"
        new_path = raw_dir / new_name

        try:
            # Copy file with new name
            shutil.copy2(webm_file, new_path)
            renamed_files[new_path] = original_name
            print(f"Renamed: [Hebrew filename] -> {new_name}")
        except Exception as e:
            print(f"Error renaming file: {e}")

    return renamed_files

def create_file_list():
    """Create a list of all renamed audio files for GUI use"""

    raw_dir = Path("data/raw_audio")
    renamed_files = list(raw_dir.glob("barkuni_*.webm"))

    # Create a simple list file
    list_file = raw_dir / "barkuni_files.txt"
    with open(list_file, 'w', encoding='utf-8') as f:
        for file_path in renamed_files:
            f.write(f"{file_path.name}\n")

    print(f"Created file list: {list_file}")
    print(f"Total files: {len(renamed_files)}")

    return renamed_files

def main():
    """Main processing function"""
    print("Simple Barkuni Audio Processing")
    print("Converting Hebrew filenames to ASCII for GUI compatibility")
    print("=" * 60)

    # Check if we have raw audio
    raw_dir = Path("data/raw_audio")
    if not raw_dir.exists():
        print("ERROR: data/raw_audio directory not found")
        return

    original_files = list(raw_dir.glob("*.webm"))
    if not original_files:
        print("ERROR: No webm files found in data/raw_audio/")
        return

    print(f"Found {len(original_files)} webm files")

    # Rename files to ASCII
    renamed_files = rename_files_to_ascii()

    # Create file list
    processed_files = create_file_list()

    print(f"\n" + "=" * 60)
    print("Processing Complete!")
    print(f"Original files: {len(original_files)}")
    print(f"Renamed files: {len(renamed_files)}")
    print(f"Ready for GUI: {len(processed_files)}")

    print(f"\nFor GUI Testing:")
    print(f"1. Run: python main.py")
    print(f"2. Choose GUI mode (1)")
    print(f"3. Browse to: {raw_dir.absolute()}")
    print(f"4. Select any 'barkuni_*.webm' file")
    print(f"5. These contain authentic Barkuni voice!")

    print(f"\nNote: Files are in original webm format")
    print(f"      Perfect for testing voice cloning interface")
    print(f"      For production training, convert to WAV later")

if __name__ == "__main__":
    main()