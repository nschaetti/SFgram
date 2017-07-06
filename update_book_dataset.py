# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
import download as dw
from db.Author import Author

######################################################
#
# Functions
#
######################################################


def get_author(author_name):
    # Check if exists
    if Author.exists(author_name=author_name):
        return Author.get_by_name(author_name)
    else:
        return Author(name=author_name)
    # end if
# end create_author

######################################################
#
# Main
#
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram MongoDB database.")

    # Argument
    parser.add_argument("--database", type=str, help="Database name", default="sfgram", required=True)
    parser.add_argument("--start-index", type=int, help="Start page index", default=1)
    parser.add_argument("--skip-book", type=int, help="Number of books to skip", default=0)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # Statistics
    count = 0
    token_count = 0

    # Open category
    gutenberg_con = dw.GutenbergBookshelf()
    gutenberg_con.open(num=68, start_index=args.start_index, skip_book=args.skip_book)

    # GoodReads connector
    goodreads_con = dw.GoodReadsConnector()

    # For each book
    for index, book in enumerate(gutenberg_con):
        # Registered
        logging.info(u"Book {} ({}), {} ({}) saved/updated in database".format(book.title, book.publication_date,
                                                                       book.author.name,
                                                                       book.country.name if book.country is not None
                                                                       else ""))

        # Save book in DB
        book.save()
    # end for

# end if
