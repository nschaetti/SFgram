# -*- coding: utf-8 -*-
#

import argparse
from archives import dataset as ds

######################################################
# Functions
######################################################

######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Check books' wikipedia page")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    parser.add_argument("--book-id", type=int, help="Book ID", required=True)
    parser.add_argument("--year", type=int, help="New year", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)
    year_collection = ds.YearCollection.create(args.dataset_dir)

    # Get book
    book = book_collection.get_book_by_id(args.book_id)

    # Get new year
    new_year = args.year

    # Year -1
    year_minus_1 = year_collection.get_year(book.year)

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
    year_collection.save(dataset.get_dataset_directory())
# end if
