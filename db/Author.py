# -*- coding: utf-8 -*-
#

from mongoengine import *
from .Book import Book


# An author in the MongoDB database
class Author(Document):
    """
    An author in the MongoDB database
    """

    # Fields
    birth_date = DateTimeField()
    death_date = DateTimeField()
    name = StringField(required=True, max_length=100)
    books = ListField(ReferenceField('Book'))

    ###############################################
    # PUBLIC
    ###############################################

    # Add a book to the collection
    def add_book(self, book):
        if book._id not in self.books:
            pass
        # end if
    # end add_book

# end Author
