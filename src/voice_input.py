"""
Voice input using faster-whisper for local speech-to-text.

Runs Whisper locally on your Mac — no API costs, no internet needed.
Uses the 'base.en' model (best speed/accuracy tradeoff for short commands).

LEARNING GOALS:
- Understand speech-to-text processing
- Learn audio recording with sounddevice
- Practice wake word detection
- Handle real-time audio input
"""

import numpy as np
import sounddevice as sd
import tempfile
import wave
import os
from typing import Optional

# Local Whisper inference — 4x faster than openai-whisper
# pip install faster-whisper
from faster_whisper import WhisperModel

# Model size — 'base.en' is ideal for short voice commands
# Options: tiny.en (fastest), base.en (recommended), small.en (more accurate)
WHISPER_MODEL = "base.en"

# Audio settings
SAMPLE_RATE = 16000  # Whisper expects 16kHz audio
CHANNELS = 1         # Mono audio

# Wake word — say this before your command
WAKE_WORD = "hey logic"


class VoiceInput:
    """Handles voice input using local Whisper model."""

    def __init__(self, model_size: str = WHISPER_MODEL):
        """
        Initialize voice input with local Whisper model.

        TODO: Implement this
        Hints:
        - Create WhisperModel with model_size
        - Use device="cpu" and compute_type="float32" for Mac
        - Store as self.model
        - Also store sample rate and other config

        Example:
            self.model = WhisperModel(
                model_size, device="cpu", compute_type="float32"
            )

        Args:
            model_size: Whisper model to use (default: "base.en")
        """
        print(f"Loading Whisper model: {model_size}")
        # TODO: Your implementation here
        pass

    def record_audio(self, duration: float = 5.0) -> np.ndarray:
        """
        Record audio from microphone for a fixed duration.

        TODO: Implement this
        Hints:
        - Use sounddevice.rec() to record
        - Parameters: frames = int(duration * SAMPLE_RATE)
        - Use samplerate=SAMPLE_RATE, channels=CHANNELS
        - dtype='float32'
        - Call sd.wait() to block until recording is done
        - Return the audio array

        Example:
            audio = sd.rec(
                int(duration * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype='float32'
            )
            sd.wait()
            return audio.flatten()

        Args:
            duration: How long to record in seconds

        Returns:
            Numpy array of audio samples
        """
        # TODO: Your implementation here
        pass

    def record_until_silence(
        self,
        silence_threshold: float = 0.01,
        silence_duration: float = 1.5,
        max_duration: float = 10.0
    ) -> np.ndarray:
        """
        Record audio until silence is detected.

        TODO: Implement this (ADVANCED)
        Hints:
        - Record in small chunks (e.g., 0.5 seconds)
        - Check if the chunk's volume is below silence_threshold
        - If silence lasts >= silence_duration, stop recording
        - Stop after max_duration regardless
        - Concatenate all chunks with np.concatenate()

        This is trickier than fixed-duration recording!
        Start with record_audio() first, then try this.

        Args:
            silence_threshold: Volume level that counts as silence
            silence_duration: How long silence must last to stop (seconds)
            max_duration: Maximum recording time (seconds)

        Returns:
            Numpy array of audio samples
        """
        # TODO: Your implementation here (start with record_audio first)
        pass

    def transcribe(self, audio: np.ndarray) -> str:
        """
        Transcribe audio using local Whisper model.

        TODO: Implement this
        Hints:
        - Save audio to a temp WAV file (Whisper needs a file path)
        - Use self.model.transcribe(temp_file_path)
        - transcribe() returns (segments, info)
        - Join all segment texts together
        - Clean up the temp file
        - Return the transcribed text

        Example:
            segments, info = self.model.transcribe(audio_path)
            text = " ".join([seg.text for seg in segments])
            return text.strip()

        Args:
            audio: Numpy array of audio samples

        Returns:
            Transcribed text string
        """
        # TODO: Your implementation here
        pass

    def _save_audio_to_wav(self, audio: np.ndarray, path: str):
        """
        Save numpy audio array to WAV file.

        TODO: Implement this helper
        Hints:
        - Use the wave module
        - Convert float32 audio to int16 (multiply by 32767)
        - Write with wave.open(path, 'w')
        - Set params: nchannels=1, sampwidth=2, framerate=SAMPLE_RATE

        Args:
            audio: Numpy audio array (float32, -1 to 1)
            path: Where to save the WAV file
        """
        # TODO: Your implementation here
        pass

    def check_wake_word(self, text: str) -> Optional[str]:
        """
        Check if text contains the wake word and extract the command.

        TODO: Implement this
        Hints:
        - Check if text.lower() starts with or contains WAKE_WORD
        - If found, return everything after the wake word
        - If not found, return None

        Example:
            "hey logic play" → "play"
            "hey logic hit record" → "hit record"
            "what time is it" → None

        Args:
            text: Transcribed text to check

        Returns:
            Command text (without wake word) or None
        """
        # TODO: Your implementation here
        pass

    def listen_for_command(self, duration: float = 5.0) -> Optional[str]:
        """
        Listen for a voice command (record + transcribe + check wake word).

        TODO: Implement this
        Hints:
        - Call record_audio() or record_until_silence()
        - Call transcribe() on the audio
        - Call check_wake_word() on the text
        - Return the command or None

        This is the main method that main.py will call.

        Args:
            duration: How long to listen

        Returns:
            Command text or None if no wake word detected
        """
        # TODO: Your implementation here
        pass


def test_voice():
    """
    Test voice input.

    TODO: Implement this test
    - Create VoiceInput
    - Record a few seconds of audio
    - Transcribe it
    - Print the result
    - Try saying "Hey Logic play" and check wake word detection
    """
    print("Testing voice input...")
    print("Speak into your microphone after the beep!")

    # TODO: Your test code here
    # voice = VoiceInput()
    # audio = voice.record_audio(duration=5.0)
    # text = voice.transcribe(audio)
    # print(f"You said: {text}")
    # command = voice.check_wake_word(text)
    # print(f"Command: {command}")


if __name__ == "__main__":
    test_voice()
