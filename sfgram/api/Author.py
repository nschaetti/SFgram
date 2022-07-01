# -*- coding: utf-8 -*-
#
# File : sfgram/api/Author.py
#
# This file is part of the SFGram distribution (https://github.com/nschaetti/SFgram).
# Copyright (c) 2022 Nils Schaetti.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Copyright Nils Schaetti, University of Neuchâtel <nils.schaetti@unine.ch>
# University of Geneva <nils.schaetti@unige.ch>, <n.schaetti@gmail.com>

# Imports
import datetime


# An author in the dataset
class Author(object):
    r"""An author in the dataset.
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
        r"""Constructor.

        :param name:
        """
        self.name = name
        self.books = list()
        self.countries = list()
        self.gender = ""
    # end __init__

    # region PUBLIC

    # Import properties from dictionary
    def import_from_dict(self, dict_var, exclude=[]):
        r"""Import properties from dictionary.

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
        r"""To dictionary.

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

    # endregion PUBLIC

    # region PRIVATE

    # endregion PRIVATE

    # region STATIC

    # endregion STATIC

# end Author
