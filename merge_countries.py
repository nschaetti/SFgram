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

    # For each book id in country 1
    for book_id in country2.books:
        # Add to country 1
        country1.books.append(book_id)
        country1.n_books += 1

        # Load the book
        book = book_collection.get_book_by_id(book_id)
        print(u"Set country of {} to {}".format(book.title, country1.name))

        # Change book's country
        book.country = country1.id

        # Load author
        author = book_collection.get_author_by_id(book.author)

        # Change author's country
        author.country = country1.id
        print(u"Set country of {} to {}".format(author.name, country1.name))
    # end for

    # Remove country
    country_collection.remove(country2)

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
