# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
import download as dw
from db.Author import Author
from db.Country import Country
from db.Book import Book

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
    parser = argparse.ArgumentParser(description="SFgram - Check all books with unknown country")

    # Argument
    parser.add_argument("--database", type=str, help="Database name", default="sfgram", required=True)
    parser.add_argument("--country", type=str, help="First country", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # First country
    country = Country.objects(name=args.country)[0]

    # Add books 1
    for book in country.books:
        logging.info(book.title)
    # end for
# end if
