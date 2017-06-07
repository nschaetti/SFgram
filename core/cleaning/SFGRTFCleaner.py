
from .SFGCleaner import SFGCleaner


# RTF cleaner
class SFGRTFCleaner(SFGCleaner):

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(SFGRTFCleaner, self).__init__()
    # end __init__

    # Clean text
    def __call__(self, text):
        """
        Clean text.
        :param text: Text to clean.
        :return: Dictionary with text and informations.
        """
        print("RTF " + text)
        # end __call__

# end SFGRTFCleaner
