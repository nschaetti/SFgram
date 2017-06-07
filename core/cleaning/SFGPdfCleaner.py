
from .SFGCleaner import SFGCleaner


# PDF cleaner
class SFGPdfCleaner(SFGCleaner):
    """
    PDF cleaner
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(SFGPdfCleaner, self).__init__()
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

# end SFGPdfCleaner
