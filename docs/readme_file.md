# 🎤 Barkoni Voice Cloning Project

Clone the voice of Barkoni, a Hebrew Israeli content creator, for LLM text-to-speech synthesis.

## 🎯 Mission
Transform any LLM text output into speech that authentically replicates Barkoni's voice, maintaining Hebrew accent, speaking patterns, and vocal characteristics.

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   python setup.py
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Collect Training Data**
   ```bash
   python scripts/collect_data.py
   ```

3. **Start Development**
   - Follow `.cursorrules` for AI assistant guidelines
   - Check `PROJECT_CONTEXT.md` for detailed architecture
   - Use `configs/` files for model parameters

## 📁 Project Structure

```
├── .cursorrules              # AI assistant rules (IMPORTANT!)
├── PROJECT_CONTEXT.md        # Detailed project context
├── setup.py                  # Automated setup script
├── requirements.txt          # Python dependencies
├── data/
│   ├── raw_audio/           # Original Barkoni audio files
│   ├── processed_audio/     # Cleaned and segmented audio
│   └── metadata/            # Audio annotations and labels
├── src/
│   ├── data_collection/     # Audio extraction tools
│   ├── preprocessing/       # Audio cleaning pipeline
│   ├── models/             # Voice cloning architectures
│   ├── training/           # Model training scripts
│   ├── inference/          # Text-to-speech generation
│   └── evaluation/         # Voice similarity metrics
├── configs/                # Configuration files
├── scripts/               # Utility scripts
├── models/               # Saved model checkpoints
└── output/              # Generated audio samples
```

## 🎯 Target Voice: Barkoni

**Sources:**
- YouTube: [@barkuni](https://youtube.com/@barkuni)
- Facebook: [Profile Link](https://www.facebook.com/share/1BZjwBhDhT/)

**Characteristics:**
- Native Hebrew speaker (Israeli accent)
- Content creator speaking style
- Modern Hebrew pronunciation patterns
- Authentic Israeli vocal characteristics

## 🔧 Technical Approach

### Voice Cloning Options:
1. **RVC (Retrieval-based Voice Conversion)** - Real-time capable
2. **SoVITS-SVC** - High quality synthesis
3. **Bark** - Advanced neural voice cloning
4. **TortoiseTTS** - Flexible and controllable

### Hebrew Language Support:
- Modern Hebrew text processing
- Hebrew phoneme mapping via espeak-ng
- Support for Hebrew grammatical patterns
- Mixed Hebrew-English content handling

## 🎮 Usage Example

```python
from src.inference import BarkoniVoiceCloner

# Initialize voice cloner
cloner = BarkoniVoiceCloner(model_path="models/final/barkoni_model.pt")

# Hebrew text input
hebrew_text = "שלום, איך הולך? היום נדבר על טכנולוגיה חדשנית"

# Generate Barkoni-style speech
audio = cloner.synthesize(hebrew_text, language="he")
cloner.save_audio(audio, "output/barkoni_sample.wav")
```

## 📊 Success Metrics

- **Voice Similarity**: >85% subjective similarity to Barkoni
- **Hebrew Pronunciation**: Natural Israeli accent and intonation
- **Consistency**: Stable quality across different texts
- **Performance**: Reasonable inference time for content creation
- **Integration**: Seamless LLM text-to-speech pipeline

## ⚠️ Important Guidelines

### For AI Assistants (Claude/Cursor):
- **READ `.cursorrules` FIRST** - Contains critical project guidelines
- Stay focused on Barkoni voice specifically (no alternatives)
- Prioritize Hebrew language requirements
- Maintain voice cloning quality over speed
- Follow the established project architecture

### Development Rules:
- **Target Voice**: Barkoni ONLY - no generic Hebrew alternatives
- **Language**: Hebrew (Modern Israeli) primary focus  
- **Quality**: Voice similarity takes priority over inference speed
- **Scope**: Voice cloning, audio processing, TTS integration only

## 🔒 Legal & Ethics

- For personal/educational use only
- Respect content creator rights
- No malicious deepfake applications
- Clear attribution when sharing results
- Follow platform terms of service

## 🛠️ Development Workflow

1. **Data Collection** → Extract clean audio from sources
2. **Preprocessing** → Clean, normalize, and segment audio
3. **Analysis** → Extract Barkoni's vocal characteristics
4. **Training** → Train voice cloning model
5. **Evaluation** → Test voice similarity and quality
6. **Integration** → Connect with LLM text generation
7. **Optimization** → Improve quality and performance

## 📞 Getting Help

- Check `PROJECT_CONTEXT.md` for detailed information
- Review configuration files in `configs/`
- Follow the `.cursorrules` when using AI assistants
- Test with sample Hebrew phrases for evaluation

---

**Remember**: The goal is authentic Barkoni voice synthesis for Hebrew text. Stay focused on this specific target! 🎯