# -*- coding: utf-8 -*-
#

import argparse
from archives import dataset as ds

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
        # For each country
        for country_id in author.countries:
            # Get country
            country = country_collection.get_by_id(country_id)

            # If doesn't exists
            if country is None:
                author.countries.remove(country_id)
            # end if
        # end for
    # end for

    # For each book
    for book in book_collection.get_books():
        # For each countries
        for country_id in book.countries:
            # Get country
            country = country_collection.get_by_id(country_id)

            # If doesn't exists
            if country is None:
                book.countries.remove(country_id)
            # end if
        # end for
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
