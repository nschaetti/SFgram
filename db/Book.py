# -*- coding: utf-8 -*-
#

from mongoengine import *


# A book in the MongoDB database
class Book(Document):
    """
    A book in the MongoDB database
    """

    # Fields
    num = IntField()
    author = ReferenceField("Author")
    authors = ListField(ReferenceField("Author"))
    average_rating = FloatField()
    category = StringField(max_length=20)
    cleaned = BooleanField()
    content = StringField()
    copyright = StringField(max_length=50)
    country = ReferenceField("Country")
    cover = FileField()
    cover_artist = StringField(max_length=50)
    description = StringField()
    format = StringField()
    genres = ListField(ReferenceField("Genre"))
    goodreads_publication_date = IntField()
    goodreads_url = StringField()
    goodreads_found = BooleanField()
    ISBN = StringField(max_length=10)
    ISBN13 = StringField(max_length=13)
    images = ListField(FileField())
    language = StringField()
    language_code = StringField()
    loc_class = StringField()
    original_title = StringField()
    pages = IntField()
    publication_date = IntField()
    rating_count = IntField()
    release_date = DateTimeField()
    similar_books = ListField(StringField())
    small_image = FileField()
    summary = StringField()
    title = StringField(required=True, max_length=100)
    wikipedia_publication_date = IntField()
    wikipedia_url = StringField()
    wikipedia_found = BooleanField()

# end Book
