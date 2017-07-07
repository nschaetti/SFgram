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
    unknown_country = Country.objects(name="Unknown")

    # Get books
    books = Book.objects(country=unknown_country[0].id)

    # Display countries
    for country in Country.objects():
        print(country.name,)
    # end for

    # For each book
    for book in books:
        # Display title
        print("{} by {}".format(book.title, book.author.name))

        # Get country name
        country_name = raw_input("Country? ").strip()

        # Exit?
        if country_name == "":
            exit()
        # end if

        # Get country or create
        if Country.exists(country_name):
            country = Country.get_by_name(country_name)
        else:
            country = Country(name=country_name)
        # end if

        # Create country
        logging.info("Updating/saving country {}".format(country.name))
        if book not in country.books:
            country.books.append(book)
            country.n_books += 1
            country.save()
        # end if

        # Update Unknown country
        unknown_country[0].books.remove(book)
        unknown_country[0].n_books -= 1
        unknown_country[0].save()

        # Update
        logging.info("Updating/saving book {}".format(book.title))
        book.country = country
        book.save()
    # end for

# end if
