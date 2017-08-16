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
    def __init__(self, countries=list()):
        """
        Constructor
        :param books: Books
        :param authors: Authors
        """
        self._countries = countries
        self._n_country = len(countries)

        # Search next country id
        self._next_country_id = self._get_next_id(countries)
    # end __init__

    ####################################################
    # Public
    ####################################################

    # Get next id
    def _get_next_id(self, collection):
        """
        Get next id
        :param collection:
        :return:
        """
        # Search next id
        max_id = 0
        for element in collection:
            if element.id > max_id:
                max_id = element.id
                # end if
        # end for
        return max_id
    # end _get_next_id

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
                self._n_country += 1

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
        self._save_dict(self._countries, dataset_directory, "countries.p")
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
        collection_json_filename = os.path.join(dataset_directory, "countries.json")

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

    # To dictionary
    def to_dict(self):
        """
        To dictionary
        :return:
        """
        result = dict()

        # Countries
        result['countries'] = list()
        for country in self._countries:
            result['countries'].append(country.to_dict())
        # end for

        return result
    # end to_dict

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
        if os.path.exists(os.path.join(dataset_directory, "countries.p")):
            countries = CountryCollection.load(dataset_directory)
            return CountryCollection(countries=countries)
        else:
            return CountryCollection()
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
        collection_filename = os.path.join(dataset_directory, "countries.p")

        # Log
        logging.getLogger(u"SFGram").info(u"Loading country collection from {}".format(collection_filename))

        # Load
        with open(collection_filename, 'rb') as f:
            return pickle.load(f)
        # end with
    # end load

# end Book
