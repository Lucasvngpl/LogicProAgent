"""
Voice input using OpenAI Realtime API with built-in VAD.

How it works:
1. Opens a WebSocket to OpenAI's Realtime API
2. Streams microphone audio continuously
3. OpenAI's server VAD detects when you start/stop talking
4. Sends back transcription only when speech is detected
5. We check for "Hey Logic" and extract the command

No local VAD model needed -- OpenAI handles speech detection server-side.

LEARNING GOALS:
- Understand WebSocket streaming for real-time audio
- Learn OpenAI's Realtime API for transcription
- Practice wake word detection
- Handle real-time audio input
"""

import os
import json
import base64
import threading
import numpy as np
import sounddevice as sd
from typing import Optional
import websocket

# Audio settings — Realtime API requires 24kHz mono PCM16
SAMPLE_RATE = 24000
CHANNELS = 1

# Wake word — say this before your command
WAKE_WORD = "hey logic"

# Realtime API endpoint
REALTIME_URL = "wss://api.openai.com/v1/realtime"
REALTIME_MODEL = "gpt-4o-mini-transcribe"


class VoiceInput:
    """Handles voice input using OpenAI Realtime API with server-side VAD."""

    def __init__(self):
        """
        Initialize voice input.

        TODO: Implement this
        Hints:
        - Get API key from OPENAI_API_KEY env var
        - Store it for WebSocket auth header
        - Initialize a variable to hold the latest transcription

        Example:
            self.api_key = os.environ.get("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self.latest_transcript = None
            self._ws = None
            self._running = False
        """
        print("Initializing OpenAI Realtime voice input...")
        # TODO: Your implementation here
        pass

    def _create_session_config(self) -> dict:
        """
        Create the session configuration for transcription + server VAD.

        TODO: Implement this
        Hints:
        - Return a session.update event that configures:
          - Transcription model (gpt-4o-mini-transcribe)
          - Server VAD with threshold 0.5 and 1 second silence duration
          - 24kHz PCM audio input format

        Example:
            return {
                "type": "session.update",
                "session": {
                    "input_audio_transcription": {
                        "model": REALTIME_MODEL,
                    },
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "silence_duration_ms": 1000,
                        "prefix_padding_ms": 300,
                    },
                }
            }
        """
        # TODO: Your implementation here
        pass

    def _on_message(self, ws, message):
        """
        Handle incoming WebSocket messages from OpenAI.

        TODO: Implement this
        Hints:
        - Parse the JSON message
        - Look for "conversation.item.input_audio_transcription.completed" events
        - Extract the "transcript" field
        - Store it in self.latest_transcript
        - Close the WebSocket so listen_for_command() returns

        Example:
            data = json.loads(message)
            if data.get("type") == "conversation.item.input_audio_transcription.completed":
                self.latest_transcript = data.get("transcript", "")
                print(f"  Heard: {self.latest_transcript}")
                self._running = False
                ws.close()
        """
        # TODO: Your implementation here
        pass

    def _on_open(self, ws):
        """
        Called when WebSocket connects. Send session config and start streaming mic.

        TODO: Implement this
        Hints:
        - Send the session config
        - Start a background thread that reads mic audio and sends it

        Example:
            ws.send(json.dumps(self._create_session_config()))
            self._mic_thread = threading.Thread(target=self._stream_mic, args=(ws,))
            self._mic_thread.daemon = True
            self._mic_thread.start()
        """
        # TODO: Your implementation here
        pass

    def _stream_mic(self, ws):
        """
        Continuously read mic audio and send to OpenAI via WebSocket.

        TODO: Implement this
        Hints:
        - Use sd.InputStream to read audio chunks
        - Record as int16 (PCM16) directly — that's what Realtime API expects
        - Base64-encode the bytes (WebSocket needs text)
        - Send as input_audio_buffer.append event
        - Use a block size of ~4800 samples (200ms at 24kHz)

        Example:
            block_size = 4800  # 200ms at 24kHz
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                                dtype='int16', blocksize=block_size) as stream:
                while self._running:
                    audio_data, _ = stream.read(block_size)
                    audio_bytes = audio_data.tobytes()
                    b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
                    event = {
                        "type": "input_audio_buffer.append",
                        "audio": b64_audio,
                    }
                    try:
                        ws.send(json.dumps(event))
                    except:
                        break
        """
        # TODO: Your implementation here
        pass

    def check_wake_word(self, text: str) -> Optional[str]:
        """
        Check if text contains the wake word and extract the command.

        TODO: Implement this
        Hints:
        - Check if text.lower() contains WAKE_WORD
        - If found, return everything after the wake word
        - If not found, return None

        Example:
            "hey logic play" -> "play"
            "hey logic open chromaverb" -> "open chromaverb"
            "testing one two" -> None

        Args:
            text: Transcribed text to check

        Returns:
            Command text (without wake word) or None
        """
        # TODO: Your implementation here
        pass

    def listen_for_command(self) -> Optional[str]:
        """
        Connect to Realtime API and wait for next voice command.

        This is the main method that main.py calls in a loop.

        TODO: Implement this
        Hints:
        - Reset self.latest_transcript to None
        - Set self._running = True
        - Connect WebSocket with auth headers
        - run_forever() blocks until ws.close() is called (from _on_message)
        - After it returns, check wake word in the transcript

        Example:
            self.latest_transcript = None
            self._running = True
            url = f"{REALTIME_URL}?model={REALTIME_MODEL}"
            ws = websocket.WebSocketApp(
                url,
                header=[
                    f"Authorization: Bearer {self.api_key}",
                    "OpenAI-Beta: realtime=v1",
                ],
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=lambda ws, e: print(f"  WebSocket error: {e}"),
            )
            ws.run_forever()

            if self.latest_transcript:
                return self.check_wake_word(self.latest_transcript)
            return None

        Returns:
            Command text or None if no wake word detected
        """
        # TODO: Your implementation here
        pass

    def stop(self):
        """Stop listening and close WebSocket."""
        self._running = False
        if self._ws:
            self._ws.close()


def test_voice():
    """
    Test voice input.

    TODO: Implement this test
    - Create VoiceInput (needs OPENAI_API_KEY env var)
    - Call listen_for_command() in a loop
    - Say "Hey Logic play" and verify it returns "play"
    """
    print("Testing voice input with OpenAI Realtime API...")
    print("Say 'Hey Logic' followed by a command.")
    print("Press Ctrl+C to stop.\n")

    # TODO: Your test code here
    # voice = VoiceInput()
    # while True:
    #     try:
    #         print("Listening...")
    #         command = voice.listen_for_command()
    #         if command:
    #             print(f"Command: {command}")
    #     except KeyboardInterrupt:
    #         voice.stop()
    #         print("\nDone.")
    #         break


if __name__ == "__main__":
    test_voice()
