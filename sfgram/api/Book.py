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


# A book in the dataset
class Book(object):
    """
    A book in the dataset
    """

    # Fields
    author = None
    author_name = ""
    authors = list()
    average_rating = -1.0
    category = ""
    cleaned = False
    content = ""
    contents = list()
    content_available = False
    content_tokens = 0
    copyright = ""
    countries = list()
    cover = ""
    cover_art = ""
    cover_art_url = ""
    cover_artist = ""
    description = ""
    format = ""
    genres = list()
    gutenberg = {'url': u"", 'num': 0}
    goodreads = {'year': -1, 'url': u"", 'found': False}
    id = 0
    images = list()
    images_urls = list()
    ISBN = ""
    ISBN13 = ""
    language = ""
    language_code = ""
    loc_class = ""
    num = -1
    n_authors = 0
    original_title = ""
    pages = 0
    publication_date = 0
    rating_count = 0
    release_date = None
    similar_books = list()
    small_image = ""
    summary = ""
    title = ""
    wikipedia = {'year': -1, 'ambiguation': False, 'url': u"", 'found': False}
    year = 0

    # Constructor
    def __init__(self, title, author_name):
        """
        Constructor
        """
        self.title = title
        self.author_name = author_name
        self.authors = list()
        self.countries = list()
        self.contents = list()
        self.genres = list()
        self.images = list()
        self.images_urls = list()
        self.similar_books = list()
        self.cover = ""
    # end __init__

    # region PUBLIC

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

    # endregion PUBLIC

# end Book
