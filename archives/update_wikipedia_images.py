# -*- coding: utf-8 -*-
#

import argparse
import wikipediaorg as wp
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
    parser.add_argument("--start", type=int, help="Starting book index", default=0)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)
    dataset.check_directories()

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)
    country_collection = ds.CountryCollection.create(args.dataset_dir)
    year_collection = ds.YearCollection.create(args.dataset_dir)

    # For each book
    for book in book_collection.get_books():
        if book.id >= args.start:
            if book.wikipedia['found']:
                # Log
                print(u"Updating images for book {} ({}) with ID {}".format(book.title, book.author_name, book.id))

                # Wikipedia & Goodreads information
                wikipedia_info = wp.WikipediaBookInformation.get_book_information_from_url(book.title, book.author_name, book.wikipedia['url'])

                # Set images
                if 'images' in wikipedia_info:
                    book.images = wikipedia_info['images']
                # end if
            # end if
        # end if
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
