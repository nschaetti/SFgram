# -*- coding: utf-8 -*-
#

# Imports


# An author in the dataset
class Author(object):
    """
    An author in the dataset
    """

    # Fields
    id = 0
    birth_date = None
    death_date = None
    name = ""
    books = list()
    bio = ""
    summary = ""
    wikipedia = {'ambiguation': False, 'url': u"", 'found': False}
    n_books = 0

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self.books = list()
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
