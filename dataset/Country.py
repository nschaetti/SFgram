# -*- coding: utf-8 -*-
#

# Imports


# A country in the dataset
class Country(object):
    """
    A country in the dataset
    """

    # Fields
    id = 0
    books = list()
    n_books = 0
    name = ""
    movies = list()
    n_movies = 0

    # Constructor
    def __init__(self, country_name):
        """
        Constructor
        """
        self.name = country_name
        self.authors = list()
        self.books = list()
        self.movies = list()
    # end __init__

    ############################################
    # Public
    ############################################

    # Import properties from dictionary
    def import_from_dict(self, dict_var, exclude=[]):
        """
        Import properties from dictionary
        :param dict_var: Dictionary to import
        :param exclude: Key to exclude
        """
        # For each dict's key
        for key in dict_var.keys():
            if key not in exclude:
                setattr(self, key, dict_var[key])
            # end if
        # end for
    # end import_from_dict

    # To dictionary
    def to_dict(self):
        """

        :return:
        """
        result = dict()
        obj_dict = self.__dict__
        for key in obj_dict.keys():
            if obj_dict[key] is not None:
                result[key] = obj_dict[key]
        # end if
        return result
    # end to_dict

    ############################################
    # Private
    ############################################

    ############################################
    # Static
    ############################################

# end Book
