# -*- coding: utf-8 -*-
#

# Imports
import datetime


# An author in the dataset
class Author(object):
    """
    An author in the dataset
    """

    # Fields
    id = 0
    born = None
    died = None
    name = ""
    books = list()
    bio = ""
    summary = ""
    wikipedia = {'ambiguation': False, 'url': u"", 'found': False}
    n_books = 0
    countries = list()
    gender = ""

    # Constructor
    def __init__(self, name):
        """
        Constructor
        """
        self.name = name
        self.books = list()
        self.countries = list()
        self.gender = ""
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
        To dictionary
        :return:
        """
        result = dict()
        obj_dict = self.__dict__
        for key in obj_dict.keys():
            if obj_dict[key] is not None:
                if type(obj_dict[key]) is datetime.datetime:
                    result[key] = str(obj_dict[key])
                else:
                    result[key] = obj_dict[key]
            # end if
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
