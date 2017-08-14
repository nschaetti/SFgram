# -*- coding: utf-8 -*-
#

# Imports


# A year in the dataset
class Year(object):
    """
    A year in the dataset
    """

    # Fields
    year = 0
    books = list()
    n_books = 0
    movies = list()
    n_movies = 0

    # Constructor
    def __init__(self, year):
        """
        Constructor
        """
        self.year = year
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

    ############################################
    # Private
    ############################################

    ############################################
    # Static
    ############################################

# end Book
