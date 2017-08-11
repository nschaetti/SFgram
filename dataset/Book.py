# -*- coding: utf-8 -*-
#

# Imports


# A book in the dataset
class Book(object):
    """
    A book in the dataset
    """

    # Fields
    author = None
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
    cover_art = ""
    cover_art_url = ""
    cover_artist = ""
    description = ""
    format = ""
    genres = list()
    gutenberg = {'url': u"", 'num': 0}
    goodreads = {'year': 0, 'url': u"", 'found': False}
    id = 0
    images = list()
    images_urls = list()
    ISBN = ""
    ISBN13 = ""
    language = ""
    language_code = ""
    loc_class = ""
    num = -1
    original_title = ""
    pages = 0
    publication_date = 0
    rating_count = 0
    release_date = None
    similar_books = list()
    small_image = ""
    summary = ""
    title = ""
    wikipedia = {'year': 0, 'ambiguation': False, 'url': u"", 'found': False}
    year = 0

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self.authors = list()
        self.country = list()
        self.genres = list()
        self.images = list()
        self.images_urls = list()
        self.similar_books = list()
    # end __init__

# end Book
