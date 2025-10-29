#!/usr/bin/env python3
"""
Text-to-speech with emotional styles for narration.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional

try:
    from TTS.api import TTS
    import torch
except ImportError as e:
    print(f"Error: Missing required dependencies. Please install them first:")
    print(f"  pip install -r requirements.txt")
    print(f"\nDetails: {e}")
    sys.exit(1)


class EmotionalTTS:
    """TTS with emotional style support."""

    # Map emotions to speaker characteristics
    EMOTION_STYLES = {
        'neutral': {'speaker': 'Claribel Dervla', 'speed': 1.0},
        'enthusiastic': {'speaker': 'Daisy Studious', 'speed': 1.1},
        'serious': {'speaker': 'Gracie Wise', 'speed': 0.95},
        'contemplative': {'speaker': 'Sofia Hellen', 'speed': 0.9},
    }

    def __init__(self, model_name: str = "tts_models/en/vctk/vits"):
        print(f"Loading TTS model: {model_name}")
        print("This may take a while on first run (downloading model)...")

        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")

            self.tts = TTS(model_name=model_name, progress_bar=True).to(device)
            self.speakers = self.tts.speakers if hasattr(self.tts, 'speakers') else []

            print(f"Model loaded successfully!")
            if self.speakers:
                print(f"Available speakers: {len(self.speakers)}")

        except Exception as e:
            print(f"Error loading TTS model: {e}")
            print("\nTrying fallback model...")
            try:
                self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC").to(device)
                self.speakers = []
                print("Fallback model loaded (single speaker, no emotion control)")
            except Exception as e2:
                print(f"Error loading fallback model: {e2}")
                raise RuntimeError("Failed to load any TTS model")

    def synthesize(
        self,
        text: str,
        output_path: str,
        style: str = 'neutral'
    ) -> bool:
        if not text or not text.strip():
            print("Error: Input text is empty")
            return False

        # Validate style
        if style not in self.EMOTION_STYLES:
            print(f"Warning: Unknown style '{style}'. Using 'neutral'.")
            print(f"Available styles: {', '.join(self.EMOTION_STYLES.keys())}")
            style = 'neutral'

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            style_config = self.EMOTION_STYLES[style]

            print(f"\nSynthesizing speech...")
            print(f"  Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            print(f"  Style: {style}")
            print(f"  Output: {output_path}")

            # Synthesize with speaker if available
            if self.speakers:
                speaker = style_config['speaker']
                if speaker not in self.speakers:
                    speaker = self.speakers[0]
                    print(f"  Speaker: {speaker} (default)")
                else:
                    print(f"  Speaker: {speaker}")

                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker=speaker
                )
            else:
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path
                )

            if not os.path.exists(output_path):
                print(f"Error: Output file was not created")
                return False

            file_size = os.path.getsize(output_path)
            print(f"\n✓ Success! Generated {file_size} bytes")
            print(f"  Saved to: {output_path}")

            return True

        except Exception as e:
            print(f"Error during synthesis: {e}")
            return False


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate emotional speech from text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python solution.py "Hello world" hello.wav
  python solution.py --style enthusiastic "Amazing discovery!" amazing.wav
  python solution.py --style serious "This is important." serious.wav

Available styles:
  neutral        - Balanced, clear narration (default)
  enthusiastic   - Excited, energetic delivery
  serious        - Formal, authoritative tone
  contemplative  - Thoughtful, slower pace
        """
    )

    parser.add_argument(
        'text',
        type=str,
        help='Text to synthesize into speech'
    )

    parser.add_argument(
        'output',
        type=str,
        help='Output WAV file path'
    )

    parser.add_argument(
        '--style',
        type=str,
        default='neutral',
        choices=['neutral', 'enthusiastic', 'serious', 'contemplative'],
        help='Emotional style for the speech (default: neutral)'
    )

    parser.add_argument(
        '--model',
        type=str,
        default='tts_models/en/vctk/vits',
        help='TTS model to use (default: tts_models/en/vctk/vits)'
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    output_path = args.output
    if not output_path.endswith('.wav'):
        print("Warning: Output file should have .wav extension")
        output_path += '.wav'

    if os.path.exists(output_path):
        response = input(f"File '{output_path}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return 1

    try:
        tts_system = EmotionalTTS(model_name=args.model)
        success = tts_system.synthesize(
            text=args.text,
            output_path=output_path,
            style=args.style
        )

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
