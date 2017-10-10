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
    parser = argparse.ArgumentParser(description="SFgram - Check author's wikipedia page")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    parser.add_argument("--start", type=int, help="Starting index", default=1)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # Author attributes
    author_attrs = ['bord', 'died', 'summary', 'bio']

    # For each author
    for author in book_collection.get_authors():
        if author.id >= args.start:
            # Show
            print(u"Author {} name {} date {}".format(author.id, author.name, author.birth_date))
            if 'url' in author.wikipedia:
                print(u"Wikipedia page : {}".format(author.wikipedia['url']))
            else:
                print(u"Wikipedia page : none")
            # end if
            print(u"Summary : {}".format(author.summary))

            # Ask
            print(u"Right page? (empty=keep, c=clear, other=new page) ")
            page_answer = raw_input(u"Page? ").strip()

            # No page
            if page_answer == u"c":
                # Set not found
                author.wikipedia = {'found': False}

                # Delete useless attributes
                for attr in author_attrs:
                    if hasattr(author, attr):
                        try:
                            delattr(author, attr)
                        except AttributeError:
                            pass
                        # end try
                    # end if
                # end for
            elif page_answer == u"":
                pass
            else:
                # Wikipedia informations
                wikipedia_info = wp.WikipediaBookInformation.get_author_information_from_url(author.name, page_answer)
                print(wikipedia_info)
                exit()
                # Wikipedia part
                author.wikipedia['url'] = page_answer
                author.wikipedia['found'] = True

                # For each attributes
                for attr in author_attrs:
                    try:
                        setattr(author, attr, wikipedia_info[attr])
                    except KeyError:
                        pass
                    # end try
                # end for
            # end if

            # Save
            book_collection.save(dataset.get_dataset_directory())
            print(u"")
        # end if
    # end for

# end if
