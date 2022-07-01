
# Imports
from archives.db.Book import Book


# Book Iterator
class BookIterator(object):
    """
    Book Iterator
    """

    # Constructor
    def __init__(self, **kwargs):
        """
        Constructor
        :param **kwargs: Properties
        """
        self._iterator = Book.objects(kwargs)
    # end __init__

    # Iterator
    def __iter__(self):
        return self
    # end __iter__

    # Next element
    def next(self):
        return self._iterator.next()
    # end next

# end BookIterator
