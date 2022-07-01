# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
from archives.db import Author
from archives.db import Country


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
    parser.add_argument("--country1", type=str, help="First country", required=True)
    parser.add_argument("--country2", type=str, help="Second country", required=True)
    parser.add_argument("--new", type=str, help="New country", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # First country
    country1 = Country.objects(name=args.country1)[0]

    # Second country
    country2 = Country.objects(name=args.country2)[0]

    # New country
    new_country = Country(name=args.new)
    new_country.save()

    # Add books 1
    for book in country1.books:
        if book not in new_country.books:
            new_country.books.append(book)
            new_country.n_books += 1
        # end if
    # end for

    # Add books 2
    for book in country2.books:
        if book not in new_country.books:
            new_country.books.append(book)
            new_country.n_books += 1
        # end if
    # end for

    # Add movies
    for movie in country1.movies:
        if movie not in new_country.movies:
            new_country.movies.append(movie)
            new_country.n_movies += 1
        # end if
    # end for

    # Add movies
    for movie in country2.movies:
        if movie not in new_country.movies:
            new_country.movies.append(movie)
            new_country.n_movies += 1
        # end if
    # end for

    # Save new country
    new_country.save()

    # Delete country
    country1.delete()
    country2.delete()

# end if
