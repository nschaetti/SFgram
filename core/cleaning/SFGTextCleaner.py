
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
        print(self.get_author(text))
        print("")
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

    # Get document's ID
    def get_id(self, text):
        """
        Get document's id
        :param text:
        :return:
        """
        title = ""

        # Possible regex
        regex = [r"^Title: ([\w \.:'\-\"]+)", r"^The Project Gutenberg EBook of ([\w \.:'\-\"]+)",
                 r"^Project Gutenberg Etext of ([\w \.:'\-\"]+)", r"^Project Gutenberg Etext:  ([\w \.:'\-\"]+)",
                 r"^The Project Gutenberg Etext of ([\w \.:'\-\"]+)"]

        # For each regex
        for r in regex:
            title_field = self._get_regex_value(r, text)
            if title_field is not None:
                return title_field
            # end if
        # end for
    # end get_title

    # Get document's title
    def get_title(self, text):
        """
        Get document's title
        :param text:
        :return:
        """
        title = ""

        # Possible regex
        regex = [r"^Title: ([\w \.:'\-\"]+)", r"^The Project Gutenberg EBook of ([\w \.:'\-\"]+)",
                 r"^Project Gutenberg Etext of ([\w \.:'\-\"]+)", r"^Project Gutenberg Etext:  ([\w \.:'\-\"]+)",
                 r"^The Project Gutenberg Etext of ([\w \.:'\-\"]+)"]

        # For each regex
        for r in regex:
            title_field = self._get_regex_value(r, text)
            if title_field is not None:
                return title_field
            # end if
        # end for
    # end get_title

    # Get document's author
    def get_author(self, text):
        """
        Get document's author
        :param text:
        :return:
        """
        author = ""

        # Possible regex
        regex = [r"^Author: ([\w \.']+)", r"by ([\w \.']+)"]

        # For each regex
        for r in regex:
            author_field = self._get_regex_value(r, text)
            if author_field is not None:
                return author_field
            # end if
        # end for
    # end get_author

# SFGFileCleaner
