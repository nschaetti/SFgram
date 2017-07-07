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
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # Get Unknown country
    unknown_country = Country.objects(name="Unknown")[0]

    # Reinit
    unknown_country.n_books = len(unknown_country.books)

    # Get books
    books = unknown_country.books

    # For each book
    for book in books:
        # Display title
        logging.info("{} by {} ({})".format(book.title, book.author.name, book.country.name))

        # If country not unknown
        if book.country != unknown_country:
            logging.info("Updateing {}".format(book.title))
            unknown_country.books.remove(book)
            unknown_country.n_books -= 1
            unknown_country.save()
        # end if
    # end for

# end if
