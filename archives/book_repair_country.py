# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
from archives.db import Author
from archives.db import Country
from archives.db import Book

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
    parser.add_argument("--country_id", type=str, help="Country ID", required=True)
    parser.add_argument("--country", type=str, help="Second country", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # Second country
    country = Country.objects(name=args.country)[0]

    # All books
    for book in Book.objects(country=None):
        if book not in country.books:
            logging.info(book.title)
            country.books.append(book)
            country.n_books += 1
            book.country = country
            book.save()
        # end if
    # end for

    # Save
    country.save()

# end if
