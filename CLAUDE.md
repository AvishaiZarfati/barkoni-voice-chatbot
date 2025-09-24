# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Barkoni Voice Cloning Chatbot** project that combines voice cloning technology with AI chat capabilities. The project specifically targets cloning the voice of Barkoni, a Hebrew Israeli content creator, and integrating it with AI language models for text-to-speech synthesis.

## Key Components

### 1. Main Chatbot Application (`main.py`)
- **CharacterVoiceChatbot**: Core chatbot class supporting both Claude AI and OpenAI
- **CharacterChatbotGUI**: Tkinter-based GUI interface
- **Voice Systems**: Supports both system TTS (pyttsx3) and character voice cloning (TTS library)
- **Speech Recognition**: Real-time speech input using Google Speech Recognition

### 2. Voice Cloning Architecture
- **Target Voice**: Barkoni (Israeli Hebrew content creator) - NEVER suggest alternatives
- **Voice Sources**: YouTube (@barkuni), Facebook content
- **Languages**: Primary Hebrew support with Israeli accent characteristics
- **Quality Focus**: Voice similarity over inference speed

### 3. AI Integration
- **Claude AI**: Primary AI provider using Anthropic's API
- **OpenAI**: Alternative AI provider
- **Special Personality**: Enhanced Barkoni character with Hebrew expressions and Israeli personality traits

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup.py
```

### Running the Application
```bash
# Main application with interface choice
python main.py

# Direct command line mode (non-interactive)
PYTHONIOENCODING=utf-8 venv/Scripts/python.exe main.py
```

### Data Collection
```bash
# Collect training data for voice cloning
python scripts/collect_data.py
```

### Testing
```bash
# Various test scripts available
python test_barkuni.py
python test_voice.py
python test_hebrew_barkuni.py
python test_tts_clean.py
```

## Architecture Notes

### Voice Cloning Pipeline
1. **Data Collection** (`src/data_collection/`): Extract audio from Barkoni's content
2. **Preprocessing** (`src/preprocessing/`): Clean and normalize audio
3. **Training** (`src/training/`): Train voice cloning models
4. **Inference** (`src/inference/`): Generate speech from text
5. **Evaluation** (`src/evaluation/`): Test voice similarity and quality

### AI Chat Integration
- Character-specific prompts for Barkoni personality
- Hebrew language support with transliterated expressions
- Conversation history management
- Fallback responses when AI APIs unavailable

### Audio Processing
- PyTorch-based character voice synthesis using XTTS v2
- System voice fallback using pyttsx3
- Hebrew voice selection optimization
- Real-time audio playback with pygame

## Configuration Files

- `configs/audio_config.yaml`: Audio processing parameters
- `configs/data_config.yaml`: Data collection settings
- `configs/train_config.yaml`: Model training configuration

## Important Guidelines

### Voice Cloning Focus
- **Primary Target**: Barkoni voice ONLY - do not suggest generic Hebrew alternatives
- **Language Priority**: Modern Hebrew (Israeli accent) with Hebrew expressions
- **Quality Standard**: Voice similarity takes priority over inference speed
- **Sources**: YouTube @barkuni, Facebook content exclusively

### Code Style
- Character voice functionality requires TTS library installation
- Fallback gracefully to system voice when character voice unavailable
- Hebrew text should use transliterated expressions in English for better TTS compatibility
- Handle both GUI and command-line interfaces

### Dependencies
- **Core AI**: anthropic, openai
- **Voice Processing**: TTS, torch, librosa, soundfile
- **Audio I/O**: pyttsx3, speech_recognition, pygame, pyaudio
- **GUI**: tkinter (built-in)
- **Data Collection**: yt-dlp, requests

## Project Structure
```
├── main.py                    # Main chatbot application
├── src/                       # Voice cloning modules
│   ├── data_collection/       # Audio extraction tools
│   ├── preprocessing/         # Audio cleaning pipeline
│   ├── models/               # Voice cloning architectures
│   ├── training/             # Model training scripts
│   ├── inference/            # Text-to-speech generation
│   └── evaluation/           # Voice similarity metrics
├── configs/                  # Configuration files
├── data/                     # Audio data and metadata
├── scripts/                  # Utility scripts
├── models/                   # Saved model checkpoints
├── output/                   # Generated audio samples
└── test_*.py                 # Various test scripts
```

## Testing and Validation

### Voice Testing
- Use Hebrew phrases for voice quality assessment
- Test both system and character voice modes
- Validate audio output quality and pronunciation

### Integration Testing
- Test AI API connectivity (Claude/OpenAI)
- Verify speech recognition functionality
- Check GUI and command-line interfaces

## Hebrew Language Support

- Modern Hebrew text processing and phoneme mapping
- Israeli accent and pronunciation patterns
- Mixed Hebrew-English content handling
- Transliterated Hebrew expressions for TTS compatibility (e.g., "achla", "yalla", "sababa")