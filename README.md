# 🎵 Logic Pro Voice Agent

Control Logic Pro with your voice while recording. No more interrupting your creative flow to click buttons! I wanted to build something that breaks down the barrier of entry for beginners picking up Logic Pro like I once did, by making the interaction with the GUI voice enabled and conversational.

## What It Does

Say natural commands like:
- "Hey Logic, hit record"
- "Play"
- "Stop"
- "Turn on the metronome"
- "Add reverb to track 2" (coming soon)
- "Load a piano" (coming soon)

The agent uses AI vision to understand Logic Pro's interface and clicks the right buttons for you by perceiving screen states through
screenshots and executing atomic actions such as clicking, typing, and scrolling, these agents, inspired by the paper 'OmegaUse: Building a General-Purpose GUI Agent
for Autonomous Task Execution'

## Why?

- 🎸 **Keep playing** - Control Logic Pro without putting down your instrument
- 💰 **Save money** - Don't need a studio engineer just to press play/stop
- 🎓 **Learn easier** - Lower barrier for new producers learning Logic Pro
- ⚡ **Stay in flow** - Don't break concentration switching to mouse

## Quick Start

### Prerequisites
- macOS with Logic Pro installed
- Python 3.9 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone this repo
git clone <your-repo-url>
cd LogicProAgent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Usage

```bash
# Make sure Logic Pro is open!

# Test mode (try a single command)
python src/main.py --command "play"

# Voice mode (continuous listening)
python src/main.py --voice

# Say "Hey Logic" followed by your command
# Or press your hotkey and speak
```

## How It Works

1. **You speak** → Voice recognition transcribes your command
2. **Screenshot** → Captures Logic Pro's current interface
3. **AI Vision** → Claude analyzes the UI and finds the right button
4. **Click** → Cursor moves and clicks automatically

## Current Status

✅ **Phase 1 (In Progress):** Basic transport controls (play, stop, record, metronome)
🔲 **Phase 2:** Voice input integration
🔲 **Phase 3:** Track control (arm, mute, solo)
🔲 **Phase 4:** Instrument loading and effects

## Cost

Uses Claude Vision API:
- ~$0.15 per command
- ~$3 per recording session (20 commands)


**Building with:** Claude AI, Python, PyAutoGUI, and a love for music production 🎶
