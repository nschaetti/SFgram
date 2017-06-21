# -*- coding: utf-8 -*-
#

import argparse
import logging
import datetime

from mongoengine import *

import db

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
    parser = argparse.ArgumentParser(description="SFgram - Clean and save Gutenberg data set to JSON files, plain text and images.")

    # Argument
    parser.add_argument("--database", type=str, help="MongoDB database name", default="sfgram", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    frank_herbert = db.Author(name="Frank Herbert", birth_date=datetime.datetime.utcnow())
    frank_herbert.save()

    us = db.Country(name="United-States")
    us.save()

    planet_opera = db.Genre(name="Planet Opera")
    planet_opera.save()

    dune = db.Book(title="Dune", author=frank_herbert, authors=[frank_herbert], country=us, genres=[planet_opera])
    dune.save()

    frank_herbert.books.append(dune)
    frank_herbert.save()

    us.add_book(dune)
    us.save()

    planet_opera.add_book(dune)
    planet_opera.save()

# end if
