#!/usr/bin/env python3
"""
Emotional Speech Generation - Expressive Documentary Narration

Uses Bark (Suno AI) for truly expressive, emotional speech synthesis.
Supports natural prosody, emotion, and documentary-style narration.
"""

import sys
import os
import argparse
import warnings
warnings.filterwarnings('ignore')

try:
    from bark import SAMPLE_RATE, generate_audio, preload_models
    from scipy.io.wavfile import write as write_wav
    import numpy as np
except ImportError as e:
    print("Error: Required dependencies not installed")
    print("  pip install git+https://github.com/suno-ai/bark.git")
    print(f"\nDetails: {e}")
    sys.exit(1)


class EmotionalTTS:
    """Expressive TTS with real emotional control using Bark."""

    # Emotional prompts with prosody markers for Bark
    EMOTION_STYLES = {
        'neutral': {
            'prefix': '',
            'suffix': '',
            'speaker': 'v2/en_speaker_6',  # Clear, professional voice
            'description': 'Balanced, clear narration'
        },
        'enthusiastic': {
            'prefix': '[laughs] ',
            'suffix': '!',
            'speaker': 'v2/en_speaker_9',  # Energetic voice
            'description': 'Excited, energetic delivery with enthusiasm'
        },
        'serious': {
            'prefix': '',
            'suffix': '.',
            'speaker': 'v2/en_speaker_1',  # Deep, authoritative voice
            'description': 'Formal, authoritative tone with gravity'
        },
        'contemplative': {
            'prefix': '...',
            'suffix': '...',
            'speaker': 'v2/en_speaker_3',  # Thoughtful voice
            'description': 'Thoughtful, reflective with pauses'
        },
        'sad': {
            'prefix': '[sighs] ',
            'suffix': '...',
            'speaker': 'v2/en_speaker_3',  # Thoughtful, melancholic voice
            'description': 'Melancholic, sorrowful with sighs'
        },
        'excited': {
            'prefix': '[laughs] ',
            'suffix': '!!!',
            'speaker': 'v2/en_speaker_9',  # Very energetic voice
            'description': 'Very energetic, joyful with excitement'
        },
        'angry': {
            'prefix': '',
            'suffix': '!',
            'speaker': 'v2/en_speaker_1',  # Intense, forceful voice
            'description': 'Intense, forceful with strong emphasis'
        }
    }

    # Available Bark speakers (v2 English)
    # Note: Each speaker has unique voice characteristics. Test them to find your preference.
    AVAILABLE_SPEAKERS = [
        'v2/en_speaker_0',
        'v2/en_speaker_1',
        'v2/en_speaker_2',
        'v2/en_speaker_3',
        'v2/en_speaker_4',
        'v2/en_speaker_5',
        'v2/en_speaker_6',  # default
        'v2/en_speaker_7',
        'v2/en_speaker_8',
        'v2/en_speaker_9'
    ]

    def __init__(self):
        """Initialize Bark TTS system."""
        print("Initializing Bark TTS (this may take a moment)...")
        print("Downloading models on first run (~2GB)...")
        try:
            # Preload models for faster generation
            preload_models()
            print("✓ Bark TTS loaded successfully")
        except Exception as e:
            print(f"Warning: {e}")
            print("Models will download during first generation")

    def synthesize(self, text, output_path, style='neutral', speaker=None):
        """
        Generate expressive speech with emotional style.

        Args:
            text: Input text to synthesize
            output_path: Path to save WAV file
            style: Emotional style (neutral, enthusiastic, serious, contemplative, sad, excited, angry)
            speaker: Optional custom speaker (e.g., 'v2/en_speaker_4'). Overrides style's default speaker.

        Returns:
            True if successful, False otherwise
        """
        if not text or not text.strip():
            print("Error: Input text is empty")
            return False

        if style not in self.EMOTION_STYLES:
            print(f"Warning: Unknown style '{style}'. Using 'neutral'.")
            style = 'neutral'

        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            config = self.EMOTION_STYLES[style]

            # Use custom speaker if provided, otherwise use style default
            selected_speaker = speaker if speaker else config['speaker']

            # Validate speaker
            if speaker and speaker not in self.AVAILABLE_SPEAKERS:
                print(f"Warning: Unknown speaker '{speaker}'. Available speakers:")
                for spk in self.AVAILABLE_SPEAKERS:
                    print(f"  {spk}")
                print(f"Using default: {config['speaker']}")
                selected_speaker = config['speaker']

            # Add prosody markers for emotional expression
            emotional_text = f"{config['prefix']}{text}{config['suffix']}"

            print(f"\nGenerating expressive speech with Bark...")
            print(f"  Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            print(f"  Style: {style} ({config['description']})")
            print(f"  Speaker: {selected_speaker}")
            print(f"  Processing... (this may take 30-60 seconds)")

            # Generate audio with Bark (includes natural prosody and emotion)
            audio_array = generate_audio(
                emotional_text,
                history_prompt=selected_speaker
            )

            # Ensure output has .wav extension
            if not output_path.endswith('.wav'):
                output_path = output_path.rsplit('.', 1)[0] + '.wav'

            # Save as WAV file
            write_wav(output_path, SAMPLE_RATE, audio_array)

            if not os.path.exists(output_path):
                print(f"Error: Output file was not created")
                return False

            file_size = os.path.getsize(output_path)
            duration = len(audio_array) / SAMPLE_RATE

            print(f"\n✓ Success! Generated expressive audio")
            print(f"  Saved to: {output_path}")
            print(f"  Size: {file_size:,} bytes")
            print(f"  Duration: {duration:.1f} seconds")
            print(f"  Sample Rate: {SAMPLE_RATE} Hz")
            print(f"  Quality: Neural TTS with natural prosody")

            return True

        except Exception as e:
            print(f"Error during synthesis: {e}")
            import traceback
            traceback.print_exc()
            return False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate expressive documentary-style narration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python solution.py "Hello world" hello.wav
  python solution.py --style enthusiastic "Amazing discovery!" amazing.wav
  python solution.py --style serious "This is critical" serious.wav
  python solution.py --speaker v2/en_speaker_4 "Female voice" female.wav
  python solution.py --style sad --speaker v2/en_speaker_3 "I'm sorry" sad.wav

Emotional Styles:
  neutral        - Balanced, professional narration
  enthusiastic   - Excited, energetic with natural enthusiasm
  serious        - Authoritative, grave tone
  contemplative  - Thoughtful, reflective with pauses
  sad            - Melancholic, sorrowful with sighs
  excited        - Very energetic, joyful
  angry          - Intense, forceful with emphasis

Available Speakers:
  v2/en_speaker_0 through v2/en_speaker_9
  Each has unique voice characteristics
  Use --list-speakers to see all options
  Test them to find your preferred voice

Features:
  - Natural prosody and intonation
  - Real emotional expression (not just speed changes)
  - Documentary-quality narration
  - Runs 100% locally (no API needed)
  - First run downloads ~2GB models

Note: Generation takes 30-60 seconds per sentence (worth it for quality!)
        """
    )

    parser.add_argument('text', nargs='?', help='Text to synthesize')
    parser.add_argument('output', nargs='?', help='Output WAV file path')
    parser.add_argument(
        '--style',
        default='neutral',
        choices=['neutral', 'enthusiastic', 'serious', 'contemplative', 'sad', 'excited', 'angry'],
        help='Emotional style for narration (default: neutral)'
    )
    parser.add_argument(
        '--speaker',
        help='Custom speaker voice (e.g., v2/en_speaker_4 for warm female)'
    )
    parser.add_argument(
        '--list-speakers',
        action='store_true',
        help='List all available speakers and exit'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    # Handle --list-speakers
    if args.list_speakers:
        tts = EmotionalTTS()
        print("\n📢 Available Bark Speakers:\n")
        for speaker in tts.AVAILABLE_SPEAKERS:
            default = " (default)" if speaker == "v2/en_speaker_6" else ""
            print(f"  {speaker}{default}")
        print("\nNote: Each speaker has unique voice characteristics.")
        print("Test them with your content to find your preferred voice.")
        print("\nUsage: python solution.py --speaker <speaker_id> \"text\" output.wav")
        print("Example: python solution.py --speaker v2/en_speaker_3 \"Hello\" test.wav")
        return 0

    # Validate required arguments
    if not args.text or not args.output:
        print("Error: text and output arguments are required")
        print("Usage: python solution.py [--style STYLE] [--speaker SPEAKER] TEXT OUTPUT")
        print("       python solution.py --list-speakers")
        return 1

    # Ensure WAV extension
    output_path = args.output
    if not output_path.endswith('.wav'):
        output_path = output_path.rsplit('.', 1)[0] + '.wav'

    if os.path.exists(output_path):
        response = input(f"File '{output_path}' exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return 1

    try:
        tts = EmotionalTTS()
        success = tts.synthesize(args.text, output_path, args.style, args.speaker)
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 1
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
