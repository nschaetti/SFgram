# -*- coding: utf-8 -*-
#

# Imports


# An author in the dataset
class Author(object):
    """
    An author in the dataset
    """

    # Fields
    id = 0
    birth_date = None
    death_date = None
    name = ""
    books = list()
    bio = ""
    summary = ""
    wikipedia = {'ambiguation': False, 'url': u"", 'found': False}
    n_books = 0

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self.books = list()
    # end __init__

# end Book
