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

    # For each author
    for author in Author.objects():
        print(u"Author's name : {}".format(author.name))
        print(u"Author's birth date : {}".format(author.birth_date))
        print(u"Author's death date : {}".format(author.death_date))
        birth_date = raw_input("Birth date : ")
        if birth_date != "":
            author.birth_date = parse(birth_date)
        else:
            author.birth_date = None
        # end if
        death_date = raw_input("Death date : ")
        if death_date != "":
            author.death_date = parse(death_date)
        else:
            author.death_date = None
        # end if
        author.save()
    # end for

# end if
