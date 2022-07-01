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
    parser.add_argument("--country1", type=str, help="First country (destination)", required=True)
    parser.add_argument("--country2", type=str, help="Second country (source)", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)
    country_collection = ds.CountryCollection.create(args.dataset_dir)
    year_collection = ds.YearCollection.create(args.dataset_dir)

    # Load first country
    country1 = country_collection.get_by_name(args.country1)
    country2 = country_collection.get_by_name(args.country2)

    # Move books
    for book_id in country2.books:
        # Add to country 1
        if book_id not in country1.books:
            country1.books.append(book_id)
        # end if

        # Get book
        book = book_collection.get_book_by_id(book_id)

        # Remove old country
        if country2.id in book.countries:
            book.countries.remove(country2.id)
        # end if

        # Add new country
        if country1.id not in book.countries:
            book.countries.append(country1.id)
        # end if
    # end for

    # Move authors
    for author_id in country2.authors:
        # Add to country 1
        if author_id not in country1.authors:
            country1.authors.append(author_id)
        # end if

        # Get author
        author = book_collection.get_author_by_id(author_id)

        # Remove old country
        if country2.id in author.countries:
            author.countries.remove(country2.id)
        # end if

        # Add new country
        if country1.id not in author.countries:
            author.countries.append(country1.id)
        # end if
    # end for

    # Remove country
    country_collection.remove(country2)

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
