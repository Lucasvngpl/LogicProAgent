"""
Claude Vision API integration for understanding Logic Pro UI.

LEARNING GOALS:
- Learn how to call the Anthropic Claude API
- Understand vision model capabilities
- Practice prompt engineering for GUI understanding
- Handle API responses and errors
"""

from anthropic import Anthropic
from typing import Dict, List, Optional
import json


class VisionAnalyzer:
    """Uses Claude Vision to understand Logic Pro interface."""

    def __init__(self, api_key: str):
        """
        Initialize the vision analyzer.

        TODO: Implement this
        Hints:
        - Create Anthropic client with api_key
        - Store it as self.client

        Args:
            api_key: Anthropic API key
        """
        pass

    def analyze_ui_for_command(
        self,
        screenshot_base64: str,
        user_command: str
    ) -> Dict:
        """
        Analyze Logic Pro screenshot to find how to execute a command.

        TODO: Implement this method
        This is the CORE of the project!

        Hints:
        - Use self.client.messages.create()
        - Model: "claude-opus-4-6" (most capable for vision)
        - Max tokens: ~1000 should be enough
        - Message content should include:
          1. The image (type: "image", source with base64 data)
          2. The prompt (type: "text")

        Prompt engineering tips:
        - Be specific about what you need
        - Ask for JSON format response
        - Request coordinates (x, y) for clicks
        - Ask for step-by-step actions if multi-step
        - Include context about Logic Pro

        Example prompt structure:
        '''
        You are analyzing a Logic Pro interface screenshot.
        The user wants to: "{user_command}"

        Analyze the interface and return a JSON response with:
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
          "reasoning": "Explanation of what you're doing"
        }}

        Be precise with coordinates.
        '''

        Args:
            screenshot_base64: Base64 encoded screenshot
            user_command: What the user wants to do (e.g., "play", "record")

        Returns:
            Dict with 'steps' and 'reasoning'
        """
        # TODO: Your implementation here
        pass

    def parse_response(self, response) -> Dict:
        """
        Parse Claude's API response into structured actions.

        TODO: Implement this
        Hints:
        - Extract text content from response
        - Parse JSON if it's JSON
        - Handle errors gracefully
        - Return a dict with 'steps' list

        Args:
            response: Raw API response from Claude

        Returns:
            Parsed dict with actions
        """
        pass


# Example usage / test
def test_vision():
    """
    Test the vision analyzer.

    TODO: Implement this test
    - You'll need an API key
    - You'll need a screenshot
    - Try analyzing for command "play"
    - Print the results
    """
    print("Testing vision analyzer...")

    # Get API key from environment or hardcode for testing
    api_key = "your-api-key-here"  # TODO: Load from environment

    # TODO: Your test code here


if __name__ == "__main__":
    test_vision()
