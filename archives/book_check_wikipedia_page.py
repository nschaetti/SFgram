# -*- coding: utf-8 -*-
#

import argparse
import wikipediaorg as wp
from archives import dataset as ds

######################################################
# Functions
######################################################

######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Check books' wikipedia page")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    parser.add_argument("--start", type=int, help="Starting index", default=1)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # For each book
    for book in book_collection.get_books():
        if book.id >= args.start:
            # Show
            print(u"Book {} title {} by {}".format(book.id, book.title, book.author_name))
            if 'url' in book.wikipedia:
                print(u"Wikipedia page : {}".format(book.wikipedia['url']))
            else:
                print(u"Wikipedia page : none")
            # end if
            print(u"Summary : {}".format(book.summary))

            # Ask
            print(u"Right page? (empty=keep, c=clear, other=new page) ")
            page_answer = raw_input(u"Page? ").strip()

            # No page
            if page_answer == u"c":
                # Set not found
                book.wikipedia = {'found': False}

                # Delete useless attributes
                for attr in ['original_title', 'cover_artist', 'publisher', 'published_in', 'plot', 'images', 'summary']:
                    if hasattr(book, attr):
                        try:
                            delattr(book, attr)
                        except AttributeError:
                            pass
                        # end try
                    # end if
                # end for
            elif page_answer == u"":
                pass
            else:
                # Wikipedia informations
                wikipedia_info = wp.WikipediaBookInformation.get_book_information_from_url(book.title,
                                                                                           book.author_name,
                                                                                           page_answer)

                # Wikipedia part
                book.wikipedia['url'] = page_answer
                book.wikipedia['found'] = True

                # Infos
                book.original_title = wikipedia_info['original_title'] if 'original_title' in wikipedia_info else None
                book.images = wikipedia_info['images'] if 'images' in wikipedia_info else None
                book.plot = wikipedia_info['plot'] if 'plot' in wikipedia_info else None
                book.cover_artist = wikipedia_info['cover_artist'] if 'cover_artist' in wikipedia_info else None
                book.publisher = wikipedia_info['publisher'] if 'publisher' in wikipedia_info else None
                book.publisher_in = wikipedia_info['publisher_in'] if 'publisher_in' in wikipedia_info else None
                book.summary = wikipedia_info['summary'] if 'summary' in wikipedia_info else None
            # end if

            # Save
            book_collection.save(dataset.get_dataset_directory())
            print(u"")
        # end if
    # end for

# end if
