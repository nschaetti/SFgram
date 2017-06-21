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
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram MongoDB database.")

    # Argument
    parser.add_argument("--database", type=str, help="Database name", default="sfgram", required=True)
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
    gutenberg_con = dw.GutenbergBookshelf()
    gutenberg_con.open(68)

    # GoodReads connector
    goodreads_con = dw.GoodReadsConnector()

    # For each book
    for index, book in enumerate(gutenberg_con):
        """if not book.downloaded(args.output):
            logger.info("Saving book %d, %s by %s, %d" % (book.get_num(), book.get_title(), book.get_author()[0],
                                                      book.get_attr("Publication date")))
            book.save(args.output)
        # end if"""
        print(book)
    # end for

    # Print information
    print("Imported: %d novels, %d tokens" % (count, token_count))

# end if
