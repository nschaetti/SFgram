# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
from archives.db import Author
from archives.db import Country
from archives.db import Book
from archives.db import Movie

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

    # Total books and movies
    total_books = len(Book.objects())
    total_movies = len(Movie.objects())

    # For each author
    total_author_n_books = 0
    for author in Author.objects():
        # Add n_books
        total_author_n_books += author.n_books
    # end for

    # For each country
    total_country_n_books = 0
    total_country_n_movies = 0
    for country in Country.objects():
        # Add n_books and n_movies
        total_country_n_books += country.n_books
        total_country_n_movies += country.n_movies
    # end for

    # Checks
    if total_author_n_books == total_books:
        logging.info(u"Total author books consistency check ok : {}".format(total_author_n_books))
    else:
        logging.info(u"Total author books inconsistent : {} vs {}".format(total_author_n_books, total_books))
    # end if

    # Checks
    if total_country_n_books == total_books:
        logging.info(u"Total country books consistency check ok : {}".format(total_country_n_books))
    else:
        logging.info(u"Total country books inconsistent : {} vs {}".format(total_country_n_books, total_books))
    # end if

    # Checks
    if total_country_n_movies == total_movies:
        logging.info(u"Total country movies consistency check ok : {}".format(total_country_n_movies))
    else:
        logging.info(u"Total country movies inconsistent : {} vs {}".format(total_country_n_movies, total_movies))
    # end if

# end if
