# -*- coding: utf-8 -*-
#

import argparse
import logging
import os
import gutenberg as gb
import goodreads as gr
import wikipedia as wp
import dataset as ds

######################################################
#
# Main
#
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram book dataset")

    # Argument
    parser.add_argument("--output-dir", type=str, help="Output directory", required=True)
    parser.add_argument("--start-index", type=int, help="Start page index", default=1)
    parser.add_argument("--skip-book", type=int, help="Number of books to skip", default=0)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name=u"SFGram")

    # Load or create book collection
    if os.path.exists(os.path.join(args.output_dir, "books.json")):
        book_collection = ds.BookCollection.load(os.path.join(args.output_dir, "books.json"))
    else:
        book_collection = ds.BookCollection()
    # end if

    # Open category
    gutenberg_con = gb.GutenbergBookshelf()
    gutenberg_con.open(num=68, start_index=args.start_index, skip_book=args.skip_book)

    # For each book
    for index, book_informations in enumerate(gutenberg_con):
        # New book
        book = ds.Book()

        # Wikipedia information
        wikipedia_info = wp.WikipediaBookInformation.get_book_information(book_informations['title'],
                                                                          book_informations['authors'][0])

        # Goodreads information
        goodreads_info = gr.GoodReadsConnector.get_book_info(book_informations['title'])

        # Properties
        book.title = book_informations['title']

        # Save images

        # Save cover

        # Save cover-art

        # Save content

        # Add to book collection

        # Save book collection
    # end for

# end if
