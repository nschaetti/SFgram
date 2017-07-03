# -*- coding: utf-8 -*-
#

from mongoengine import *
from .Book import Book


# A country in the MongoDB database
class Country(Document):
    """
    A country in the MongoDB database.
    """

    # Fields
    authors = ListField(ReferenceField("Author"))
    n_authos = IntField()
    books = ListField(ReferenceField("Book"))
    n_books = IntField()
    name = StringField(required=True, max_length=100)
    movies = ListField(ReferenceField("Movie"))
    n_movies = IntField(default=0)

    ###############################################
    # PUBLIC
    ###############################################

    # Does the country exists
    @staticmethod
    def exists(country_name):
        """
        Does country exists
        :param country_name:
        :return:
        """
        countries = Country.objects(name=country_name)
        return countries.count() > 0
    # end exists

    # Get book from title
    @staticmethod
    def get_by_name(country_name):
        """
        Get book from its title
        :param country_name:
        :return:
        """
        countries = Country.objects(name=country_name)
        if countries.count() > 0:
            return countries[0]
        else:
            return None
        # end if
    # end get_by_title

# end Country
