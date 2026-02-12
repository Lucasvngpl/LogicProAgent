# Getting Started - Learning Path

Welcome! This guide will walk you through building the Logic Pro Voice Agent step-by-step. The vision model runs locally on your Mac, and voice services use lightweight APIs at near-zero cost.

## Prerequisites

- [ ] macOS on Apple Silicon (M1/M2/M3/M4)
- [ ] 16GB+ RAM recommended (for Qwen2.5-VL-7B vision model)
- [ ] Logic Pro installed (trial or full version)
- [ ] Python 3.9+ (`python3 --version` to check)
- [ ] Basic Python knowledge (functions, classes, imports)
- [ ] Text editor or IDE (VS Code recommended)
- [ ] Microphone for voice input (built-in is fine for testing)
- [ ] OpenAI API key for voice input ([get one here](https://platform.openai.com/api-keys) -- new accounts get $5 free credits)
- [ ] (Optional) ElevenLabs API key for premium voice responses ([free tier here](https://elevenlabs.io/)) -- macOS `say` fallback is always available

## Phase 1: Environment Setup (15 minutes)

### Step 1: Create Virtual Environment

```bash
# In the LogicProAgent directory
python3 -m venv venv
source venv/bin/activate  # Your prompt should change to show (venv)
```

**What's happening?** Virtual environments isolate your project's dependencies from system Python.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**What's installing?**
- `mlx-vlm` - Local vision model inference on Apple Silicon (Qwen2.5-VL-7B)
- `pyautogui` - Screen capture and cursor control
- `pillow` - Image processing
- `openai` - Speech-to-text API (gpt-4o-mini-transcribe)
- `elevenlabs` - Text-to-speech API client (optional, free tier)
- `sounddevice` - Microphone audio recording
- `numpy` - Audio/image processing
- `pyobjc-framework-Quartz` / `CoreGraphics` - macOS screen capture
- `python-dotenv` - Environment variable loading
- `pytest` - Testing

**Note:** First run of the agent will download the vision model automatically (~4-5GB). Subsequent runs are instant.

### Step 3: Set Up API Keys

```bash
cp .env.example .env
# Edit .env and add your keys, then:

# REQUIRED: OpenAI key for voice input (speech-to-text)
# Get yours at https://platform.openai.com/api-keys
# New accounts get $5 free credits (~1,600 min of transcription)
export OPENAI_API_KEY='your-key-here'

# OPTIONAL: ElevenLabs for premium voice responses
# Get a free key at https://elevenlabs.io/
export ELEVENLABS_API_KEY='your-key-here'
```

**Cost breakdown:**
- **Voice input (OpenAI):** ~$0.003/min -- a 50-command session costs ~$0.01
- **Voice output (ElevenLabs):** Free tier gives 10k chars/month. No key? The agent falls back to macOS `say` -- free, unlimited, offline.

Try the fallback now:
```bash
say "Hello Lucas, I'm your Logic Pro assistant"
```

### Step 4: Test Your Setup

```bash
python -c "import pyautogui; from mlx_vlm import load; from openai import OpenAI; print('All imports work!')"
```

**Troubleshooting:**
- If `mlx_vlm` fails: Make sure you're on Apple Silicon (`uname -m` should show `arm64`)
- If `openai` fails: Try `pip install openai` again
- If `sounddevice` fails: Try `pip install sounddevice` -- may need PortAudio (`brew install portaudio`)

---

## Phase 2: Screen Capture (30 minutes)

**Goal:** Learn to take screenshots programmatically

### Implement `src/screen_capture.py`

Open the file and implement each TODO:

#### 1. `__init__` method
```python
def __init__(self):
    # PyAutoGUI failsafe: If you move mouse to corner, it raises exception
    # Useful safety feature during development
    pyautogui.FAILSAFE = True
```

#### 2. `capture_screen` method
```python
def capture_screen(self, save_path: Optional[str] = None) -> Image.Image:
    # Take the screenshot
    screenshot = pyautogui.screenshot()

    # Save if path provided
    if save_path:
        screenshot.save(save_path)
        print(f"Screenshot saved to: {save_path}")

    return screenshot
```

#### 3. `image_to_base64` method
```python
def image_to_base64(self, image: Image.Image) -> str:
    # Create a bytes buffer
    buffered = io.BytesIO()

    # Save image to buffer as PNG
    image.save(buffered, format="PNG")

    # Get the bytes
    img_bytes = buffered.getvalue()

    # Encode to base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return img_base64
```

**Why base64?** Vision models need images in specific formats. Base64 converts binary (images) to text, which we can pass through our processing pipeline to the local model.

#### 4. Implement the rest and test it

```bash
python src/screen_capture.py
```

You should see:
- A screenshot saved to `data/screenshots/test_capture.png`
- Confirmation messages printed

**Learning checkpoint:** Can you explain what each method does? Why do we need base64?

---

## Phase 3: Local Vision Model (45 minutes)

**Goal:** Learn to run a vision-language model locally on Apple Silicon

Qwen2.5-VL-7B is a vision-language model that can "see" screenshots and understand UI elements. We run it locally using `mlx-vlm`, which is optimized for Apple Silicon GPUs. No API keys, no internet, no cost.

### Implement `src/vision.py`

This is the CORE of the project. Take your time!

#### 1. `__init__` method
```python
def __init__(self):
    """Initialize with local Qwen2.5-VL model."""
    print(f"Loading vision model: {MODEL_NAME}")
    print("(First run will download ~4-5GB, this is a one-time setup)")
    self.model, self.processor = load(MODEL_NAME)
    self.config = load_config(MODEL_NAME)
```

**Key concepts:**
- `load()` downloads (first time) and loads model weights into Apple Silicon GPU memory
- `load_config()` loads the chat template configuration the model expects
- The model is 4-bit quantized -- this means a 7B parameter model fits in ~4GB RAM instead of ~14GB

#### 2. `_decode_base64_image` helper
```python
def _decode_base64_image(self, base64_string: str) -> Image.Image:
    img_bytes = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(img_bytes))
```

We need to convert the base64 string back to a PIL Image because mlx-vlm expects PIL Image objects. This is the reverse of what we did in screen_capture.py.

#### 3. `analyze_ui_for_command` method

This is the most important method:

```python
def analyze_ui_for_command(self, screenshot_base64: str, user_command: str) -> Dict:
    # 1. Decode base64 back to PIL Image
    image = self._decode_base64_image(screenshot_base64)

    # 2. Build the prompt (same prompt engineering principles as cloud APIs!)
    prompt = f"""You are analyzing a Logic Pro interface screenshot.
The user wants to: "{user_command}"

Find the UI element(s) needed and return a JSON response:
{{
  "steps": [
    {{
      "action": "click",
      "x": 123,
      "y": 456,
      "element": "play_button",
      "description": "Click the play button"
    }}
  ],
  "reasoning": "Explanation of what you found"
}}

Return ONLY valid JSON, no other text."""

    # 3. Format prompt using model's chat template
    formatted = apply_chat_template(
        self.processor, self.config, prompt, num_images=1
    )

    # 4. Run inference locally (takes ~3-5 seconds)
    response = generate(
        self.model, self.processor, formatted,
        images=[image], max_tokens=500, verbose=False
    )

    # 5. Parse the response
    return self.parse_response(response)
```

**Key learning:**
- The prompt is almost identical to what you'd send to a cloud API! Prompt engineering works the same way for local models.
- `apply_chat_template` formats the prompt with special image tokens that Qwen2.5-VL expects.
- `generate` runs the model on your Mac's GPU. This takes ~3-5 seconds per command.

#### 4. `parse_response` method

```python
def parse_response(self, response_text: str) -> Dict:
    try:
        parsed = json.loads(response_text)
        return parsed
    except json.JSONDecodeError:
        # Local models sometimes add extra text around JSON
        # Try to extract JSON from the response
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end > start:
            try:
                return json.loads(response_text[start:end])
            except json.JSONDecodeError:
                pass
        print("Warning: Could not parse response as JSON")
        return {"steps": [], "reasoning": response_text}
```

**Why the fallback?** Local models are more likely than cloud APIs to add extra text around JSON. The extraction logic (finding `{` and `}`) handles this gracefully.

#### 5. Test it

```bash
# Open Logic Pro first, then:
python src/screen_capture.py  # Take a screenshot
```

Then test vision:
```python
# No API key needed!
analyzer = VisionAnalyzer()  # Downloads model on first run

# Load a screenshot
with open("data/screenshots/test_capture.png", "rb") as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')

# Analyze
result = analyzer.analyze_ui_for_command(img_data, "play")
print(result)
```

**Expected output:** JSON with coordinates for the play button!

**Learning checkpoint:**
- What happens if you ask for something not visible?
- Try different prompts -- how do results change?
- How long does inference take? Try timing it.

---

## Phase 4: Cursor Control (20 minutes)

**Goal:** Learn to control the mouse programmatically

### Implement `src/cursor_control.py`

**WARNING:** This will actually move your cursor!

#### Implementation

```python
def __init__(self, move_duration: float = 0.3):
    self.move_duration = move_duration
    pyautogui.PAUSE = 0.1  # Small pause between actions

def click_at(self, x: int, y: int, description: str = "") -> bool:
    try:
        print(f"  Clicking: {description} at ({x}, {y})")

        # Move cursor smoothly
        pyautogui.moveTo(x, y, duration=self.move_duration)

        # Click
        pyautogui.click()

        # Wait for UI to respond
        time.sleep(0.3)

        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def execute_action(self, action: Dict) -> bool:
    if action["action"] == "click":
        return self.click_at(
            action["x"],
            action["y"],
            action.get("description", "")
        )
    # Could add more action types here
    return False

def execute_actions(self, actions: List[Dict]) -> bool:
    for action in actions:
        if not self.execute_action(action):
            return False
        time.sleep(0.2)  # Delay between actions
    return True
```

#### Test it (carefully!)

```bash
python src/cursor_control.py
# Watch your cursor move!
```

**Learning checkpoint:** Why do we need delays? What happens if you remove them?

---

## Phase 5: Command Processing (20 minutes)

**Goal:** Map natural language to intents

### Implement `src/commands.py`

```python
def parse_command(self, user_input: str) -> Optional[str]:
    user_input = user_input.lower().strip()

    # Check each command pattern
    for command, patterns in self.command_patterns.items():
        for pattern in patterns:
            if pattern in user_input:
                return command

    return None

def get_command_description(self, command: str) -> str:
    descriptions = {
        "play": "Playing track",
        "stop": "Stopping playback",
        "record": "Starting recording",
        "metronome_on": "Turning on metronome",
        "metronome_off": "Turning off metronome"
    }
    return descriptions.get(command, "Unknown command")

def is_valid_command(self, command: str) -> bool:
    return command in self.command_patterns
```

**Learning:** This is simple pattern matching. Later you could use an LLM for better understanding!

---

## Phase 6: Putting It All Together (30 minutes)

**Goal:** Build the complete agent loop: Sense -> Think -> Act -> Speak

### Implement `src/main.py`

#### The Agent class

```python
def __init__(self):
    print("Initializing Logic Pro Agent...")
    self.screen_capture = ScreenCapture()
    self.vision = VisionAnalyzer()         # Local model, no API key!
    self.cursor = CursorController()
    self.commands = CommandProcessor()
    self.voice_input = VoiceInput()        # OpenAI STT API
    self.tts = TextToSpeech()              # ElevenLabs or macOS say
    print("Ready!")

def execute_command(self, user_command: str) -> bool:
    print(f"\nCommand: {user_command}")

    # 1. Parse command
    parsed = self.commands.parse_command(user_command)
    if not parsed:
        self.tts.speak("I don't understand that command.")
        return False

    print(f"  Parsed as: {parsed}")

    # 2. SPEAK - Confirm we're working on it
    self.tts.speak_for_command(parsed)

    # 3. SENSE - Capture screenshot
    print("  Capturing screen...")
    img, img_base64 = self.screen_capture.capture_and_encode(
        f"data/screenshots/{parsed}_{int(time.time())}.png"
    )

    # 4. THINK - Analyze with LOCAL vision model
    print("  Analyzing UI with Qwen2.5-VL...")
    result = self.vision.analyze_ui_for_command(img_base64, parsed)

    if not result.get("steps"):
        self.tts.speak("I couldn't find that button.")
        return False

    print(f"  Found {len(result['steps'])} action(s)")
    if result.get("reasoning"):
        print(f"  Reasoning: {result['reasoning']}")

    # 5. ACT - Execute actions
    print("  Executing actions...")
    success = self.cursor.execute_actions(result["steps"])

    if success:
        print("Command completed successfully!")
    else:
        self.tts.speak("Something went wrong.")

    return success
```

#### The voice loop

```python
def voice_loop(self):
    """Continuously listen for voice commands."""
    print("Voice mode active. Say 'Hey Logic' + command.")
    print("Press Ctrl+C to stop.\n")
    while True:
        try:
            command = self.voice_input.listen_for_command()
            if command:
                self.execute_command(command)
        except KeyboardInterrupt:
            print("\nStopping voice mode.")
            break
```

**Learning:** This is the full agent loop -- listen for a wake word, parse the command, sense the screen, think about what to do, act on it, and speak the result. Then go back to listening.

#### The main function

```python
def main():
    parser = argparse.ArgumentParser(description="Logic Pro Voice Agent")
    parser.add_argument("--command", help="Test a single command")
    parser.add_argument("--voice", action="store_true", help="Start voice mode")
    args = parser.parse_args()

    # No API key needed! Everything runs locally.
    agent = LogicProAgent()

    if args.command:
        agent.execute_command(args.command)
    elif args.voice:
        agent.voice_loop()
    else:
        print("Usage:")
        print("  python src/main.py --command 'play'")
        print("  python src/main.py --voice")

if __name__ == "__main__":
    main()
```

---

## Phase 7: Voice Input (30 minutes)

**Goal:** Learn to capture speech and transcribe it using OpenAI's speech-to-text API

OpenAI's `gpt-4o-mini-transcribe` model provides fast, accurate transcription at ~$0.003/min. For short voice commands like "Hey Logic, play", each transcription costs a fraction of a cent.

### Implement `src/voice_input.py`

#### 1. `__init__` method
```python
def __init__(self, model: str = "gpt-4o-mini-transcribe"):
    print(f"Initializing OpenAI STT (model: {model})")
    self.client = OpenAI()  # Reads OPENAI_API_KEY from env automatically
    self.model = model
```

**How simple is that?** No model downloads, no GPU setup. The OpenAI client reads your API key from the `OPENAI_API_KEY` environment variable automatically.

#### 2. `record_audio` method
```python
def record_audio(self, duration: float = 5.0) -> np.ndarray:
    print(f"Listening for {duration} seconds...")
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()  # Block until recording is done
    return audio.flatten()
```

#### 3. `_save_audio_to_wav` helper
```python
def _save_audio_to_wav(self, audio: np.ndarray) -> str:
    # Create temp file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    # Convert float32 (-1 to 1) to int16 (-32768 to 32767)
    audio_int16 = (audio * 32767).astype(np.int16)
    with wave.open(temp_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())
    return temp_path
```

#### 4. `transcribe` method
```python
def transcribe(self, audio: np.ndarray) -> str:
    # Save to temp WAV file
    temp_path = self._save_audio_to_wav(audio)

    # Send to OpenAI API
    with open(temp_path, "rb") as audio_file:
        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
        )

    # Clean up temp file
    os.unlink(temp_path)

    return transcription.text.strip()
```

**Key learning:** The OpenAI SDK handles all the complexity -- encoding, network calls, error handling. You just pass a file and get text back.

#### 5. `check_wake_word` method
```python
def check_wake_word(self, text: str) -> Optional[str]:
    text_lower = text.lower().strip()
    if "hey logic" in text_lower:
        idx = text_lower.index("hey logic") + len("hey logic")
        command = text_lower[idx:].strip()
        return command if command else None
    return None
```

**Note:** This is simple string matching. Production systems use dedicated models (like Porcupine) for always-on wake word detection with minimal CPU usage.

#### 6. `listen_for_command` method
```python
def listen_for_command(self, duration: float = 5.0) -> Optional[str]:
    audio = self.record_audio(duration)
    text = self.transcribe(audio)
    print(f"  Heard: {text}")
    return self.check_wake_word(text)
```

#### 7. Test it

```bash
python src/voice_input.py
# Speak: "Hey Logic play"
# Expected output: Command: "play"
```

**Learning checkpoint:**
- What happens with background noise?
- Try `gpt-4o-transcribe` instead of `gpt-4o-mini-transcribe` -- is accuracy noticeably better for short commands?
- How would you implement `record_until_silence` instead of fixed duration?

---

## Phase 8: Voice Response (20 minutes)

**Goal:** Learn text-to-speech with a premium API and free local fallback

The agent speaks back to you! We use ElevenLabs for high-quality voice when available, with macOS `say` as a free unlimited fallback.

### Implement `src/text_to_speech.py`

#### 1. `__init__` method
```python
def __init__(self, use_elevenlabs: bool = True):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if use_elevenlabs and api_key:
        self.client = ElevenLabs(api_key=api_key)
        self.use_elevenlabs = True
        print("Using ElevenLabs TTS")
    else:
        self.client = None
        self.use_elevenlabs = False
        print("Using macOS say for TTS (free, unlimited)")
```

**Learning:** This is a graceful fallback pattern. Try the premium option first; if not available, fall back to something that always works. Your agent never fails to speak.

#### 2. `speak` method
```python
def speak(self, text: str):
    if self.use_elevenlabs:
        try:
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=DEFAULT_VOICE_ID,
                model_id=DEFAULT_MODEL,
                output_format="mp3_44100_128"
            )
            play(audio)
        except Exception as e:
            print(f"ElevenLabs error: {e}, falling back to macOS say")
            self._speak_macos(text)
    else:
        self._speak_macos(text)
```

#### 3. `_speak_macos` fallback
```python
def _speak_macos(self, text: str):
    subprocess.run(["say", text])
```

Instant, free, and always available on macOS. Works offline too!

#### 4. `speak_for_command` method
```python
def speak_for_command(self, command: str):
    response = COMMAND_RESPONSES.get(command, f"Working on {command}.")
    self.speak(response)
```

Pre-defined responses serve two purposes: (1) they sound more natural than generated text, and (2) they save ElevenLabs character quota by keeping responses short (~30 chars each).

#### 5. Test it

```bash
# Quick test with macOS say (no setup needed):
python -c "import subprocess; subprocess.run(['say', 'Sure Lucas, playing now'])"

# Full test:
python src/text_to_speech.py
```

---

## Phase 9: First Test! (The Moment of Truth)

### Prerequisites:
1. Open Logic Pro
2. Load a project (any project)
3. Make sure Logic Pro window is visible

### Run it:

```bash
# Make sure your API key is set:
export OPENAI_API_KEY='your-key'
python src/main.py --command "play"
```

### What should happen:
1. Models load (first time takes a minute, then instant)
2. Screenshot captured
3. Analyzed by local Qwen2.5-VL model (~3-5 seconds)
4. Play button coordinates found
5. Cursor moves to play button
6. Clicks!
7. Agent says "Sure Lucas, playing now"
8. Logic Pro starts playing!

### Try voice mode:

```bash
python src/main.py --voice
# Say: "Hey Logic, play"
```

### Troubleshooting:
- **"ModuleNotFoundError"**: Did you activate venv? Try `source venv/bin/activate`
- **Model download stalls**: First run downloads ~4-5GB. Check your internet connection.
- **Out of memory**: Qwen2.5-VL-7B needs ~8GB VRAM. Close other apps. If you have 8GB RAM, try the 3B model.
- **Wrong coordinates**: Logic Pro window size might differ. Try full screen. Adjust the prompt in vision.py.
- **Nothing happens**: Check if Logic Pro is in foreground. Check macOS Accessibility permissions for Python.
- **Microphone not working**: Check System Settings > Privacy > Microphone. Grant access to Terminal/VS Code.
- **No sound from agent**: If ElevenLabs isn't set up, the agent uses `say`. Test with: `say "test"` in Terminal.

---

## Next Steps

Once you have "play" working:

1. **Test other commands:**
   ```bash
   python src/main.py --command "stop"
   python src/main.py --command "record"
   python src/main.py --command "metronome on"
   ```

2. **Try voice mode for a full session:**
   ```bash
   python src/main.py --voice
   # Try: "Hey Logic, play" / "Hey Logic, stop" / "Hey Logic, record"
   ```

3. **Improve accuracy:**
   - Adjust prompts in vision.py
   - Try a larger model (Qwen2.5-VL-32B) if you have 32GB+ RAM
   - Add more command patterns in commands.py

4. **Move to Phase 2 from CLAUDE.md** -- Track control (arm, mute, solo specific tracks)

5. **Move to Phase 3 from CLAUDE.md** -- Multi-step commands (loading plugins, adding effects)

---

## Learning Reflections

After completing Phases 1-9, you should understand:

- How to structure a Python application
- Running vision-language models locally with MLX on Apple Silicon
- Speech-to-text with OpenAI's API
- Text-to-speech with graceful API/local fallback
- Computer vision for GUI understanding
- Cursor automation with PyAutoGUI
- The agent loop: Sense -> Think -> Act -> Speak
- Error handling and debugging
- Prompt engineering for vision models (works the same locally!)

**Questions to think about:**
- What are the trade-offs of local models vs cloud APIs?
- How could you make inference faster?
- What if Logic Pro UI changes? (Hint: zero-shot approach handles this!)
- How would you add more complex commands?
- What are the trade-offs of 4-bit quantization vs full precision?

---

## Getting Help

- **Read the code comments** - Lots of hints!
- **Check CLAUDE.md** - Architecture details
- **Print debugging** - Add print() everywhere
- **Test incrementally** - One function at a time
- **Experiment** - Try changing prompts and see what happens
- **Model docs** - [mlx-vlm](https://github.com/Blaizzy/mlx-vlm), [OpenAI STT](https://developers.openai.com/api/docs/guides/speech-to-text), [ElevenLabs](https://github.com/elevenlabs/elevenlabs-python)

---

**Ready? Start with Phase 1!**

Remember: The goal is to LEARN, not just to finish. Take your time, experiment, and have fun!
