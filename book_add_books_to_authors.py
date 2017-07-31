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
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # For each authors
    for author in Author.objects():
        logging.info(u"Examining author {}...".format(author.name))
        # For each book
        for book in Book.objects():
            if author in book.authors and book not in author.books:
                logging.info(u"Adding {} to author {}".format(book.title, author.name))
                author.books.append(book)
                author.save()
            # end if
        # end for
    # end for

# end if
