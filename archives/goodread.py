# -*- coding: utf-8 -*-
#

import argparse

from goodreads import client

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
    parser = argparse.ArgumentParser(description="SFgram - Test GoodReads.")

    # Argument
    args = parser.parse_args()

    gc = client.GoodreadsClient("3H4jhs695dsDscTWMjKmw", "IGxF8r6Gg4FWPCQlPBpwkmQU2nZJWa6ZXCDRW7FtT5c")
    book = gc.search_books("The Time Machine")[0]
    print(book.title)
    print(book.authors)
    print(book.similar_books)
    print(book.description)
    print(book.is_ebook)
    print(book.publication_date)
    print(book.series_works)
    print(book.popular_shelves[0])
    print(book.popular_shelves[0].name)
    print(book.popular_shelves[0].count)
    print(book.popular_shelves[0])

# end if
