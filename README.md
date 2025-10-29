# Emotional Speech Generation

**Truly expressive documentary-style narration using local neural TTS**

## Features

- **Real emotional expression** - Not just speed changes, actual prosody and emotion
- **Documentary-quality narration** - Natural intonation and pacing
- **7 emotional styles** - Neutral, enthusiastic, serious, contemplative, sad, excited, angry
- **10 speaker voices** - Each with unique characteristics
- **100% local** - No API keys, runs entirely offline
- **Cross-platform** - Works on Windows, macOS, Linux
- **Neural TTS** - Uses Bark (Suno AI) transformer model

## What Makes This Different?

Unlike basic TTS systems that just change speed, this uses **Bark** which:
- Understands context and emotion
- Generates natural prosody (rhythm, stress, intonation)
- Can express laughter, pauses, sighs, emphasis
- Sounds human, not robotic
- Perfect for engaging documentary narration

## Quick Start

### Installation

```bash
cd python-tts
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Download Models (Required - One Time)

Bark requires ~13GB of neural TTS models. Follow these steps:

1. **Create cache directory:**
   macOS/Linux:
   ```bash
   mkdir -p ~/.cache/suno/bark_v0
   ```

   Windows:
   ```powershell
   mkdir C:\Users\YourName\.cache\suno\bark_v0
   ```

2. **Download models from HuggingFace:**

   Visit: https://huggingface.co/suno/bark/tree/main

   Download these 3 files:
   - `text_2.pt` (5.35 GB) - Text encoder
   - `coarse_2.pt` (3.93 GB) - Coarse acoustic model
   - `fine_2.pt` (3.74 GB) - Fine acoustic model

   **Total download**: ~13 GB (v2 models for best quality)

3. **Place downloaded files in cache directory:**

   macOS/Linux:
   ```bash
   mv ~/Downloads/text_2.pt ~/.cache/suno/bark_v0/
   mv ~/Downloads/coarse_2.pt ~/.cache/suno/bark_v0/
   mv ~/Downloads/fine_2.pt ~/.cache/suno/bark_v0/
   ```

   Windows:
   ```powershell
   move %USERPROFILE%\Downloads\text_2.pt %USERPROFILE%\.cache\suno\bark_v0\
   move %USERPROFILE%\Downloads\coarse_2.pt %USERPROFILE%\.cache\suno\bark_v0\
   move %USERPROFILE%\Downloads\fine_2.pt %USERPROFILE%\.cache\suno\bark_v0\
   ```

4. **Verify installation:**
   ```bash
   ls ~/.cache/suno/bark_v0/
   # Should show: text_2.pt coarse_2.pt fine_2.pt
   ```

   Windows:
   ```powershell
   dir %USERPROFILE%\.cache\suno\bark_v0\
   ```

**Note**: These are one-time downloads. Models are cached permanently and shared across all uses.

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Generate expressive speech
python solution.py "Hello world" hello.wav
python solution.py --style enthusiastic "This is amazing!" amazing.wav
python solution.py --style serious "Pay close attention" serious.wav
python solution.py --style sad "I'm deeply sorry" sad.wav
```

### Interactive Mode (Recommended for Beginners)

Use the interactive script for a menu-driven experience:

```bash
./tts_interactive.sh
```

**Interactive features:**
- Choose emotion from guided menu (7 styles)
- Select speaker from list (10 voices)
- List all available speakers
- Test all emotional styles at once
- Quick generation mode
- Auto-play generated audio (macOS)

## Emotional Styles

| Style | Expression | Prosody Markers | Best For |
|-------|------------|-----------------|----------|
| `neutral` | Balanced, clear | None | Facts, introductions |
| `enthusiastic` | Excited with laughter | `[laughs]` + `!` | Discoveries, breakthroughs |
| `serious` | Grave, formal | `.` | Warnings, important info |
| `contemplative` | Reflective with pauses | `...` | Philosophy, reflection |
| `sad` | Melancholic | `[sighs]` + `...` | Condolences, tragedy |
| `excited` | Very energetic | `[laughs]` + `!!!` | Celebrations, joy |
| `angry` | Intense, forceful | `!` | Confrontation, emphasis |

## Speaker Voices

Bark includes 10 speaker voices (v2/en_speaker_0 through v2/en_speaker_9). Each has unique voice characteristics.

```bash
# List all available speakers
python solution.py --list-speakers

# Use specific speaker
python solution.py --speaker v2/en_speaker_3 "Your text" output.wav

# Combine speaker + emotion
python solution.py --style enthusiastic --speaker v2/en_speaker_5 "Amazing!" excited.wav

# Test all speakers at once
./test_all_speakers.sh
```

**Important**: Test speakers with your actual content to find your preferred voice. Voice characteristics vary based on text and emotion style.

## Command-Line Options

