# -*- coding: utf-8 -*-
#

import argparse
import logging
import os
import wikipediaorg as wp
import dataset as ds
import goodreadscom as gr
import gutenberg as gb

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
    parser.add_argument("--name", type=str, help="Author's name", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # New author
    new_author = ds.Author(name=args.name)

    # Add
    book_collection.add(new_author)

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
# end if
