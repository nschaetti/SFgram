# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
import download as dw
from db.Author import Author
from db.Country import Country
from db.Book import Book
from db.Movie import Movie
from dateutil.parser import parse

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

    # For each book
    for book in Book.objects():
        print(u"Book title : {}".format(book.title))
        print(u"Book year : {}".format(book.year))
        print(u"Author : {}".format(book.author.name))
        print(u"Birth {}, Death {}".format(book.author.birth_date, book.author.death_date))
        year = raw_input("Year : ")
        if year != "":
            book.year = int(year)
            book.save()
        # end if
    # end for

# end if
