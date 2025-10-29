# Emotional Speech Generation

Text-to-speech with emotional styles for narration.

## Features

- Neural TTS using Coqui TTS (VCTK-VITS model)
- 4 emotional styles: neutral, enthusiastic, serious, contemplative
- Multi-speaker support
- Simple CLI interface
- WAV output

## Quick Start

### Installation

```bash
cd python-tts
pip install -r requirements.txt
```

First run downloads the model (~200MB automatically).

### Usage

```bash
python solution.py "Hello world" hello.wav
python solution.py --style enthusiastic "Amazing discovery!" amazing.wav
```

## Options

`--style STYLE` - Emotional style (default: neutral)
`--model MODEL` - TTS model (default: tts_models/en/vctk/vits)

### Styles

| Style | Description | Use Case |
|-------|-------------|----------|
| `neutral` | Balanced, clear narration | General purpose, facts |
| `enthusiastic` | Excited, energetic delivery | Discoveries, positive news |
| `serious` | Formal, authoritative tone | Important information, warnings |
| `contemplative` | Thoughtful, slower pace | Reflective content, analysis |

### Examples

```bash
python solution.py "Welcome to the documentary" intro.wav
python solution.py --style enthusiastic "Scientists made a breakthrough!" excited.wav
python solution.py --style serious "This changes everything." serious.wav
python solution.py "Hello" output/hello.wav
```

## Requirements

- Python 3.8+
- 4GB RAM minimum
- Internet for first model download
- Optional: GPU for faster synthesis

## Troubleshooting

**Missing dependencies**: `pip install -r requirements.txt`

**Model loading error**: Check internet connection or clear cache at `~/.local/share/tts/`

**Slow generation**: First run downloads model (~200MB). GPU speeds this up significantly.

## Limitations

- English only
- Emotion control based on speaker selection
- Long texts (>200 words) may degrade quality
