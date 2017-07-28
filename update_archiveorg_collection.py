# -*- coding: utf-8 -*-
#

import argparse
import logging
import time
from mongoengine import *
import psutil
import os
import download as dw
from db.Author import Author
from db.Book import Book
from db.Country import Country
from db.Genre import Genre
from db.Image import Image
from tools.Tools import Tools

######################################################
#
# Functions
#
######################################################


# Get an author
def get_author(author_name):
    """
    Get an author
    :param author_name:
    :return:
    """
    # Check if exists
    if Author.exists(author_name=author_name):
        return Author.get_by_name(author_name)
    else:
        return Author(name=author_name)
    # end if
# end create_author


# Get image data
def get_image(image_url, image_ext=""):
    """
    Get image data
    :param image_url:
    :return:
    """
    # Get/create image
    if image_url != "":
        if not Image.exists(image_url):
            # New image
            image = Image()

            # Data
            ext, data = Tools.download_http_file(image_url)

            # Info
            image.image.put(data)
            image.url = image_url
            if image_ext == "":
                image.extension = ext
            else:
                image.extension = image_ext
            # end if

            # Save
            image.save()
        else:
            image = Image.get_by_url(image_url)
        # end if
    # end if
    return image
# end get_image


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
    parser.add_argument("--collection", type=str, help="Collection's name", required=True)
    #parser.add_argument("--author", type=str, help="Corresponding author's name", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # AI collection
    collection = dw.ArchiveOrgCollection(args.collection)

    # Get collection information
    collection_info = dw.ArchiveOrgCollectionInformation.get_item_information(args.collection)

    # Create or get author
    if Author.exists(author_name=collection_info['name']):
        author = Author.get_by_name(collection_info['name'])
    else:
        logging.info(u"New author {}".format(collection_info['name']))
        author = Author(name=collection_info['name'])
        author.bio = collection_info['description']
        author.save()
    # end if

    # Debug
    pid = os.getpid()
    py = psutil.Process(pid)

    # List items
    for item in collection:
        # Log
        logging.debug(u"Memory used 1: {}".format(py.memory_info()[0] / 2. ** 30))

        # Get informations
        info = dw.ArchiveOrgBookInformation.get_item_information(item)
        isfdb_info = dw.ISFDbBookInformation.get_book_information(info['isfdb_link'])

        # If there is text
        if not info['content_error']:
            # Book's name
            book_title = isfdb_info['Title Reference'] + u" " + isfdb_info['Date'].strftime("(%B)")

            # Create of get book
            if not Book.exists(book_title):
                logging.info(u"New book {}".format(book_title))
                book = Book(title=book_title)
                book.save()

                # Properties
                book.author = author
                if book not in author.books:
                    author.books.append(book)
                    author.n_books += 1
                # end if
                book.publication_date = isfdb_info['Date'].year

                # For each authors
                for au in info['authors']:
                    if Author.exists(author_name=au):
                        add_author = Author.get_by_name(au)
                    else:
                        add_author = Author(name=au)
                        add_author.save()
                    # end if
                    book.authors.append(add_author)
                    if book not in add_author.books:
                        add_author.books.append(book)
                        add_author.n_books += 1
                    # end if
                    add_author.save()
                    del add_author
                # end for

                # Get IA cover image
                if not info['cover_error']:
                    book.cover = get_image(info['cover_image'], ".jpg")
                # end if

                # Get ISFDb cover image
                book.covert_art = get_image(isfdb_info['cover'])

                # Content
                book.content = info['content']

                # Save
                book.save()
                author.save()

                # Delete
                del book
            # end if
        # end if

        # Delete info
        del info
        del isfdb_info
        del item
    # end for

# end if
