# Logic Pro Voice Agent

## Project Overview

A voice-controlled GUI automation agent for Logic Pro that allows music producers to control their DAW hands-free while recording. Built as a learning exercise in AI agents, computer vision, and GUI automation.

### The Problem
- Music producers need to control Logic Pro while playing instruments
- Hiring a studio engineer just to press play/record is expensive
- Switching between instrument and mouse breaks creative flow
- Barrier of entry for new producers learning complex DAW interfaces

### The Solution
Voice commands → Vision-based GUI understanding → Automated cursor control

**Example:** Say "Hey Logic, hit record" and the agent finds and clicks the record button for you.

---

## Architecture

### Zero-Shot Vision Approach (100% Local, Free)

```
┌──────────────────┐
│   Voice Input    │  (faster-whisper, local Whisper base.en)
│   "Hey Logic,    │
│    hit record"   │
└──────┬───────────┘
       │
       ▼
┌─────────────────┐
│ Intent Parsing  │  (keyword matching + NLU)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Screen Capture  │  (PyAutoGUI/Pillow)
└──────┬──────────┘
       │
       ▼
┌──────────────────────────┐
│ Local Vision Model       │  (Qwen2.5-VL-7B via mlx-vlm)
│ Runs on Apple Silicon    │  (No API, no internet, no cost)
└──────┬───────────────────┘
       │
       ▼
┌─────────────────┐
│ Action Planning │  (Parse model's JSON response)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Cursor Control  │  (PyAutoGUI - move & click)
└──────┬──────────┘
       │
       ▼
┌──────────────────────┐
│ Voice Response       │  (ElevenLabs free tier / macOS say)
│ "Sure Lucas,         │
│  starting recording" │
└──────────────────────┘
```

### Why Zero-Shot?
- **No training data needed** - Qwen2.5-VL already understands UIs
- **Fast to build** - Start prototyping immediately
- **Adaptable** - Works even when Logic Pro UI changes
- **Learning-friendly** - Can see each step working
- **Free** - All models run locally on your Mac

**Trade-offs:**
- Slower (~3-5 seconds per command) vs trained model (<1 second)
- First run downloads models (~4-5GB for vision, ~150MB for Whisper)
- Requires 16GB+ RAM for Qwen2.5-VL-7B

For a recording session (10-50 commands), this is totally acceptable.

---

## Technology Stack

### Core Dependencies
- **Python 3.9+** - Main language
- **mlx-vlm** - Local vision model inference on Apple Silicon (Qwen2.5-VL-7B)
- **faster-whisper** - Local speech-to-text (Whisper base.en model)
- **elevenlabs** - Text-to-speech for agent responses (free tier: 10k chars/month)
- **pyautogui** - Cross-platform cursor control and screenshots
- **pillow** - Image processing
- **sounddevice** - Microphone audio recording
- **numpy** - Audio processing

### macOS-Specific
- **Quartz/CoreGraphics** - Better window capture (optional)
- **macOS `say` command** - Free TTS fallback (no internet needed)
- **pyobjc** - macOS Accessibility API (future enhancement)

---

## Project Structure

```
LogicProAgent/
├── CLAUDE.md              # This file - project documentation
├── README.md              # User-facing documentation
├── requirements.txt       # Python dependencies
│
├── src/
│   ├── __init__.py
│   ├── main.py            # Entry point + agent loop
│   ├── voice_input.py     # faster-whisper speech-to-text
│   ├── text_to_speech.py  # ElevenLabs TTS + macOS say fallback
│   ├── vision.py          # Qwen2.5-VL-7B local vision (mlx-vlm)
│   ├── screen_capture.py  # Screenshot utilities
│   ├── cursor_control.py  # PyAutoGUI wrapper
│   └── commands.py        # Command definitions
│
├── tests/
│   ├── test_voice.py
│   ├── test_vision.py
│   └── test_commands.py
│
├── examples/
│   └── basic_commands.py # Example usage
│
└── data/
    └── screenshots/      # For debugging/testing
```

---

## Development Phases

### ✅ Phase 1: Basic Transport (START HERE)
**Goal:** Get one command working end-to-end

