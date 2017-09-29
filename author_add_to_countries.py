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

    # For each author
    for author in book_collection.get_authors():
        if author.country != -1:
            # Load country
            country = country_collection.get_by_id(author.country)

            # Add if not present
            if author.id not in country.authors:
                print(u"Adding {} to country {}".format(author.name, country.name))
                country.authors.append(author.id)
            # end if
        else:
            print(u"Warning author {} as country -1".format(author.name))
            # Get author's first book
            first_book = book_collection.get_book_by_id(author.books[0])

            # Load country
            country = country_collection.get_by_id(first_book.country)

            # Set author's country
            print(u"Author {} country set to {}".format(author.name, country.name))
            author.country = country.id

            # Add if not present
            if author.id not in country.authors:
                print(u"Adding {} to country {}".format(author.name, country.name))
                country.authors.append(author.id)
            # end if
        # end if
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
