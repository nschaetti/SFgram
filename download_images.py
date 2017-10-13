# -*- coding: utf-8 -*-
#

import argparse
import logging
import os
import wikipediaorg as wp
import dataset as ds
import goodreadscom as gr
import gutenberg as gb
import tools

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
            # Log
            print(u"Downloading images for book {} ({}) with ID {}".format(book.title, book.author_name, book.id))

            # Save gutenberg images
            if hasattr(book, 'images_urls') and book.images_urls is not None:
                for image_url in book.images_urls:
                    print(u"\tDownloading {}".format(image_url))
                    try:
                        (data, name) = tools.Tools().download_http_file(image_url)
                        book_collection.save_image(dataset.get_dataset_directory(), book.id, data, name)
                    except tools.DownloadErrorException:
                        pass
                    # end try
                # end for
            # end if

            # Save gutenberg images
            if hasattr(book, 'images') and book.images is not None:
                for image_url in book.images:
                    print(u"\tDownloading {}".format(image_url))
                    try:
                        (data, name) = tools.Tools().download_http_file(image_url)
                        book_collection.save_image(dataset.get_dataset_directory(), book.id, data, name)
                    except tools.DownloadErrorException:
                        pass
                    # end try
                # end if
            # end if

            # Save cover from Goodreads
            if hasattr(book, 'cover') and book.cover is not None:
                if book.cover != "":
                    print(u"\tDownloading {}".format(book.cover))
                    try:
                        (data, name) = tools.Tools().download_http_file(book.cover)
                        book_collection.save_cover(dataset.get_dataset_directory(), book.id, data, name)
                    except tools.DownloadErrorException:
                        pass
                    # end try
                # end if
            # end if

            # Save cover from gutenberg
            if hasattr(book, 'cover_art_url') and book.cover_art_url is not None:
                if book.cover_art_url != "":
                    print(u"\tDownloading {}".format(book.cover_art_url))
                    try:
                        (data, name) = tools.Tools().download_http_file(book.cover_art_url)
                        book_collection.save_cover(dataset.get_dataset_directory(), book.id, data, name)
                    except tools.DownloadErrorException:
                        pass
                    # end try
                # end if
            # end if

            # Space
            #print("")
        # end if
    # end for

# end if
