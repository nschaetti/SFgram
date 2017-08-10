# -*- coding: utf-8 -*-
#

# Imports
import datetime


# A book in the MongoDB database
class Book(object):
    """
    A book in the dataset
    """

    # Fields
    num = -1
    ambiguation = False
    author = ""
    authors = list()
    average_rating = -1.0
    category = ""
    cleaned = False
    content = ""
    content_available = False
    content_tokens = 0
    copyright = ""
    country = list()
    cover = ""
    covert_art = ""
    cover_artist = ""
    description = ""
    format = ""
    genres = list()
    goodreads = {'publication_date': 0, 'url': u"", 'found': False}
    images = list()
    ISBN = ""
    ISBN13 = ""
    language = ""
    language_code = ""
    loc_class = ""
    original_title = ""
    pages = 0
    publication_date = 0
    rating_count = 0
    release_date = None
    similar_books = list()
    small_image = ""
    summary = ""
    title = ""
    wikipedia = {'publication_year': 0, 'url': u"", 'found': False}

    ####################################################
    # Static
    ####################################################

    # Does the book exists
    @staticmethod
    def exists(book_title):
        pass
    # end exists

    # Get book from title
    @staticmethod
    def get_by_title(book_title):
        """
        Get book from its title
        :param book_title:
        :return:
        """
        pass
    # end get_by_title

# end Book
