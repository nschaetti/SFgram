# -*- coding: utf-8 -*-
#

from mongoengine import *
from .Image import Image


# A book in the MongoDB database
class Book(Document):
    """
    A book in the MongoDB database
    """

    # Fields
    num = IntField()
    ambiguation = BooleanField()
    author = ReferenceField("Author")
    authors = ListField(ReferenceField("Author"))
    average_rating = FloatField()
    category = StringField(max_length=20)
    cleaned = BooleanField()
    content = StringField()
    content_available = BooleanField()
    content_tokens = IntField()
    copyright = StringField()
    country = ReferenceField("Country", default=None)
    cover = ReferenceField("Image")
    covert_art = ReferenceField("Image")
    cover_artist = StringField(max_length=100)
    description = StringField()
    format = StringField()
    genres = ListField(ReferenceField("Genre"))
    goodreads_publication_date = IntField()
    goodreads_url = StringField()
    goodreads_found = BooleanField()
    ISBN = StringField(max_length=10)
    ISBN13 = StringField(max_length=13)
    images = ListField(ReferenceField("Image"))
    language = StringField()
    language_code = StringField()
    loc_class = StringField()
    original_title = StringField()
    pages = IntField()
    publication_date = IntField()
    rating_count = IntField()
    release_date = DateTimeField()
    similar_books = ListField(StringField())
    small_image = ReferenceField("Image")
    summary = StringField()
    title = StringField(max_length=100)
    wikipedia_publication_date = IntField()
    wikipedia_url = StringField()
    wikipedia_found = BooleanField()

    # Does the book exists
    @staticmethod
    def exists(book_title):
        books = Book.objects(title=book_title)
        return books.count() > 0
    # end exists

    # Get book from title
    @staticmethod
    def get_by_title(book_title):
        """
        Get book from its title
        :param book_title:
        :return:
        """
        books = Book.objects(title=book_title)
        if books.count() > 0:
            return books[0]
        else:
            return None
        # end if
    # end get_by_title

# end Book
