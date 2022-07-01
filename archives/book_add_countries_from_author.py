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
        # Author's countries
        author_countries = author.countries

        # For each of its books
        for book_id in author.books:
            # Get book
            book = book_collection.get_book_by_id(book_id)
            book.countries = list()

            # For each country
            for author_country in author_countries:
                if author_country not in book.countries:
                    book.countries.append(author_country)
                # end if
            # end for
        # end for
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
