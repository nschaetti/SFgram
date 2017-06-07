
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
        :return: Dictionary with text and information.
        """
        print(self.get_title(text))
    # end __call__

    # Get regex value of first group
    def _get_regex_value(self, pattern, text):
        """
        Get regex value of first group
        :param pattern:
        :param text:
        :return:
        """
        match = re.search(pattern, text, flags=re.MULTILINE)
        if match is not None:
            return match.groups(0)[0]
        # end if
        return None
    # end get_regex_value

    def get_title(self, text):
        title = ""

        # Possible regex
        regex = [r"^Title: ([\w \.:']+)", r"^The Project Gutenberg EBook of ([\w ]+)",
                 r"^Project Gutenberg Etext of ([\w ]+)", r"^Project Gutenberg Etext:  ([\w ]+)",
                 r"^The Project Gutenberg Etext of ([\w ]+)"]

        # For each regex
        for r in regex:
            title_field = self._get_regex_value(r, text)
            if title_field is not None:
                return title_field
            # end if
        # end for

    # end get_title

# SFGFileCleaner
