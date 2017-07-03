# -*- coding: utf-8 -*-
#

from mongoengine import *
from .Image import Image


# A movie in the MongoDB database
class Movie(Document):
    """
    A movie in the MongoDB database
    """

    # Fields
    movie_id = StringField()
    title = StringField()
    poster = ReferenceField("Poster")
    year = IntField()
    url = URLField()
    keywords = ListField(ReferenceField("Keyword"))
    country = ReferenceField("Country")
    language = StringField()
    plot = StringField()
    gross = FloatField(null=True)

    # Does the movie exists
    @staticmethod
    def exists(movie_title, year):
        """
        Does a movie exists
        :param movie_title:
        :return:
        """
        movies = Movie.objects(title=movie_title, year=year)
        return movies.count() > 0
    # end exists

    # Get book from title
    @staticmethod
    def get_by_title_and_year(movie_title, year):
        """
        Get book from its title
        :param book_title:
        :return:
        """
        movies = Movie.objects(title=movie_title, year=year)
        if movies.count() > 0:
            return movies[0]
        else:
            return None
        # end if
    # end get_by_title

# end Book
