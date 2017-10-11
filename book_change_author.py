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
    parser.add_argument("--book-id", type=int, help="Book's ID", required=True)
    parser.add_argument("--author-id", type=int, help="Last author ID", required=True)
    parser.add_argument("--new-author-id", type=int, help="New author ID", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # Get book
    book = book_collection.get_book_by_id(args.book_id)

    # Get author
    new_author = book_collection.get_author_by_id(args.new_author_id)

    # Last author
    last_author = book_collection.get_author_by_id(args.author_id)

    # Change book's author
    book.author_name = new_author.name
    book.authors.append(new_author.id)
    new_author.books.append(book.id)

    # Remove last author
    book.authors.remove(last_author.id)
    last_author.books.remove(book.id)

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
# end if
