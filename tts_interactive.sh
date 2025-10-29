#!/bin/bash
# Interactive Emotional TTS Script
# Provides menu-driven interface for generating expressive speech

set -e

# Colors for better UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate || {
        echo -e "${RED}Error: Virtual environment not found${NC}"
        echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    }
fi

# Main menu
show_menu() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   ${MAGENTA}🎭 Emotional Speech Generator${CYAN}              ║${NC}"
    echo -e "${CYAN}║   ${NC}Powered by Bark Neural TTS${CYAN}                 ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${YELLOW}What would you like to do?${NC}"
    echo
    echo "  1) Generate speech with emotion"
    echo "  2) List all available speakers"
    echo "  3) Test all emotional styles"
    echo "  4) Quick generation (neutral, default speaker)"
    echo "  5) Exit"
    echo
}

# List all available Bark speakers
list_speakers() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   ${MAGENTA}🎙️  Available Bark Speakers${CYAN}                ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${GREEN}Available speakers (v2/English):${NC}"
    echo
    echo "    v2/en_speaker_0"
    echo "    v2/en_speaker_1"
    echo "    v2/en_speaker_2"
    echo "    v2/en_speaker_3"
    echo "    v2/en_speaker_4"
    echo "    v2/en_speaker_5"
    echo "    v2/en_speaker_6  ${YELLOW}(default)${NC}"
    echo "    v2/en_speaker_7"
    echo "    v2/en_speaker_8"
    echo "    v2/en_speaker_9"
    echo
    echo -e "${YELLOW}Note:${NC} Each speaker has unique voice characteristics."
    echo "Test them with your content to find your preferred voice."
    echo
    echo -e "${BLUE}Usage:${NC} python solution.py --speaker <speaker_id> \"text\" output.wav"
    echo -e "${BLUE}Example:${NC} python solution.py --speaker v2/en_speaker_3 \"Hello\" test.wav"
    echo
}

# Generate speech with full customization
generate_custom() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   ${MAGENTA}🎬 Custom Speech Generation${CYAN}                ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo

    # Select emotion/style
    echo -e "${YELLOW}Select emotion style:${NC}"
    echo "  1) Neutral      - Balanced, professional"
    echo "  2) Enthusiastic - Excited, energetic with laughter"
    echo "  3) Serious      - Formal, authoritative"
    echo "  4) Contemplative - Thoughtful, reflective"
    echo "  5) Sad          - Melancholic, sorrowful"
    echo "  6) Excited      - Very energetic, joyful"
    echo "  7) Angry        - Intense, forceful"
    echo
    read -p "Choice (1-7): " emotion_choice

    case $emotion_choice in
        1) emotion="neutral" ;;
        2) emotion="enthusiastic" ;;
        3) emotion="serious" ;;
        4) emotion="contemplative" ;;
        5) emotion="sad" ;;
        6) emotion="excited" ;;
        7) emotion="angry" ;;
        *) echo -e "${RED}Invalid choice${NC}"; sleep 2; return ;;
    esac

    echo
    echo -e "${YELLOW}Select speaker:${NC}"
    echo "  0) v2/en_speaker_0"
    echo "  1) v2/en_speaker_1"
    echo "  2) v2/en_speaker_2"
    echo "  3) v2/en_speaker_3"
    echo "  4) v2/en_speaker_4"
    echo "  5) v2/en_speaker_5"
    echo "  6) v2/en_speaker_6 (default)"
    echo "  7) v2/en_speaker_7"
    echo "  8) v2/en_speaker_8"
    echo "  9) v2/en_speaker_9"
    echo " 10) Custom (enter speaker ID)"
    echo
    read -p "Choice (0-10): " speaker_choice

    case $speaker_choice in
        0) speaker="v2/en_speaker_0" ;;
        1) speaker="v2/en_speaker_1" ;;
        2) speaker="v2/en_speaker_2" ;;
        3) speaker="v2/en_speaker_3" ;;
        4) speaker="v2/en_speaker_4" ;;
        5) speaker="v2/en_speaker_5" ;;
        6) speaker="v2/en_speaker_6" ;;
        7) speaker="v2/en_speaker_7" ;;
        8) speaker="v2/en_speaker_8" ;;
        9) speaker="v2/en_speaker_9" ;;
        10)
            echo
            read -p "Enter speaker ID (e.g., v2/en_speaker_5): " speaker
            ;;
        *) echo -e "${RED}Invalid choice${NC}"; sleep 2; return ;;
    esac

    echo
    read -p "Enter text to synthesize: " text

    if [ -z "$text" ]; then
        echo -e "${RED}Text cannot be empty${NC}"
        sleep 2
        return
    fi

    # Generate filename
    timestamp=$(date +%Y%m%d_%H%M%S)
    output="output_${emotion}_${timestamp}.wav"

    echo
    echo -e "${GREEN}Generating speech...${NC}"
    echo -e "  Text: ${text:0:50}..."
    echo -e "  Emotion: $emotion"
    echo -e "  Speaker: $speaker"
    echo -e "  Output: $output"
    echo

    python solution.py --style "$emotion" --speaker "$speaker" "$text" "$output"

    if [ $? -eq 0 ]; then
        echo
        echo -e "${GREEN}✓ Success! Generated: $output${NC}"
        echo
        read -p "Play audio? (y/n): " play_choice
        if [[ "$play_choice" =~ ^[Yy]$ ]]; then
            if command -v afplay &> /dev/null; then
                afplay "$output"
            elif command -v aplay &> /dev/null; then
                aplay "$output"
            elif command -v ffplay &> /dev/null; then
                ffplay -nodisp -autoexit "$output"
            else
                echo -e "${YELLOW}No audio player found. File saved as $output${NC}"
            fi
        fi
    else
        echo -e "${RED}✗ Generation failed${NC}"
    fi

    echo
    read -p "Press Enter to continue..."
}

