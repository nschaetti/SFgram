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
    parser.add_argument("--name", type=str, help="Author's new name", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # For each author
    for author in book_collection.get_authors():
        if author.name.lower() == args.name.lower():
            print(author.id)
            print(author.name)
            print(author.books)
        # end if
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
# end if
