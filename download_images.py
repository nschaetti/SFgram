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
            # Log
            print(u"Downloading images for book {} ({}) with ID {}".format(book.title, book.author_name, book.id))

            # Wikipedia & Goodreads information
            wikipedia_info = wp.WikipediaBookInformation.get_book_information_from_url(book.title, book.author_name, book.wikipedia['url'])
            goodreads_info = gr.GoodReadsConnector.get_book_info_url(book.title, book.author_name, book.goodreads['url'])
            if book.id == 7:
                print(wikipedia_info)
                exit()
            # end if
            # Save gutenberg images
            for image_url in book.images_urls:
                (data, name) = tools.Tools().download_http_file(image_url)
                book_collection.save_image(dataset.get_dataset_directory(), book.id, data, name)
            # end for

            # Save gutenberg images
            if wikipedia_info['wikipedia']['found']:
                for (data, name) in wikipedia_info['images']:
                    book_collection.save_image(dataset.get_dataset_directory(), book.id, data,
                                               name)
                # end for
            # end if

            # Save cover (from wikipedia)
            if 'cover' in book_informations.keys():
                book_collection.save_cover(dataset.get_dataset_directory(), book.id,
                                           book_informations['cover'][0], book_informations['cover'][1])
            # end if

            # Save cover (from goodreads)
            if 'cover' in goodreads_info.keys():
                book_collection.save_cover(dataset.get_dataset_directory(), book.id,
                                           goodreads_info['cover'][0], goodreads_info['cover'][1])
            # end if

            # Save small image
            if 'small_image' in goodreads_info.keys():
                book_collection.save_image(dataset.get_dataset_directory(), book.id,
                                           goodreads_info['small_image'][0], goodreads_info['small_image'][1])
            # end if

            # Save content
            if book.content_available:
                book_collection.save_content(dataset.get_dataset_directory(), book.id,
                                             book_informations['content'])
            # end if

            # Space
            print("")
        # end if
    # end for

# end if
