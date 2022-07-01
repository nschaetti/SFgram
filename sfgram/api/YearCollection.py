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

    _years = list()
    _n_year = 0

    # Constructor
    def __init__(self, years=list()):
        """
        Constructor
        """
        self._years = years
        self._n_years = len(years)
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
                self._n_years += 1
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
        # Order by year
        self._order_by_year()

        # Save books
        self._save_dict(self._years, dataset_directory, "years.p")
    # end save

    ####################################################
    # Static
    ####################################################

    # Order by year
    def _order_by_year(self):
        """
        Order the collection by year
        :return:
        """
        # To sort the list in place...
        self._years.sort(key=lambda x: x.year, reverse=True)

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
        collection_json_filename = os.path.join(dataset_directory, "years.json")

        # Log
        logging.getLogger(u"SFGram").info(u"Saving country collection to {}".format(collection_filename))

        # Save
        with open(collection_filename, 'wb') as f:
            pickle.dump(d, f)
        # end with

        # Save
        with open(collection_json_filename, 'wb') as f:
            json.dump(self.to_dict(), f, indent=4)
        # end with
    # end _save_dict

    ####################################################
    # Static
    ####################################################

    # Create collection
    @staticmethod
    def create(dataset_directory):
        """
        Create or load the collection
        :param dataset_directory:
        :return:
        """
        # Load or create book collection
        if os.path.exists(os.path.join(dataset_directory, "years.p")):
            years = YearCollection.load(dataset_directory)
            return YearCollection(years=years)
        else:
            return YearCollection()
        # end if
    # end create

    # Load book collection
    @staticmethod
    def load(dataset_directory):
        """
        Load book collection
        :param filename:
        :return:
        """
        # Collection file
        collection_filename = os.path.join(dataset_directory, "years.p")

        # Log
        logging.getLogger(u"SFGram").info(u"Loading year collection from {}".format(collection_filename))

        # Load
        with open(collection_filename, 'rb') as f:
            return pickle.load(f)
        # end with
    # end load

    # To dictionary
    def to_dict(self):
        """
        To dictionary
        :return:
        """
        result = dict()

        # Countries
        result['years'] = list()
        for year in self._years:
            result['years'].append(year.to_dict())
        # end for

        return result
    # end to_dict

# end Book