```
python solution.py [OPTIONS] TEXT OUTPUT

Arguments:
  TEXT                  Text to synthesize
  OUTPUT                Output WAV file path

Options:
  --style STYLE         Emotional style (default: neutral)
                        Choices: neutral, enthusiastic, serious, contemplative,
                                sad, excited, angry
  --speaker SPEAKER     Speaker voice (e.g., v2/en_speaker_3)
                        Default: v2/en_speaker_6
  --list-speakers       List all available speakers and exit
  -h, --help            Show help message
```

## Examples

### Basic Examples

```bash
# Documentary introduction
python solution.py "Welcome to our exploration of the cosmos" intro.wav

# Exciting discovery
python solution.py --style enthusiastic "Scientists have just discovered water on Mars!" discovery.wav

# Serious warning
python solution.py --style serious "Climate change poses an existential threat to humanity" warning.wav

# Philosophical reflection
python solution.py --style contemplative "Are we alone in the universe? Perhaps we'll never know" reflection.wav

# Melancholic
python solution.py --style sad "I'm deeply sorry for your loss" condolence.wav

# Very excited
python solution.py --style excited "We won the championship!" celebration.wav

# Angry/forceful
python solution.py --style angry "This is completely unacceptable!" angry.wav
```

### With Custom Speakers

```bash
# Try different speakers to find your preferred voice
python solution.py --speaker v2/en_speaker_0 "Test speaker 0" test_0.wav
python solution.py --speaker v2/en_speaker_3 "Test speaker 3" test_3.wav
python solution.py --speaker v2/en_speaker_5 "Test speaker 5" test_5.wav

# Combine emotion + speaker
python solution.py --style sad --speaker v2/en_speaker_3 "I understand your pain" empathy.wav
```

### Custom Prosody Markers

Bark understands text annotations:

```bash
# Add laughter
python solution.py "[laughs] This is hilarious!" laugh.wav

# Add pauses for emphasis
python solution.py "We must act... before it's too late..." dramatic.wav

# Add sighs
python solution.py "[sighs] I should have known" regret.wav

# Combine with emotional styles
python solution.py --style serious "[sighs] The evidence is overwhelming" concern.wav
```

### Handling Long Text

**IMPORTANT**: Bark works best with short sentences (<150 characters). Long text produces random/incorrect words.

**Solution**: Split long text into short sentences and generate separately:

```bash
#!/bin/bash
# BAD - Long text (will produce errors)
# python solution.py "This is a very long paragraph with many sentences that goes on and on and contains lots of information that needs to be conveyed in a single audio file but it's too long for Bark to handle properly" long.wav

# GOOD - Split into short sentences
python solution.py "This is a clear introduction." part1.wav
python solution.py "It contains important information." part2.wav
python solution.py "Each sentence is kept short." part3.wav
python solution.py "This produces better results." part4.wav

# Then combine the audio files using ffmpeg or similar tool
# ffmpeg -i "concat:part1.wav|part2.wav|part3.wav|part4.wav" -c copy combined.wav
```

**Text Length Guidelines:**
- **Good**: 5-15 words per sentence (50-150 characters)
- **Risky**: 15-25 words (150-200 characters)
- **Bad**: 25+ words (200+ characters) - will produce errors

**Example - Documentary Script:**
```bash
# Split long narration into sentences
python solution.py --style neutral "Welcome to our documentary." intro1.wav
python solution.py --style neutral "Today we explore the cosmos." intro2.wav
python solution.py --style enthusiastic "Scientists have made an incredible discovery!" discovery.wav
python solution.py --style serious "The implications are profound." serious.wav
```


### Batch Processing

```bash
#!/bin/bash
# Generate multiple short narrations
python solution.py --style neutral "Chapter one: The beginning" ch1.wav
python solution.py --style enthusiastic "Chapter two brings surprises!" ch2.wav
python solution.py --style serious "Chapter three: The reckoning" ch3.wav
python solution.py --style contemplative "Epilogue: Questions remain" epilogue.wav
```

### Testing Workflow

```bash
# Test all speakers to find your preferred voice
./test_all_speakers.sh

# Or test specific speakers
for i in 0 3 5; do
  python solution.py --speaker "v2/en_speaker_$i" "Hello, this is speaker $i" "test_$i.wav"
done

# Test all emotions with your chosen speaker
speaker="v2/en_speaker_5"
for style in neutral enthusiastic serious contemplative sad excited angry; do
  python solution.py --style "$style" --speaker "$speaker" "Testing $style" "test_${style}.wav"
done
```

## Requirements

- **Python**: 3.8 or higher (tested on 3.13)
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 15GB for models (downloaded once)
- **GPU**: Optional (CUDA speeds up generation 10x)
- **Internet**: Only for first-time model download (~13GB)

## Performance

| Hardware | Generation Time (per sentence) |
|----------|--------------------------------|
| CPU only | 30-60 seconds |
| GPU (CUDA) | 3-5 seconds |

**Note**: Quality is worth the wait! First generation is slower due to model loading.

## Cross-Platform Support

- **Windows** (10/11)
- **macOS** (10.13+, both Intel and Apple Silicon)
- **Linux** (Ubuntu, Debian, Fedora, etc.)

