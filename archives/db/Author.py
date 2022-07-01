# -*- coding: utf-8 -*-
#

from mongoengine import *
from DBObject import DBObject


# An author in the MongoDB database
class Author(DBObject):
    """
    An author in the MongoDB database
    """

    # Indexes
    meta = {
        'indexes': [
            {
                'fields': ['#name']
            }]
    }

    # Fields
    id = IntField()
    ambiguation = BooleanField()
    birth_date = DateTimeField()
    death_date = DateTimeField()
    name = StringField(required=True, max_length=100)
    books = ListField(ReferenceField('Book'))
    bio = StringField()
    summary = StringField()
    wikipedia_page = URLField()
    n_books = IntField(default=0)

    ###############################################
    # PUBLIC
    ###############################################

    # Does the book exists
    @staticmethod
    def exists(author_name):
        authors = Author.objects(name=author_name)
        return authors.count() > 0
    # end exists

    # Get book from title
    @staticmethod
    def get_by_name(author_name):
        """
        Get book from its title
        :param book_title:
        :return:
        """
        authors = Author.objects(name=author_name)
        if authors.count() > 0:
            return authors[0]
        else:
            return None
        # end if
    # end get_by_title

# end Author
