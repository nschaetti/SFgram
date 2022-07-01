
# Imports
from mongoengine import *
from archives.db.BookIterator import BookIterator
from archives.db.Country import Country
from archives.db.Author import Author


# SFGram connector
class SFGramConnector(object):
    """
    The SFGram database connector
    """

    # Constructor
    def __init__(self, database_name):
        # Connection to MongoDB
        connect(database_name)
    # end __init__

    # Get books
    def get_books(self, **kwargs):
        """
        Get books
        :param properties: Properties to filter.
        :param author: Book's author or none.
        :param country: Book's country or none.
        :return: A book iterator
        """
        # Author and country
        author = kwargs.get('author', None)
        country = kwargs.get('country', None)

        # If author given
        author_object = None
        if author is not None:
            author_object = Author.get_by_name(author)
            kwargs['author'] = author_object
        else:
            kwargs['author'] = None
        # end if

        # If country given
        country_object = None
        if country_object is not None:
            country_object = Country.get_by_name(country)
            kwargs['country'] = country_object
        else
            kwargs['country'] = None
        # end if

        # Return a book iterator
        return BookIterator(kwargs)
    # end get_books

# end SFGramConnector
