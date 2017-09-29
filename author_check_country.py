# -*- coding: utf-8 -*-
#

import argparse
import logging
import os
import wikipediaorg as wp
import dataset as ds
import goodreadscom as gr
import gutenberg as gb
from dataset.CountryCollection import CountryCollection
from dataset.Country import Country

######################################################
# Functions
#######################################################


######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram book dataset")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)
    country_collection = ds.CountryCollection.create(args.dataset_dir)
    year_collection = ds.YearCollection.create(args.dataset_dir)

    # Reset authors in countries
    for country in country_collection.get_countries():
        print(country.name)
        country.authors = list()
        del country.books
        del country.n_books
    # end for

    # Remove country in authors
    for author in book_collection.get_authors():
        del author.country
        author.countries = list()
    # end for

    # Remove country in books
    for book in book_collection.get_books():
        del book.country
    # end for

    # For each author
    for index, author in enumerate(book_collection.get_authors()):
        # Show
        print(u"Author {}?".format(author.name))

        # Get new country name
        country_response = raw_input(u"New countries? ").strip()

        # Split
        new_countries = country_response.split(u',')

        # Country list
        new_countries_obj = list()

        # Get country objects
        for new_country in new_countries:
            # Get object
            new_country_obj = country_collection.get_by_name(new_country.strip())

            # If don't exists
            if new_country_obj is None:
                new_country_obj = Country(country_name=new_country)
                country_collection.add(new_country_obj)
            # end if

            # Add to list
            new_countries_obj.append(new_country_obj)
        # end for

        # Add to author's country
        for new_country_obj in new_countries_obj:
            # Add to author's country if needed
            if new_country_obj.id not in author.countries:
                author.countries.append(new_country_obj.id)
            # end if

            # Add author to country
            if author.id not in new_country_obj.authors:
                new_country_obj.authors.append(author.id)
            # end if
        # end for

        # Save
        if index % 20 == 0:
            # Save collections
            book_collection.save(dataset.get_dataset_directory())
            country_collection.save(dataset.get_dataset_directory())
            year_collection.save(dataset.get_dataset_directory())
        # end if
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