**Tasks:**
1. Set up Python environment
2. Install dependencies
3. Capture Logic Pro screenshot
4. Send to Claude Vision API
5. Parse response
6. Click the play button
7. Test with "play", "stop", "record"

**Success Criteria:**
- Can say "play" and Logic Pro starts playing
- Works 9/10 times

**Learning Focus:**
- Python project setup
- API calls with anthropic library
- Basic image handling
- Cursor automation

---

### 🔲 Phase 2: Voice Input Integration
**Goal:** Replace test commands with actual voice input

**Tasks:**
1. Set up speech_recognition
2. Implement continuous listening
3. Add wake word ("Hey Logic") or push-to-talk
4. Handle background noise

**Success Criteria:**
- Can speak naturally and agent responds
- Minimal false triggers

**Learning Focus:**
- Audio processing
- Speech-to-text APIs
- Background thread management

---

### 🔲 Phase 3: Track Control
**Goal:** Control specific tracks

**Commands:**
- "arm track 2 for recording"
- "mute track 1"
- "solo vocals"

**New Challenges:**
- Finding specific UI elements (track by number or name)
- Multiple similar elements on screen

**Learning Focus:**
- More complex vision prompts
- Coordinate calculation
- Handling ambiguity

---

### 🔲 Phase 4: Multi-Step Commands
**Goal:** Handle commands requiring multiple actions

**Commands:**
- "load a piano on track 2"
- "add reverb to vocals"

**New Challenges:**
- Action sequences
- Menu navigation
- Search and selection

**Learning Focus:**
- State management
- Error handling
- Retry logic

---

### 🔲 Phase 5: Polish & Error Handling
**Goal:** Make it robust and production-ready

**Tasks:**
- Handle Logic Pro window not found
- Handle ambiguous voice commands
- Add confirmation for destructive actions
- Implement "undo last command"
- Add visual/audio feedback

**Learning Focus:**
- Production-grade error handling
- UX considerations
- Testing edge cases

---

## Key Learning Concepts

### 1. **Computer Vision for GUI Understanding**
- How AI models "see" user interfaces
- Coordinate systems and screen resolution
- Element detection and localization

### 2. **API Integration**
- RESTful API calls
- Authentication and API keys
- Rate limiting and costs
- Error handling

### 3. **GUI Automation**
- Cursor control and input simulation
- Timing and synchronization
- Platform-specific considerations (macOS)

### 4. **Voice Interfaces**
- Speech-to-text technologies
- Wake word detection
- Natural language understanding
- Handling ambiguity

### 5. **Agent Design Patterns**
- Sense → Think → Act loop
- State management
- Action planning
- Error recovery

---

## Getting Started

