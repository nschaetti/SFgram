# -*- coding: utf-8 -*-
#

# Imports
import os
import logging
import pickle
import json
from .Year import Year


# A collection of year in the dataset
class YearCollection(object):
    """
    A collection of year in the dataset
    """

    _next_year_id = 0
    _years = list()
    _n_year = 0

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self._years = list()
    # end if

    ####################################################
    # Public
    ####################################################

    # Exists
    def exists(self, year):
        """

        :param country:
        :return:
        """
        for y in self._years:
            if y.year == year.year:
                return True
            # end if
        # end for
        return False
    # end book_exists

    # Add a year
    def add(self, year):
        """
        Add a year
        :param year:
        :return:
        """
        if not self.exists(year):
            if type(year) is Year:
                # Log
                logging.getLogger(u"SFGram").info(u"New year added {}".format(year.year))

                # Add
                self._years.append(year)
            # end if
        else:
            return self.get_year(year.year)
        # end if

        return year
    # end add

    # Get country
    def get_year(self, year):
        """
        Get country by name
        :param year:
        :return:
        """
        for y in self._years:
            if y.year == year:
                return y
            # end if
        # end for
        return None
    # end get_by_name

    # Save the collection
    def save(self, dataset_directory):
        """
        Save the collection
        :param dataset_directory:
        :return:
        """
        # Save books
        self._save_dict(self._years, dataset_directory, "year.p")
    # end save

    ####################################################
    # Static
    ####################################################

    # Save variable
    def _save_dict(self, d, dataset_directory, filename):
        """
        Save dictionary
        :param dict:
        :param filename:
        :param directory:
        :return:
        """
        # Collection file
        collection_filename = os.path.join(dataset_directory, filename)

        # Log
        logging.getLogger(u"SFGram").info(u"Saving country collection to {}".format(collection_filename))

        # Save
        with open(collection_filename, 'wb') as f:
            pickle.dump(d, f)
        # end with
    # end _save_dict

    ####################################################
    # Static
    ####################################################

    # Load book collection
    @staticmethod
    def load(dataset_directory):
        """
        Load book collection
        :param filename:
        :return:
        """
        # Collection file
        collection_filename = os.path.join(dataset_directory, "year.p")

        # Log
        logging.getLogger(u"SFGram").info(u"Loading country collection from {}".format(collection_filename))

        # Load
        with open(collection_filename, 'rb') as f:
            return pickle.load(collection_filename, f)
        # end with
    # end load

# end Book
