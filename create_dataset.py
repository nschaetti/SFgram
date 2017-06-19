# -*- coding: utf-8 -*-
#

import argparse
import os
import re
import logging
import core.cleaning as cl
import core.download as dw

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
    parser.add_argument("--output", type=str, help="Output dataset directory", default=".", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

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
        if not book.downloaded(args.output):
            logger.info("Saving book %d, %s by %s, %d" % (book.get_num(), book.get_title(), book.get_author()[0],
                                                      book.get_attr("Publication date")))
            book.save(args.output)
        # end if
    # end for

    # Print information
    print("Imported: %d novels, %d tokens" % (count, token_count))

# end if