# Test all emotional styles
test_all_styles() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   ${MAGENTA}🧪 Testing All Emotional Styles${CYAN}            ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo

    read -p "Enter speaker ID (e.g., v2/en_speaker_6) or press Enter for default: " test_speaker

    declare -a speakers
    if [ -z "$test_speaker" ]; then
        speakers=("v2/en_speaker_6")
    else
        speakers=("$test_speaker")
    fi

    echo
    echo -e "${GREEN}Generating test samples...${NC}"
    echo

    for speaker in "${speakers[@]}"; do
        speaker_name=$(echo "$speaker" | cut -d'/' -f2)
        echo -e "${YELLOW}Testing with $speaker_name:${NC}"

        # Test each emotion
        python solution.py --style neutral --speaker "$speaker" \
            "This is a neutral documentary narration." \
            "test_neutral_${speaker_name}.wav" 2>/dev/null
        echo "  ✓ Neutral"

        python solution.py --style enthusiastic --speaker "$speaker" \
            "This discovery is absolutely amazing!" \
            "test_enthusiastic_${speaker_name}.wav" 2>/dev/null
        echo "  ✓ Enthusiastic"

        python solution.py --style serious --speaker "$speaker" \
            "This is a matter of grave importance." \
            "test_serious_${speaker_name}.wav" 2>/dev/null
        echo "  ✓ Serious"

        python solution.py --style contemplative --speaker "$speaker" \
            "What does this mean for our future?" \
            "test_contemplative_${speaker_name}.wav" 2>/dev/null
        echo "  ✓ Contemplative"

        echo
    done

    echo -e "${GREEN}✓ All test files generated!${NC}"
    echo -e "Files: test_*_en_speaker_*.wav"
    echo
    read -p "Press Enter to continue..."
}

# Quick generation
quick_generate() {
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   ${MAGENTA}⚡ Quick Generation${CYAN}                        ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo

    read -p "Enter text: " text

    if [ -z "$text" ]; then
        echo -e "${RED}Text cannot be empty${NC}"
        sleep 2
        return
    fi

    output="quick_$(date +%Y%m%d_%H%M%S).wav"

    echo
    echo -e "${GREEN}Generating...${NC}"
    python solution.py "$text" "$output"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Saved as: $output${NC}"
    fi

    echo
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    show_menu
    read -p "Enter choice (1-5): " choice

    case $choice in
        1) generate_custom ;;
        2) list_speakers; echo; read -p "Press Enter to continue..." ;;
        3) test_all_styles ;;
        4) quick_generate ;;
        5)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            sleep 1
            ;;
    esac
done
