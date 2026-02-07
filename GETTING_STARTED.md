# Getting Started - Learning Path

Welcome! This guide will walk you through building the Logic Pro Voice Agent step-by-step. Each section teaches you new concepts as you implement the project.

## Prerequisites

- [ ] macOS with Logic Pro installed
- [ ] Python 3.9+ (`python3 --version` to check)
- [ ] Basic Python knowledge (functions, classes, imports)
- [ ] Text editor or IDE (VS Code recommended)
- [ ] Anthropic API key ([get one here](https://console.anthropic.com/))

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
- `anthropic` - Claude API client
- `pyautogui` - Screen capture and cursor control
- `pillow` - Image processing

### Step 3: Set Up API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your real API key
# Then load it:
export ANTHROPIC_API_KEY='your-actual-key-here'
```

**Security note:** Never commit .env to git! (Already in .gitignore)

### Step 4: Test Your Setup

```bash
python -c "import pyautogui; import anthropic; print('✓ All imports work!')"
```

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

**Why base64?** APIs expect text, not binary data. Base64 converts binary (images) to text.

#### 4. Implement the rest and test it

```bash
python src/screen_capture.py
```

You should see:
- A screenshot saved to `data/screenshots/test_capture.png`
- Confirmation messages printed

**Learning checkpoint:** Can you explain what each method does? Why do we need base64?

---

## Phase 3: Claude Vision Integration (45 minutes)

**Goal:** Learn to call AI vision APIs

### Implement `src/vision.py`

This is the CORE of the project. Take your time!

#### 1. `__init__` method
```python
def __init__(self, api_key: str):
    # Create the Anthropic client
    self.client = Anthropic(api_key=api_key)
```

#### 2. `analyze_ui_for_command` method

This is complex! Here's the structure:

```python
def analyze_ui_for_command(self, screenshot_base64: str, user_command: str) -> Dict:
    # Construct the prompt
    prompt = f"""You are analyzing a Logic Pro interface screenshot.
The user wants to: "{user_command}"

Analyze the interface and return a JSON response with the coordinates to click.

Return format:
{{
  "steps": [
    {{
      "action": "click",
      "x": 100,
      "y": 50,
      "element": "play_button",
      "description": "Click the green play button in transport bar"
    }}
  ],
  "reasoning": "The play button is located at the top center of the interface..."
}}

Be precise with coordinates. Think step by step.
"""

    # Make the API call
    response = self.client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": screenshot_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    # Parse the response
    return self.parse_response(response)
```

**Key learning:**
- Vision models need both image AND text prompt
- Prompt engineering matters! Be specific about format
- Asking for reasoning helps the model think better

#### 3. `parse_response` method

```python
def parse_response(self, response) -> Dict:
    # Extract the text content
    text_content = response.content[0].text

    # Try to parse as JSON
    try:
        parsed = json.loads(text_content)
        return parsed
    except json.JSONDecodeError:
        # Sometimes Claude might return text with JSON inside
        # You could extract it, or just return error
        print("Warning: Could not parse response as JSON")
        print(text_content)
        return {"steps": [], "reasoning": text_content}
```

#### 4. Test it (you'll need API key!)

Create a test screenshot first:
```bash
# Open Logic Pro first!
python src/screen_capture.py
```

Then test vision:
```python
# In test_vision():
api_key = os.getenv("ANTHROPIC_API_KEY")
analyzer = VisionAnalyzer(api_key)

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
- Try different prompts - how do results change?

---

## Phase 4: Cursor Control (20 minutes)

**Goal:** Learn to control the mouse programmatically

### Implement `src/cursor_control.py`

⚠️ **WARNING:** This will actually move your cursor!

#### Implementation

```python
def __init__(self, move_duration: float = 0.3):
    self.move_duration = move_duration
    pyautogui.PAUSE = 0.1  # Small pause between actions

def click_at(self, x: int, y: int, description: str = "") -> bool:
    try:
        print(f"  → Clicking: {description} at ({x}, {y})")

        # Move cursor smoothly
        pyautogui.moveTo(x, y, duration=self.move_duration)

        # Click
        pyautogui.click()

        # Wait for UI to respond
        time.sleep(0.3)

        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
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

**Goal:** Build the complete agent loop

### Implement `src/main.py`

#### The Agent class

```python
def __init__(self, api_key: str):
    print("Initializing Logic Pro Agent...")
    self.screen_capture = ScreenCapture()
    self.vision = VisionAnalyzer(api_key)
    self.cursor = CursorController()
    self.commands = CommandProcessor()
    print("✓ Ready!")

def execute_command(self, user_command: str) -> bool:
    print(f"\n🎵 Command: {user_command}")

    # 1. Parse command
    parsed = self.commands.parse_command(user_command)
    if not parsed:
        print("✗ Unknown command")
        return False

    print(f"  → Parsed as: {parsed}")
    print(f"  → {self.commands.get_command_description(parsed)}")

    # 2. SENSE - Capture screenshot
    print("  → Capturing screen...")
    img, img_base64 = self.screen_capture.capture_and_encode(
        f"data/screenshots/{parsed}_{int(time.time())}.png"
    )

    # 3. THINK - Analyze with vision
    print("  → Analyzing UI with Claude Vision...")
    result = self.vision.analyze_ui_for_command(img_base64, parsed)

    if not result.get("steps"):
        print("✗ Could not determine actions")
        return False

    print(f"  → Found {len(result['steps'])} action(s)")
    if result.get("reasoning"):
        print(f"  → Reasoning: {result['reasoning']}")

    # 4. ACT - Execute actions
    print("  → Executing actions...")
    success = self.cursor.execute_actions(result["steps"])

    if success:
        print("✓ Command completed successfully!")
    else:
        print("✗ Command failed")

    return success
```

#### The main function

```python
def main():
    parser = argparse.ArgumentParser(description="Logic Pro Voice Agent")
    parser.add_argument("--command", help="Test a single command")
    parser.add_argument("--api-key", help="Anthropic API key (or use env)")
    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: No API key provided")
        print("Set ANTHROPIC_API_KEY env variable or use --api-key")
        sys.exit(1)

    # Create agent
    agent = LogicProAgent(api_key)

    # Run command
    if args.command:
        agent.execute_command(args.command)
    else:
        print("Usage: python src/main.py --command 'play'")

if __name__ == "__main__":
    main()
```

---

## Phase 7: First Test! (The Moment of Truth)

### Prerequisites:
1. Open Logic Pro
2. Load a project (any project)
3. Make sure Logic Pro window is visible

### Run it:

```bash
export ANTHROPIC_API_KEY='your-key'
python src/main.py --command "play"
```

### What should happen:
1. Screenshot captured ✓
2. Sent to Claude ✓
3. Claude analyzes and finds play button ✓
4. Cursor moves to play button ✓
5. Clicks! ✓
6. Logic Pro starts playing! ✓✓✓

### Troubleshooting:
- **"ModuleNotFoundError"**: Did you activate venv?
- **"API key not found"**: Export it again
- **"Wrong coordinates"**: Logic Pro window size might differ. Try full screen.
- **Nothing happens**: Check if Logic Pro is in foreground

---

## Next Steps

Once you have "play" working:

1. **Test other commands:**
   ```bash
   python src/main.py --command "stop"
   python src/main.py --command "record"
   python src/main.py --command "metronome on"
   ```

2. **Improve accuracy:**
   - Adjust prompts in vision.py
   - Add more context about Logic Pro UI
   - Handle edge cases

3. **Add voice input** (Phase 2 from CLAUDE.md)
   - Install speech_recognition
   - Add continuous listening
   - Integrate with agent

---

## Learning Reflections

After completing Phase 1-7, you should understand:

- ✅ How to structure a Python application
- ✅ API integration with Anthropic Claude
- ✅ Computer vision for GUI understanding
- ✅ Cursor automation with PyAutoGUI
- ✅ The agent loop: Sense → Think → Act
- ✅ Error handling and debugging
- ✅ Prompt engineering for vision models

**Questions to think about:**
- What are the limitations of this approach?
- How could you make it faster?
- What if Logic Pro UI changes?
- How would you add more complex commands?

---

## Getting Help

- **Read the code comments** - Lots of hints!
- **Check CLAUDE.md** - Architecture details
- **Print debugging** - Add print() everywhere
- **Test incrementally** - One function at a time
- **Experiment** - Try changing prompts and see what happens

---

**Ready? Start with Phase 1!** 🚀

Remember: The goal is to LEARN, not just to finish. Take your time, experiment, and have fun!
