"""
Command definitions and natural language processing.

LEARNING GOALS:
- Understand command pattern matching
- Learn basic NLP techniques
- Practice data structures for command mapping
"""

from typing import Optional, List


class CommandProcessor:
    """Processes natural language commands into standardized intents."""

    def __init__(self):
        """
        Initialize command processor.

        TODO: Think about what data structures you need
        - How will you map different phrases to the same command?
        - "play", "hit play", "start playing" → all mean PLAY
        """
        # Define command patterns
        # TODO: Fill this in
        self.command_patterns = {
            "play": ["play", "start", "hit play", "start playing"],
            "stop": ["stop", "pause", "halt"],
            "record": ["record", "hit record", "start recording"],
            "metronome_on": ["metronome on", "click on", "turn on metronome"],
            "metronome_off": ["metronome off", "click off", "turn off metronome"],
        }

    def parse_command(self, user_input: str) -> Optional[str]:
        """
        Parse user's natural language into a standard command.

        TODO: Implement this
        Hints:
        - Convert user_input to lowercase
        - Check if it matches any pattern
        - Return the command key (e.g., "play", "record")
        - Return None if no match

        Challenge: How to handle partial matches?
        - "can you play it" should match "play"
        - Use string contains? Fuzzy matching?

        Args:
            user_input: Raw text from user

        Returns:
            Standard command string or None
        """
        pass

    def get_command_description(self, command: str) -> str:
        """
        Get a human-readable description of what a command does.

        TODO: Implement this
        Useful for confirmation messages:
        - "Playing track..."
        - "Starting recording..."

        Args:
            command: Standard command string

        Returns:
            Human description
        """
        descriptions = {
            "play": "Playing track",
            "stop": "Stopping playback",
            "record": "Starting recording",
            "metronome_on": "Turning on metronome",
            "metronome_off": "Turning off metronome"
        }
        # TODO: Return appropriate description
        pass

    def is_valid_command(self, command: str) -> bool:
        """
        Check if a command is valid.

        TODO: Implement this
        Simple: check if command is in self.command_patterns

        Args:
            command: Command to validate

        Returns:
            True if valid
        """
        pass


# Test function
def test_commands():
    """
    Test command processing.

    TODO: Implement this
    Test cases:
    - "play" → should parse to "play"
    - "can you hit play please" → should parse to "play"
    - "start recording" → should parse to "record"
    - "xyz123" → should return None
    """
    print("Testing command processor...")

    processor = CommandProcessor()

    # Test cases
    test_inputs = [
        "play",
        "can you play",
        "record",
        "asdfasdf",  # Invalid
        "metronome on"
    ]

    # TODO: Test each input and print results


if __name__ == "__main__":
    test_commands()
