# -*- coding: utf-8 -*-
#

import argparse
import logging
import gutenberg as gb

######################################################
#
# Functions
#
######################################################


"""def get_author(author_name):
    # Check if exists
    if Author.exists(author_name=author_name):
        return Author.get_by_name(author_name)
    else:
        return Author(name=author_name)
    # end if
# end create_author"""

######################################################
#
# Main
#
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram book dataset")

    # Argument
    parser.add_argument("--output-dir", type=str, help="Output directory", required=True)
    parser.add_argument("--start-index", type=int, help="Start page index", default=1)
    parser.add_argument("--skip-book", type=int, help="Number of books to skip", default=0)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name=u"SFGram")

    # Open category
    gutenberg_con = gb.GutenbergBookshelf()
    gutenberg_con.open(num=68, start_index=args.start_index, skip_book=args.skip_book)

    # For each book
    for index, book in enumerate(gutenberg_con):
        print(book)
        # Registered
        """logging.info(u"Book {} ({}), {} ({}) saved/updated in database".format(book.title, book.publication_date,
                                                                       book.author.name,
                                                                       book.country.name if book.country is not None
                                                                       else ""))

        # Save book in DB
        book.save()"""
    # end for

# end if
