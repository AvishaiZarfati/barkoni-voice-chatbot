# Barkoni Voice Cloning Project

## Mission Statement
Transform any LLM text output into speech that sounds like Barkoni, a Hebrew Israeli content creator, maintaining authentic vocal characteristics, accent, and speaking patterns.

## Target Voice Profile: Barkoni
- **Language**: Hebrew (Modern Israeli)
- **Source**: YouTube: @barkuni, Facebook content
- **Characteristics**: Israeli Hebrew accent, content creator speaking style
- **Content Type**: Likely commentary, educational, or entertainment content
- **Voice Traits**: (To be analyzed from source material)

## Project Architecture
```
├── data_collection/          # Audio extraction from sources
├── preprocessing/           # Audio cleaning and preparation  
├── model_training/          # Voice cloning model training
├── inference/              # Text-to-speech generation
├── evaluation/             # Voice similarity testing
└── integration/            # LLM integration layer
```

## Current Focus
1. **Phase 1**: Audio data collection from Barkoni's content
2. **Phase 2**: Voice analysis and feature extraction
3. **Phase 3**: Model training and fine-tuning
4. **Phase 4**: LLM integration for real-time synthesis

## Technical Stack
- **Voice Cloning**: RVC, SoVITS-SVC, or Bark
- **Audio Processing**: librosa, PyTorch Audio
- **Hebrew TTS**: espeak-ng, Festival (Hebrew support)
- **ML Framework**: PyTorch or TensorFlow
- **Audio Format**: WAV, MP3 support
- **Language**: Python 3.8+

## Off Limits
- ❌ Generic Hebrew voices or alternatives to Barkoni
- ❌ Major architecture changes without performance justification
- ❌ Non-Hebrew language support (unless specifically requested)
- ❌ Real-time constraints that compromise voice quality
- ❌ Suggesting different voice cloning targets

## Success Metrics
- Voice similarity score > 85% (subjective/objective measures)
- Natural Hebrew pronunciation and intonation
- Consistent quality across different text inputs
- Reasonable inference time for content creation use
- Stable integration with LLM text generation

## Data Sources
- YouTube: https://youtube.com/@barkuni
- Facebook: https://www.facebook.com/share/1BZjwBhDhT/
- Additional Hebrew content as needed for training

## Hebrew Language Requirements
- Support Modern Hebrew text input
- Handle Hebrew punctuation and formatting
- Proper phoneme mapping for Hebrew sounds
- Support for Hebrew-specific vocal characteristics
- Mixed script handling (Hebrew + English/numbers)

## Legal & Ethical Considerations
- Voice cloning for personal/educational use
- Respect content creator's rights
- No malicious deepfake applications
- Clear attribution when sharing results