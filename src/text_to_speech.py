"""
Text-to-speech for agent voice responses.

Uses ElevenLabs (free tier: 10k chars/month) for high-quality voice,
with macOS 'say' command as a free unlimited fallback.

LEARNING GOALS:
- Learn text-to-speech API integration
- Understand streaming audio playback
- Practice graceful fallback patterns
- Handle API limits and errors
"""

import subprocess
import os
from typing import Optional

# ElevenLabs TTS — high quality, free tier available
# pip install elevenlabs
# Get your free API key at: https://elevenlabs.io/
from elevenlabs.client import ElevenLabs
from elevenlabs import play


# Pre-defined responses for common commands
# Keeps responses short to save ElevenLabs character quota
COMMAND_RESPONSES = {
    "play": "Sure Lucas, playing now.",
    "stop": "Stopping playback.",
    "record": "Starting recording, go for it!",
    "metronome_on": "Metronome is on.",
    "metronome_off": "Metronome off.",
}

# Default ElevenLabs voice — "George" is a good natural male voice
# Browse voices at: https://elevenlabs.io/voice-library
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

# ElevenLabs model — multilingual v2 is highest quality
DEFAULT_MODEL = "eleven_multilingual_v2"


class TextToSpeech:
    """Handles agent voice responses using ElevenLabs + macOS say fallback."""

    def __init__(self, use_elevenlabs: bool = True):
        """
        Initialize text-to-speech.

        TODO: Implement this
        Hints:
        - If use_elevenlabs is True, try to create an ElevenLabs client
        - Get API key from ELEVENLABS_API_KEY environment variable
        - If no key found, fall back to macOS say
        - Store self.client (ElevenLabs) or None
        - Store self.use_elevenlabs flag

        Example:
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if use_elevenlabs and api_key:
                self.client = ElevenLabs(api_key=api_key)
                self.use_elevenlabs = True
            else:
                self.client = None
                self.use_elevenlabs = False
                print("No ElevenLabs key found, using macOS say")

        Args:
            use_elevenlabs: Whether to try ElevenLabs (default True)
        """
        # TODO: Your implementation here
        pass

    def speak(self, text: str):
        """
        Speak the given text aloud.

        TODO: Implement this
        Hints:
        - If self.use_elevenlabs, use ElevenLabs API
        - Otherwise, fall back to macOS say
        - Wrap ElevenLabs call in try/except — fall back to say on error

        ElevenLabs example:
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=DEFAULT_VOICE_ID,
                model_id=DEFAULT_MODEL,
                output_format="mp3_44100_128"
            )
            play(audio)

        macOS say example:
            subprocess.run(["say", text])

        Args:
            text: Text to speak aloud
        """
        # TODO: Your implementation here
        pass

    def speak_for_command(self, command: str):
        """
        Speak the pre-defined response for a command.

        TODO: Implement this
        Hints:
        - Look up command in COMMAND_RESPONSES
        - If found, call self.speak() with that response
        - If not found, speak a generic response

        Args:
            command: Standard command string (e.g., "play", "record")
        """
        # TODO: Your implementation here
        pass

    def _speak_macos(self, text: str):
        """
        Speak using macOS built-in 'say' command.

        TODO: Implement this
        Hints:
        - Use subprocess.run(["say", text])
        - This is instant, free, and always available on macOS
        - Works offline too!

        Args:
            text: Text to speak
        """
        # TODO: Your implementation here
        pass


def test_tts():
    """
    Test text-to-speech.

    TODO: Implement this test
    - Create TextToSpeech (will try ElevenLabs, fall back to say)
    - Test with a sample response
    - Try both ElevenLabs and macOS say paths

    Quick macOS test (no code needed):
        Open Terminal and run: say "Hello Lucas"
    """
    print("Testing text-to-speech...")

    # TODO: Your test code here
    # tts = TextToSpeech()
    # tts.speak("Sure Lucas, playing now.")
    # tts.speak_for_command("play")


if __name__ == "__main__":
    test_tts()
