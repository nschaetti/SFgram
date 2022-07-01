
from .SFGCleaner import SFGCleaner


# HTML file cleaner
class SFGHTMLCleaner(SFGCleaner):
    """
    HTML file cleaner
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(SFGHTMLCleaner, self).__init__()
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

# end SFGHTMLCleaner