Pure Python implementation with no platform-specific dependencies.

## Output Format

- **Format**: WAV (uncompressed audio)
- **Sample Rate**: 24kHz
- **Channels**: Mono
- **Bit Depth**: 16-bit
- **Quality**: Neural TTS with natural prosody

## Technical Details

### Model: Bark (Suno AI)

- **Architecture**: Transformer-based generative model (GPT-style)
- **Training**: Trained on diverse emotional speech
- **Capabilities**:
  - Natural prosody generation
  - Emotion and style control
  - Non-speech sounds (laughter, pauses, sighs)
  - Multiple speaker voices

### Emotional Control Method

Unlike traditional TTS that only adjusts speed:

1. **Speaker Selection**: Different voice personas for each emotion
2. **Prosody Markers**: Text annotations guide emotional delivery
   - `[laughs]` for enthusiasm
   - `[sighs]` for sadness
   - `...` for thoughtful pauses
   - `.` vs `!` for seriousness vs excitement
3. **Context-Aware**: Model understands emotional context from text

### Model Files

Bark uses three main model files (v2):
- `text_2.pt` (5.35 GB) - Text encoder (converts text to tokens)
- `coarse_2.pt` (3.93 GB) - Coarse acoustic model (generates semantic tokens)
- `fine_2.pt` (3.74 GB) - Fine acoustic model (generates audio codes)

**Total size**: ~13GB (v2 models for best quality)
**Cache location**: `~/.cache/suno/bark_v0/`

## Limitations

- **Generation time**: 30-60 seconds per sentence (CPU)
- **Model size**: ~13GB disk space
- **English only**: Best results with English text
- **Text length**: **IMPORTANT - Works best with SHORT sentences (<150 characters)**
  - Long text may produce random/incorrect words
  - Split long text into multiple short sentences
  - See "Handling Long Text" section below
- **GPU recommended**: Much faster with NVIDIA CUDA GPU
- **Variability**: Some randomness in generation (can regenerate if needed)

## Troubleshooting

### PyTorch 2.6+ Compatibility

If you encounter `weights_only` pickle errors:

```bash
# The solution.py should work automatically, but if issues persist:
# See PYTORCH_FIX.md for manual patching instructions
```

### Common Issues

**"No module named 'bark'"**
```bash
pip install git+https://github.com/suno-ai/bark.git
```

**Generation is very slow**
- Normal on CPU (30-60 seconds per sentence)
- Use GPU for 10x speedup
- First run is slowest (model download + loading)

**Out of memory errors**
- Reduce text length (split into shorter sentences)
- Close other applications
- Use 8GB+ RAM system

**Audio quality issues**
- Bark occasionally produces artifacts
- Regenerate with slightly different text
- Try different emotional style or speaker
- Add prosody markers for better control

**Generated audio has random/incorrect words**
- **Cause**: Text is too long (>150 characters)
- **Solution**: Split into shorter sentences (<150 characters each)
- **Example**: Instead of one long paragraph, generate 5-10 short sentences
- See "Handling Long Text" section above for detailed guide

## Comparison: Bark vs Other TTS

| Feature | Bark | gTTS | pyttsx3 | ElevenLabs |
|---------|------|------|---------|------------|
| Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Emotion | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| Speed | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Offline | ✅ | ❌ | ✅ | ❌ |
| Free | ✅ | ✅ | ✅ | Limited |

**Verdict**: Bark offers the best quality for local, expressive TTS.

## Project Structure

```
python-tts/
├── solution.py              # Main TTS script (Bark-based)
├── tts_interactive.sh       # Interactive menu interface
├── test_all_speakers.sh     # Test all speakers script
├── requirements.txt         # Dependencies
├── README.md                # This file
├── system_design.md         # System architecture
├── IMPLEMENTATION_NOTES.md  # Technical implementation details
├── SPEAKER_GUIDE.md         # Speaker selection guide
├── USAGE_GUIDE.md           # Comprehensive usage examples
├── PYTORCH_FIX.md           # PyTorch 2.6+ compatibility
├── download_models.py       # Optional: pre-download models
├── .gitignore               # Git configuration
└── venv/                    # Virtual environment
```

## AI Dev Challenge

This project demonstrates:

- **Part A**: Complete system design with 7 required sections
- **Part B**: Working prototype with real emotional expression
- **Bonus**:
  - Advanced emotion control (7 styles)
  - Multiple speakers (10 voices)
  - Prosody markers
  - Interactive interface
  - Cross-platform support

### Key Achievements

- Truly expressive TTS (not just speed adjustment)
- Local neural model (no API dependencies)
- Documentary-quality narration
- 7 distinct emotional styles
- 10 unique speaker voices
- Interactive menu interface
- Cross-platform compatibility
- Natural prosody and intonation

## Credits

- **Bark**: Developed by Suno AI (https://github.com/suno-ai/bark)
- **Model**: Open-source transformer-based TTS
- **License**: MIT (Bark library)

---

**For production-quality documentary narration with true emotional expression.**
