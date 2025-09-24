# Barkoni Voice Cloning Chatbot

A voice cloning chatbot that combines AI chat capabilities with voice synthesis, specifically targeting the voice of Barkoni, a Hebrew Israeli content creator. This project integrates modern AI technology with authentic Hebrew language support and Israeli accent characteristics.

## Features

### 🎭 AI Integration
- **Claude AI** (Primary) - Enhanced Barkoni personality with Hebrew expressions
- **OpenAI** (Alternative) - Fallback AI provider
- Real-time conversation with authentic Barkoni character traits
- Hebrew-English mixed responses with Israeli slang

### 🎤 Voice Technology
- **Voice Cloning** using TTS library with XTTS v2 model
- **System TTS** fallback with Hebrew accent simulation
- Real-time text-to-speech synthesis
- Support for Hebrew pronunciation with Israeli accent
- 60+ authentic Barkoni voice samples for training

### 🎮 User Interface
- **GUI Interface** - User-friendly Tkinter-based chat window
- **Command Line** - Direct terminal interaction
- **Speech Recognition** - Real-time voice input using Google Speech Recognition
- **Audio Playback** - High-quality audio output with pygame

### 🇮🇱 Hebrew Language Support
- Modern Hebrew text processing
- Israeli accent and pronunciation patterns
- Mixed Hebrew-English content handling
- Authentic Israeli expressions: "achla", "yalla", "sababa", "eizeh kef"

## Installation

### Prerequisites
- Python 3.8+ (Python 3.11 recommended for voice cloning)
- Windows/Linux/macOS support
- Microphone (for speech input)
- Speakers/Headphones (for audio output)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/AvishaiZarfati/barkoni-voice-chatbot.git
cd barkoni-voice-chatbot
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
```

5. **Run setup script:**
```bash
python setup.py
```

## Usage

### Quick Start
```bash
python main.py
```

### Command Line Options
```bash
# GUI mode (default)
python main.py

# Command line mode
python main.py --cli

# Voice cloning test
python test_barkoni_voice_cloning.py

# Hebrew language test
python test_hebrew_barkuni.py
```

### Configuration Options
- **AI Provider**: Choose between Claude AI or OpenAI
- **Voice Mode**: System TTS or character voice cloning
- **Language**: Hebrew-English mixed responses
- **Interface**: GUI or command-line interaction

## Project Structure

```
├── main.py                    # Main chatbot application
├── run_tests.py              # Comprehensive test runner
├── src/                       # Voice cloning modules
│   ├── data_collection/       # Audio extraction tools
│   ├── preprocessing/         # Audio cleaning pipeline
│   ├── models/               # Voice cloning architectures
│   ├── training/             # Model training scripts
│   ├── inference/            # Text-to-speech generation
│   └── evaluation/           # Voice similarity metrics
├── tests/                    # Organized test suite
│   ├── unit/                 # Individual component tests
│   ├── integration/          # Full system tests
│   ├── voice/               # Voice synthesis tests
│   └── personality/         # Character behavior tests
├── configs/                  # Configuration files
│   ├── audio_config.yaml    # Audio processing settings
│   ├── data_config.yaml     # Data collection config
│   └── train_config.yaml    # Training parameters
├── scripts/                  # Utility scripts
│   └── collect_data.py      # Data collection automation
├── utils/                   # Utility functions and tools
├── docs/                    # Documentation and guides
├── examples/                # Example usage scripts
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Voice Cloning Pipeline

### 1. Data Collection
- Extract audio from Barkoni's YouTube content (@barkuni)
- Process Facebook video content
- Clean and normalize audio samples
- Generate training dataset

### 2. Training
- Use XTTS v2 model for voice synthesis
- Train on Hebrew-English mixed content
- Optimize for Israeli accent characteristics
- Fine-tune voice similarity parameters

### 3. Inference
- Real-time text-to-speech generation
- Hebrew pronunciation optimization
- Character voice integration
- Audio quality enhancement

## Testing

### Comprehensive Test Suite
```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py voice
python run_tests.py personality
python run_tests.py integration
python run_tests.py unit

# List available tests
python run_tests.py --list
```

### Individual Test Categories

**Voice Testing:**
```bash
# Comprehensive voice tests
python tests/voice/test_barkuni_voice_comprehensive.py

# Voice cloning tests (requires Python 3.11)
python tests/voice/test_barkoni_voice_cloning.py

# Microphone and audio tests
python tests/voice/test_microphone.py
```

**Personality & Hebrew Testing:**
```bash
# Hebrew language and character validation
python tests/personality/test_barkuni_hebrew_character.py

# Deep personality analysis
python tests/personality/test_barkuni_personality_deep.py
```

**Integration Testing:**
```bash
# Full system integration
python tests/integration/test_current_barkoni.py

# API integration tests
python tests/integration/test_with_api.py
```

## Configuration

### Audio Settings (`configs/audio_config.yaml`)
```yaml
sample_rate: 22050
channels: 1
bit_depth: 16
format: wav
```

### Training Settings (`configs/train_config.yaml`)
```yaml
model: xtts_v2
language: he-IL
batch_size: 8
learning_rate: 0.0001
epochs: 100
```

## Dependencies

### Core Libraries
- `anthropic` - Claude AI integration
- `openai` - OpenAI API support
- `TTS` - Voice cloning library
- `torch` - Machine learning framework
- `librosa` - Audio processing
- `soundfile` - Audio I/O

### Audio Processing
- `pyttsx3` - System text-to-speech
- `speech_recognition` - Voice input
- `pygame` - Audio playback
- `pyaudio` - Microphone access

### Interface
- `tkinter` - GUI framework (built-in)
- `python-dotenv` - Environment variables

## Troubleshooting

### Common Issues

**Voice cloning not working:**
- Ensure Python 3.11 is installed
- Install TTS library: `pip install TTS torch`
- Check CUDA availability for GPU acceleration

**Hebrew pronunciation issues:**
- Verify system Hebrew language support
- Check audio output device settings
- Test with different TTS voices

**API connection errors:**
- Verify API keys in `.env` file
- Check internet connection
- Ensure API quotas are not exceeded

**Microphone not working:**
- Check microphone permissions
- Test with `python test_microphone.py`
- Verify audio input device settings

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- **Barkoni** (@barkuni) - Original voice and personality inspiration
- **Anthropic** - Claude AI integration
- **Coqui AI** - TTS voice cloning technology
- **Hebrew Language Community** - Language support and feedback

## Disclaimer

This project is for educational and entertainment purposes. All voice samples and content are used with respect to the original creator's work. This is a fan project and not officially affiliated with Barkoni.

---

**Made with ❤️ for the Hebrew-speaking gaming community**