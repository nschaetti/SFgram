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
    parser.add_argument("--year", type=int, help="Year to check", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)
    country_collection = ds.CountryCollection.create(args.dataset_dir)
    year_collection = ds.YearCollection.create(args.dataset_dir)

    # Year -1
    year_minus_1 = year_collection.get_year(args.year)

    # Target years
    target_years = set(year_minus_1.books)

    # For each books
    for book_id in target_years:
        # Get book
        book = book_collection.get_book_by_id(book_id)

        # Show
        print(u"Book {} title {} by {}".format(book.id, book.title, book.author_name))

        # Get new year
        new_year = int(raw_input(u"Year of publication? ").strip())

        # Get object or create
        new_year_obj = year_collection.get_year(new_year)
        if new_year_obj is None:
            new_year_obj = year_collection.add(ds.Year(year=new_year))
        # end if

        # Change book's year
        book.year = new_year

        # Remove from old year
        if book.id in year_minus_1.books:
            year_minus_1.books.remove(book.id)
        # end if

        # Add to new year
        if book.id not in new_year_obj.books:
            new_year_obj.books.append(book.id)
        # end if

        # No duplicates
        year_minus_1.books = list(set(year_minus_1.books))
        new_year_obj.books = list(set(new_year_obj.books))

        # Sort
        year_minus_1.books.sort()
        new_year_obj.books.sort()

        # Save
        book_collection.save(dataset.get_dataset_directory())
        country_collection.save(dataset.get_dataset_directory())
        year_collection.save(dataset.get_dataset_directory())
    # end for
# end if
