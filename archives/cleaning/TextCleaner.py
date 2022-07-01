# -*- coding: utf-8 -*-
#

import sys
import re
from .SFGCleaner import SFGCleaner

reload(sys)
sys.setdefaultencoding('utf8')


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
        if u"START OF THIS PROJECT GUTENBERG" in unicode(text).upper():
            # Split by lines
            lines = text.split(u'\r\n')

            # For each line
            result = list()
            save = False
            for line in lines:
                # Check if we passe the end ebbok tag
                if u"END OF THIS PROJECT GUTENBERG" in unicode(line).upper() or \
                                u"end of project gutenberg's" in unicode(line).lower() or \
                                u"end of the project gutenberg" in unicode(line).lower():
                    save = False
                # end if

                # Save line
                if save and len(line) > 0 and line != u"\n" and line != u"\r\n" and line != u"\n\r"\
                        and line != u"\u000A\u000D" and line[0] != chr(1) and line[0] != u"\r":
                    result.append(line)
                # end if

                # Check if we pass the start ebook tag
                if u"START OF THIS PROJECT GUTENBERG" in unicode(line).upper():
                    save = True
                # end if
            # end for

            # Join
            joined_text = u'\n'.join(result)

            # Remove useless character
            joined_text = joined_text.replace(u"\r", u" ")              # No \r
            joined_text = joined_text.replace(u"\n\n", u"\n")           # No newline
            joined_text = joined_text.replace(u"\n\n", u"\n")           # No newline
            joined_text = joined_text.replace(u"\t", u" ")              # No tab
            joined_text = joined_text.replace(u"  ", u" ")              # Double space
            joined_text = joined_text.replace(u"   ", u" ")             # Triple space
            joined_text = joined_text.replace(u"    ", u" ")            # Quadruple space

            # Return
            return joined_text, True
        else:
            return text, False
        # end if
    # end __call__

# SFGFileCleaner
