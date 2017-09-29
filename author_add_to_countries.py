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

    # For each books
    for book in book_collection.get_books():
        # For each country
        for country_id in book.countries:
            # Get country
            book_country = country_collection.get_by_id(country_id)
            if book_country.books is None:
                book_country.books = list()
            # end if

            # Add book to country
            if book.id not in book_country.books:
                book_country.books.append(book.id)
            # end if
        # end for
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
