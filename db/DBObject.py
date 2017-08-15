# -*- coding: utf-8 -*-
#

from mongoengine import *
from .Book import Book


# An object in the database
class DBObject(Document):
    """
    An object in the database
    """

    ###############################################
    # PUBLIC
    ###############################################

    # Does the object exsists
    @staticmethod
    def exists(object_id):
        """
        Does the object exists if the db
        :param object_id:
        :return:
        """
        pass
    # end exists

    # Create or get the object
    @staticmethod
    def get(*args, **kwargs):
        """
        Create or get the object
        :param args:
        :param kwargs:
        :return:
        """
        pass
    # end create_or_get

# end Author
