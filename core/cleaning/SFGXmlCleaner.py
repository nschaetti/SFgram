
from .SFGCleaner import SFGCleaner


# XML cleaner
class SFGLitCleaner(SFGCleaner):

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(SFGLitCleaner, self).__init__()
    # end __init__

    # Clean text
    def __call__(self, text):
        """
        Clean text.
        :param text: Text to clean.
        :return: Dictionary with text and informations.
        """
        print("XML " + text)
        # end __call__

# end SFGRTFCleaner
