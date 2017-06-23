# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
import download as dw

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
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram MongoDB Movie database.")

    # Argument
    parser.add_argument("--database", type=str, help="Database name", default="sfgram", required=True)
    parser.add_argument("--page-index", type=int, help="Start page index", default=1)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # Statistics
    count = 0
    token_count = 0

    # Open category
    imdb_con = dw.IMDbMovieConnector()
    imdb_con.open("sci_fi", page_index=args.page_index)

    # For each book
    for index, movie in enumerate(imdb_con):
        logging.info(u"Movie {} ({}), {}, {}".format(movie.title, movie.year, movie.country, movie.language))
    # end for

# end if
