
import re
from .SFGCleaner import SFGCleaner


# Clean file from project Gutenberg
class TextCleaner(SFGCleaner):
    """
    Clean file from project Gutenberg.
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(TextCleaner, self).__init__()
    # end __init__

    # Clean text
    def __call__(self, text):
        """
        Clean text.
        :param text: Text to clean.
        :return: Dictionary with text and information.
        """
        # Check if the default marker is here
        if u"*** START OF THIS PROJECT GUTENBERG" in text.upper():
            # Split by lines
            lines = text.split('\n')

            # For each line
            result = list()
            save = False
            for line in lines:
                # Check if we passe the end ebbok tag
                if u"*** END OF THIS PROJECT GUTENBERG" in line.upper() or u"End of Project Gutenberg's" in line or u"End of the Project Gutenberg" in line:
                    save = False
                # end if

                # Save line
                if save and len(line) > 0 and line != u"\n" and line != u"\r\n" and line != u"\n\r"\
                        and line != u"\u000A\u000D" and line[0] != chr(1) and line[0] != u"\r":
                    result.append(line)
                # end if

                # Check if we pass the start ebook tag
                if u"*** START OF THIS PROJECT GUTENBERG" in line.upper():
                    save = True
                # end if
            # end for
            return u'\n'.join(result), True
        else:
            return text, False
        # end if
    # end __call__

# SFGFileCleaner
