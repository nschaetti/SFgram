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
    parser.add_argument("--author-id", type=int, help="Author's ID", required=True)
    parser.add_argument("--name", type=str, help="Author's new name", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # Get author
    author = book_collection.get_author_by_id(args.author_id)

    # Change name
    author.name = args.name

    # For each book
    for book_id in author.books:
        # Get book
        book = book_collection.get_book_by_id(book_id)

        # Change author's name
        book.author_name = args.name
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
# end if
