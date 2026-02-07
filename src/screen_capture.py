"""
Screen capture utilities for capturing Logic Pro window.

LEARNING GOALS:
- Understand how to take screenshots programmatically
- Learn PIL/Pillow image handling
- Practice encoding images for API transmission
"""

import pyautogui
from PIL import Image
import io
import base64
from typing import Optional


class ScreenCapture:
    """Handles screenshot capture of Logic Pro window."""

    def __init__(self):
        """Initialize screen capture."""
        # TODO: Research PyAutoGUI failsafe feature
        # Should we enable it during development? Why or why not?
        pass

    def capture_screen(self, save_path: Optional[str] = None) -> Image.Image:
        """
        Capture the entire screen.

        TODO: Implement this method
        Hints:
        - Use pyautogui.screenshot()
        - Return a PIL Image object
        - Optionally save to save_path if provided
        - Print confirmation when saved

        Args:
            save_path: Optional path to save screenshot

        Returns:
            PIL Image object
        """
        pass

    def image_to_base64(self, image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string for API transmission.

        TODO: Implement this method
        Hints:
        - Create a BytesIO buffer
        - Save image to buffer as PNG
        - Get bytes from buffer
        - Use base64.b64encode()
        - Decode to string with .decode('utf-8')

        Why do we need this?
        - Claude API expects images as base64 strings
        - This is a common format for transmitting binary data over text protocols

        Args:
            image: PIL Image object

        Returns:
            Base64 encoded string
        """
        pass

    def capture_and_encode(self, save_path: Optional[str] = None) -> tuple[Image.Image, str]:
        """
        Capture screen and return both image and base64 encoding.

        TODO: Implement this method
        Hints:
        - Call capture_screen()
        - Call image_to_base64()
        - Return both

        Args:
            save_path: Optional path to save screenshot

        Returns:
            Tuple of (PIL Image, base64 string)
        """
        pass


# Test function
def test_capture():
    """
    Test function to verify screen capture works.

    TODO: Implement this
    - Create ScreenCapture instance
    - Capture a screenshot
    - Save it to data/screenshots/test_capture.png
    - Print the image dimensions
    - Print the base64 string length
    """
    print("Testing screen capture...")
    # Your code here


if __name__ == "__main__":
    # When you run: python src/screen_capture.py
    # This will execute
    test_capture()
