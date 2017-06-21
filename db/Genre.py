
from mongoengine import *
from .Book import Book


# A genre in the MongoDB database
class Genre(Document):
    """
    A genre in the MongoDB database.
    """

    # Fields
    authors = ListField(ReferenceField("Author"))
    books = ListField(ReferenceField("Book"))
    name = StringField(required=True, max_length=100)

    ###############################################
    # PUBLIC
    ###############################################

    # Add a book to the collection
    def add_book(self, book):
        pass
    # end add_book

# end Genre
