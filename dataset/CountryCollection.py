# -*- coding: utf-8 -*-
#

# Imports
import os
import logging
import pickle
import json
from .Country import Country


# A collection of country in the dataset
class CountryCollection(object):
    """
    A collection of book in the dataset
    """

    _next_country_id = 0
    _countries = list()
    _n_country = 0

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self._countries = list()
    # end if

    ####################################################
    # Public
    ####################################################

    # Exists
    def exists(self, country):
        """

        :param country:
        :return:
        """
        for c in self._countries:
            if c.name == country.name:
                return True
            # end if
        # end for
        return False
    # end book_exists

    # Add a country
    def add(self, country):
        """
        Add a country
        :param country:
        :return:
        """
        if not self.exists(country):
            if type(country) is Country:
                # Log
                logging.getLogger(u"SFGram").info(u"New country added {}".format(country.name))

                # Set ID
                country.id = self._next_country_id

                # Add
                self._countries.append(country)

                # Next id
                self._next_country_id += 1
            # end if
        else:
            return self.get_by_name(country.name)
        # end if

        return country
    # end add

    # Get country
    def get_by_name(self, country_name):
        """
        Get country by name
        :param country_name:
        :return:
        """
        for country in self._countries:
            if country.name == country_name:
                return country
            # end if
        # end for
        return None
    # end get_by_name

    # Get next country id
    def get_next_country_id(self):
        """
        Get next country ID
        :return:
        """
        return self._next_country_id
    # end get_next_book_id

    # Save the collection
    def save(self, dataset_directory):
        """
        Save the collection
        :param dataset_directory:
        :return:
        """
        # Save books
        self._save_dict(self._countries, dataset_directory, "country.p")
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
