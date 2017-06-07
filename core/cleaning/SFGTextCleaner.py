
import re
from .SFGCleaner import SFGCleaner


# Clean file from project Gutenberg
class SFGTextCleaner(SFGCleaner):
    """
    Clean file from project Gutenberg.
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(SFGTextCleaner, self).__init__()
    # end __init__

    # Clean text
    def __call__(self, text):
        """
        Clean text.
        :param text: Text to clean.
        :return: Dictionary with text and informations.
        """
        print("TEXT " + text)
        # Split lines
        """for line in text.split('\n'):
            m = re.search("$Title : (\w+)")
            print(m.group(0))"""
        # end for
    # end __call__

# SFGFileCleaner
