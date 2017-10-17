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
######################################################

######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Check author's gender")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    parser.add_argument("--start", type=int, help="Starting index", default=1)
    parser.add_argument("--end", type=int, help="End index", default=10000000)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # For each author
    for author in book_collection.get_authors():
        if author.id >= args.start and author.id <= args.end:
            # Show
            print(u"Author {} name {} date {}/{}".format(author.id, author.name, author.born, author.died))
            print(u"Summary : {}".format(author.summary))
            if author.wikipedia['found']:
                print(u"Wikipedia page : {}".format(author.wikipedia['url']))
            # end if

            # Ask
            print(u"Gender? (empty=unknown, m, f) ")
            page_answer = raw_input(u"Gender? ").strip().lower()

            # Change gender
            author.gender = page_answer

            # Save
            if author.id % 10 == 0:
                book_collection.save(dataset.get_dataset_directory())
            # end if
            print(u"")
        # end if
    # end for

    # Save
    book_collection.save(dataset.get_dataset_directory())

# end if
