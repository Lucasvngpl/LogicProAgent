"""
Text-to-Speech using OpenAI's TTS API.

Uses the same OpenAI API key as voice input (STT), so no extra keys needed.

LEARNING GOALS:
- Understand streaming audio from an API
- Practice error handling with external services
"""

import os
import subprocess
import tempfile

from openai import OpenAI


class TextToSpeech:
    """Text-to-speech using OpenAI API."""

    def __init__(self, voice: str = "coral"):
        """
        Initialize TTS.

        Args:
            voice: OpenAI voice to use. Options: alloy, ash, ballad, coral,
                   echo, fable, nova, onyx, sage, shimmer, verse, marin, cedar.
        """
        self.voice = voice
        self.model = "gpt-4o-mini-tts"
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print(f"  TTS: OpenAI {self.model} (voice: {self.voice})")

    def speak(self, text: str, instructions: str = None):
        """
        Speak the given text aloud.

        Args:
            text: Text to speak.
            instructions: Optional tone/style instructions
                          (e.g. "Speak in a friendly, casual tone").
        """
        if not text:
            return

        kwargs = {
            "model": self.model,
            "voice": self.voice,
            "input": text,
            "response_format": "mp3",
        }
        if instructions:
            kwargs["instructions"] = instructions

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            temp_path = f.name

        try:
            with self.client.audio.speech.with_streaming_response.create(**kwargs) as response:
                response.stream_to_file(temp_path)

            # Play with afplay (macOS built-in)
            subprocess.run(["afplay", temp_path], check=True)
        finally:
            os.unlink(temp_path)