### Prerequisites
1. **macOS with Apple Silicon** (M1/M2/M3/M4, 16GB+ RAM)
2. **Logic Pro installed** (trial or full version)
3. **Python 3.9+** installed
4. **Microphone** for voice input
5. **ElevenLabs API key** (optional, free at https://elevenlabs.io/ — falls back to macOS `say`)

### Quick Start

```bash
# 1. Clone/navigate to project
cd LogicProAgent

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set up ElevenLabs for premium voice responses
export ELEVENLABS_API_KEY='your-key-here'  # Or skip — macOS say works fine

# 5. Run basic test
# First run downloads vision model (~4-5GB) + Whisper model (~150MB)
python src/main.py --test-mode

# 6. Try first command
# (Open Logic Pro first!)
python src/main.py --command "play"

# 7. Voice mode
python src/main.py --voice
# Say: "Hey Logic, hit record"
```

---

## Example Usage

```python
from main import LogicProAgent

# Initialize agent (no API key needed — all models run locally!)
agent = LogicProAgent()

# Execute a command
agent.execute_command("play")
agent.execute_command("record")
agent.execute_command("stop")

# Voice mode — speak commands hands-free
agent.voice_loop()  # Say "Hey Logic, play" etc.
```

---

## Testing Strategy

### Manual Testing
1. Open Logic Pro with a test project
2. Run command from CLI
3. Verify it works visually

### Automated Testing
- Mock vision model responses
- Test coordinate parsing
- Test action sequences
- Integration tests with screenshots

### Debugging
- Save screenshots before each action
- Log all API responses
- Record cursor movements
- Verbose mode for troubleshooting

---

## Common Pitfalls & Solutions

### Issue: Vision model returns wrong coordinates
**Solution:**
- Provide better context in prompt
- Show previous successful examples
- Ask for step-by-step reasoning
- Try a larger model (Qwen2.5-VL-32B) if 7B isn't accurate enough

### Issue: Commands execute too fast
**Solution:**
- Add delays between actions
- Wait for UI to update
- Verify action completed before next step

### Issue: Can't find Logic Pro window
**Solution:**
- Check Logic Pro is running
- Bring Logic Pro to foreground
- Use window title matching

### Issue: Voice recognition mishears commands
**Solution:**
- Use push-to-talk instead of continuous
- Add command confirmation
- Implement "undo" feature

---

## Future Enhancements

### Short-term
- [ ] Support for Logic Pro keyboard shortcuts (faster than clicking)
- [ ] Command history and undo
- [ ] Visual feedback overlay
- [ ] Better error messages

### Medium-term
- [ ] Learn user's preferred plugins/instruments
- [ ] Custom voice commands ("my piano" → specific preset)
- [ ] Batch commands ("set up recording session")
- [ ] Integration with MIDI controllers

### Long-term
- [ ] Train specialized model for faster inference
- [ ] Support for other DAWs (Ableton, Pro Tools)
- [ ] Cloud-based processing
- [ ] Mobile app control

---

## Cost Estimates

### All Local Models — $0 per command!
- **Vision (Qwen2.5-VL-7B):** Free, runs locally
- **STT (faster-whisper):** Free, runs locally
- **TTS (ElevenLabs free tier):** 10,000 chars/month free (~5 sessions)
- **TTS fallback (macOS say):** Free, unlimited, offline

**Per session: $0** (vs ~$3.00 with Claude Vision API)

### One-Time Setup Costs
- Vision model download: ~4-5GB
- Whisper model download: ~150MB
- That's it!

### ElevenLabs Free Tier Budget
- 10,000 characters/month
- Average response: ~30 characters
- ~330 responses/month = ~6-7 sessions of 50 commands
- If you need more: macOS `say` fallback is always available

---

## Resources

### Documentation
- [mlx-vlm (Vision Models on Mac)](https://github.com/Blaizzy/mlx-vlm)
- [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [ElevenLabs Python SDK](https://github.com/elevenlabs/elevenlabs-python)
- [PyAutoGUI Docs](https://pyautogui.readthedocs.io/)

### Inspiration
- OmegaUse paper: GUI agents with vision models
- [Anthropic Computer Use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
- [ShowUI](https://github.com/showlab/computer_use_ootb) - GUI agent with vision models
- Open Interpreter project

### Community
- File issues on GitHub
- Share examples and improvements
- Document what you learn!

---

## Contributing

This is a learning project! Feel free to:
- Try different approaches
- Experiment with prompts
- Add new commands
- Improve error handling
- Document your learnings

**Philosophy:** Build, break, learn, iterate.

---

## Notes for Future Claude Sessions

### When resuming this project:
1. Check which phase we're in (see Development Phases above)
2. Read recent commit messages for context
3. Check `data/screenshots/` for debugging examples
4. Test with `python src/main.py --test-mode` first

### Key Design Decisions:
- **Zero-shot over training:** Prioritizes speed of development and learning
- **Python over Swift:** Cross-platform, better AI libraries, easier for beginners
- **Vision over AppleScript:** Logic Pro has no comprehensive scripting support
- **Local models over APIs:** $0 cost, no internet needed, privacy-friendly
- **Qwen2.5-VL-7B:** Best accuracy for GUI understanding on 16GB Mac
- **faster-whisper over openai-whisper:** 4x faster, same accuracy
- **ElevenLabs + macOS say:** Premium voice when available, free fallback always

### User's Goals:
- Learn about AI agents and GUI automation
- Make a practical tool for music production
- Hands-free control while recording instruments
- Lower barrier of entry for new producers

---

**Last Updated:** 2026-02-07
**Status:** Phase 1 - Skeleton code with local model stack
**Next Step:** Implement the TODO methods in each file, starting with vision.py
