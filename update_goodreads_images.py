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
    parser.add_argument("--start", type=int, help="Starting book index", default=0)
    parser.add_argument("--end", type=int, help="Starting book index", default=100000000)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)
    dataset.check_directories()

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # For each book
    for book in book_collection.get_books():
        if book.id >= args.start and book.id <= args.end:
            if book.goodreads['found']:
                # Log
                print(u"Updating images for book {} ({}) with ID {}".format(book.title, book.author_name, book.id))

                # Wikipedia & Goodreads information
                goodreads_info = gr.GoodReadsConnector.get_book_info_url(book.title, book.author_name, book.goodreads['url'])

                if goodreads_info is not None:
                    # Set cover
                    if 'large_cover' in goodreads_info:
                        book.cover = goodreads_info['large_cover']
                    elif 'cover' in goodreads_info:
                        book.cover = goodreads_info['cover']
                    elif 'small_image' in goodreads_info:
                        book.cover = goodreads_info['small_image']
                    # end if
                # end if

                # Save
                if book.id % 10 == 0:
                    print(u"Saving...")
                    book_collection.save(dataset.get_dataset_directory())
                # end if
            else:
                if hasattr(book, 'cover'):
                    delattr(book, 'cover')
                # end if
            # end if
        # end if
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())

# end if
