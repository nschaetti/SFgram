# -*- coding: utf-8 -*-
#

import argparse
import logging
import os
import wikipediaorg as wp
import dataset as ds
import goodreadscom as gr
import gutenberg as gb
from dataset.CountryCollection import CountryCollection
from dataset.Country import Country

######################################################
# Functions
######################################################

######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Check books' goodreads page")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    parser.add_argument("--start", type=int, help="Starting index", default=1)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # Attributes
    gr_attrs = ['classes', 'isbn13', 'isbn', 'similar_books', 'description', 'language_code', 'rating_count', 'pages', 'similar_books']

    # For each book
    for book in book_collection.get_books():
        if book.id >= args.start:
            # Show
            print(u"Book {} title {} by {}".format(book.id, book.title, book.author_name))
            if 'url' in book.goodreads:
                print(u"Goodreads page : {}".format(book.goodreads['url']))
            else:
                print(u"Goodreads page : none")
            # end if
            print(u"Summary : {}".format(book.description))

            # Ask
            print(u"Right page? (empty=keep, c=clear, other=new page) ")
            page_answer = raw_input(u"Page? ").strip()

            # Delete format
            try:
                delattr(book, 'format')
            except KeyError:
                pass
            # end try

            # No page
            if page_answer == u"c":
                # Set not found
                book.goodreads = {'found': False}

                # Delete useless attributes
                for attr in gr_attrs:
                    if hasattr(book, attr):
                        try:
                            delattr(book, attr)
                        except AttributeError:
                            pass
                        # end try
                    # end if
                # end for
                pass
            elif page_answer == u"":
                pass
            else:
                # Goodread informations
                goodreads_info = gr.GoodReadsConnector.get_book_info_url(book.title, book.author_name, page_answer)

                # Goodreads part
                book.goodreads = {'url': page_answer, 'found': True}

                # Found
                if goodreads_info is not None:
                    # Info
                    for attr in gr_attrs:
                        try:
                            setattr(book, attr, goodreads_info[attr])
                        except KeyError:
                            delattr(book, attr)
                        # end try
                    # end for
                else:
                    print(u"Not found...")
                    exit()
                # end if
            # end if

            # Save
            book_collection.save(dataset.get_dataset_directory())
            print(u"")
        # end if
    # end for

# end if
