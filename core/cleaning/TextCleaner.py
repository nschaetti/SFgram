
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
        if "**** START OF THIS PROJECT GUTENBERG" in text.upper():
            # Split by lines
            lines = text.split('\n')

            # For each line
            result = list()
            save = False
            for line in lines:
                # Check if we passe the end ebbok tag
                if "*** END OF THIS PROJECT GUTENBERG" in line.upper():
                    save = False
                # end if

                # Save line
                if save:
                    result.append(line)
                # end if

                # Check if we pass the start ebook tag
                if "*** START OF THIS PROJECT GUTENBERG" in line.upper():
                    save = True
                # end if
            # end for
            return result.join('\n')
        else:
            return text
        # end if
    # end __call__

# SFGFileCleaner
