
from .SFGCleaner import SFGCleaner


# XML cleaner
class SFGXmlCleaner(SFGCleaner):
    """
    XML File Cleaner
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(SFGXmlCleaner, self).__init__()
    # end __init__

    # Clean text
    def __call__(self, text):
        """
        Clean text.
        :param text: Text to clean.
        :return: Dictionary with text and informations.
        """
        pass
        # end __call__

# end SFGRTFCleaner
