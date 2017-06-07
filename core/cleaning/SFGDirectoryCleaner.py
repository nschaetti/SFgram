
from .SFGCleaner import SFGCleaner


# Directory cleaner
class SFGDirectoryCleaner(SFGCleaner):
    """
    Directory cleaner
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        pass
    # end __init__

    # Clean text
    def __call__(self, text):
        """
        Clean text.
        :param text: Text to clean.
        :return: Dictionary with text and informations.
        """
        print("DIR " + text)
        # Split lines
        """for line in text.split('\n'):
            m = re.search("$Title : (\w+)")
            print(m.group(0))"""
        # end for
    # end __call__

# end SFGDirectoryCleaner
