#!/usr/bin/env python3
"""
Barkoni Voice Cloning Project Setup Script
Automated setup for voice cloning development environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """Execute shell command with error handling"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def create_project_structure():
    """Create project directory structure"""
    directories = [
        "data/raw_audio",
        "data/processed_audio", 
        "data/metadata",
        "src/data_collection",
        "src/preprocessing", 
        "src/models",
        "src/training",
        "src/inference",
        "src/evaluation",
        "models/checkpoints",
        "models/final",
        "output/samples",
        "output/evaluation",
        "configs",
        "scripts",
        "notebooks",
        "tests",
        "logs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

def setup_environment():
    """Setup Python environment and dependencies"""
    print("Setting up Python environment...")
    
    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        run_command(f"{sys.executable} -m venv venv")
    
    # Determine activation script based on OS
    if sys.platform == "win32":
        activate_script = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_script = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install requirements
    if Path("requirements.txt").exists():
        run_command(f"{pip_cmd} install -r requirements.txt")
    
    # Install espeak-ng for Hebrew phonemes (system level)
    print("Installing espeak-ng for Hebrew support...")
    if sys.platform == "linux":
        run_command("sudo apt-get update && sudo apt-get install -y espeak-ng", check=False)
    elif sys.platform == "darwin":  # macOS
        run_command("brew install espeak", check=False)
    elif sys.platform == "win32":
        print("Please install espeak-ng manually from: https://github.com/espeak-ng/espeak-ng/releases")

def create_config_files():
    """Create initial configuration files"""
    
    # Audio processing config
    audio_config = """# Audio Processing Configuration
sample_rate: 22050
hop_length: 256
win_length: 1024
n_fft: 1024
n_mels: 80
fmin: 0
fmax: 8000

# Voice cloning specific
target_voice: "barkoni"
language: "he"  # Hebrew
"""
    
    with open("configs/audio_config.yaml", "w", encoding="utf-8") as f:
        f.write(audio_config)
    
    # Data collection config
    data_config = """# Data Collection Configuration
sources:
  youtube:
    channel: "@barkuni"
    quality: "best"
    format: "wav"
  facebook:
    url: "https://www.facebook.com/share/1BZjwBhDhT/"
    
output:
  raw_audio_dir: "data/raw_audio"
  segment_length: 10  # seconds
  min_segment_length: 3
  
preprocessing:
  noise_reduction: true
  normalize_volume: true
  remove_silence: true
  sample_rate: 22050
"""
    
    with open("configs/data_config.yaml", "w", encoding="utf-8") as f:
        f.write(data_config)
    
    # Training config
    train_config = """# Training Configuration
model:
  type: "rvc"  # or "sovits", "bark", "tortoise"
  
training:
  batch_size: 8
  learning_rate: 0.0001
  epochs: 100
  save_interval: 10
  
data:
  train_ratio: 0.8
  val_ratio: 0.2
  
hebrew:
  phoneme_model: "espeak-ng"
  text_normalization: true
"""
    
    with open("configs/train_config.yaml", "w", encoding="utf-8") as f:
        f.write(train_config)

def create_initial_scripts():
    """Create initial utility scripts"""
    
    # Data collection script template
    collect_script = '''#!/usr/bin/env python3
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
'''
    
    with open("scripts/collect_data.py", "w", encoding="utf-8") as f:
        f.write(collect_script)
    
    # Make script executable
    if sys.platform != "win32":
        os.chmod("scripts/collect_data.py", 0o755)

def main():
    """Main setup function"""
    print("🎤 Setting up Barkoni Voice Cloning Project")
    print("=" * 50)
    
    # Create project structure
    print("\n📁 Creating project directories...")
    create_project_structure()
    
    # Setup environment
    print("\n🐍 Setting up Python environment...")
    setup_environment()
    
    # Create config files
    print("\n⚙️  Creating configuration files...")
    create_config_files()
    
    # Create initial scripts
    print("\n📝 Creating utility scripts...")
    create_initial_scripts()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Activate virtual environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
    print("2. Run data collection: python scripts/collect_data.py")
    print("3. Check PROJECT_CONTEXT.md for detailed workflow")
    print("4. Follow the .cursorrules for development guidelines")

if __name__ == "__main__":
    main()
