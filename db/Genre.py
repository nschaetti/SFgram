
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
    movies = ListField(ReferenceField("Movies"))
    name = StringField(required=True, max_length=100)

    ###############################################
    # PUBLIC
    ###############################################

    # Does the country exists
    @staticmethod
    def exists(genre_name):
        """
        Does country exists
        :param genre_name:
        :return:
        """
        genres = Genre.objects(name=genre_name)
        return genres.count() > 0
    # end exists

    # Get book from title
    @staticmethod
    def get_by_name(genre_name):
        """
        Get book from its title
        :param genre_name:
        :return:
        """
        genres = Genre.objects(name=genre_name)
        if genres.count() > 0:
            return genres[0]
        else:
            return None
        # end if
    # end get_by_title

# end Genre
