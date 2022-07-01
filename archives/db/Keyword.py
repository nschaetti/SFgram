
from mongoengine import *
from .Book import Book


# A keyword in the MongoDB database
class Keyword(Document):
    """
    A keyword in the MongoDB database.
    """

    # Fields
    movies = ListField(ReferenceField("Movie"))
    name = StringField(required=True, max_length=100)
    n_movies = IntField(default=0)

    ###############################################
    # PUBLIC
    ###############################################

    # Does the keyword exists
    @staticmethod
    def exists(keyword_name):
        """
        Does country exists
        :param keyword_name:
        :return:
        """
        keywords = Keyword.objects(name=keyword_name)
        return keywords.count() > 0
    # end exists

    # Get keyword from title
    @staticmethod
    def get_by_name(keyword_name):
        """
        Get book from its title
        :param keyword_name:
        :return:
        """
        keywords = Keyword.objects(name=keyword_name)
        if keywords.count() > 0:
            return keywords[0]
        else:
            return None
        # end if
    # end get_by_title

# end Genre
