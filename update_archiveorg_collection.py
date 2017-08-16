# -*- coding: utf-8 -*-
#

import argparse
import logging
import time
from mongoengine import *
import psutil
import os
import download as dw
import wikipediaorg as wp
import dataset as ds
import goodreadscom as gr
import gutenberg as gb
import internetarchiveorg as ia
import isfdb
from tools.Tools import Tools
import hashlib

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

            if hashlib.md5(data).hexdigest() == "25403b9749d2de7454a4f7c0124443b7":
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
                return None
            # end if
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
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram archive.org collection in the dataset")

    # Argument
    parser.add_argument("--output-dir", type=str, help="Output directory", required=True)
    parser.add_argument("--collection", type=str, help="Collection's name", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Dataset
    dataset = ds.Dataset(args.output_dir)
    dataset.check_directories()

    # Load or create collections
    book_collection = ds.BookCollection.create(args.output_dir)
    country_collection = ds.CountryCollection.create(args.output_dir)
    year_collection = ds.CountryCollection.create(args.output_dir)

    # AI collection
    collection = ia.ArchiveOrgCollection(args.collection)

    # Get collection information
    collection_info = ia.ArchiveOrgCollectionInformation.get_item_information(args.collection)

    # Create author
    author = ds.Author(name=collection_info['name'])
    author = book_collection.add(author)

    # Authors books
    author_books = dict()

    # List items
    for item in collection:
        # Get informations
        info = ia.ArchiveOrgBookInformation.get_item_information(item)
        try:
            isfdb_info = isfdb.ISFDbBookInformation.get_book_information(info['isfdb_link'])
        except KeyError:
            continue
        # end try

        # If there is text
        if not info['content_error']:
            # Book's name
            book_title = isfdb_info['Title Reference'] + u" " + isfdb_info['Date'].strftime("(%B)")

            # Create of get book
            if not Book.exists(book_title):
                logging.info(u"New book {}".format(book_title))
                book = Book(title=book_title)
                book.save()

                # For each authors
                for au in info['authors']:
                    if Author.exists(author_name=au):
                        add_author = Author.get_by_name(au)
                    else:
                        add_author = Author(name=au)
                        author_books[au] = list()
                        add_author.save()
                    # end if

                    # Add author to book's authors
                    if add_author not in book.authors:
                        book.authors.append(add_author)
                        book.save()
                    # end if

                    del add_author
                # end for

                # Properties
                book.author = author
                author.books.append(book)
                author.n_books += 1
                book.publication_date = isfdb_info['Date'].year
                book.format = "Magazine"

                # Get IA cover image
                if not info['cover_error']:
                    cover_image = get_image(info['cover_image'], ".jpg")
                    if cover_image is not None:
                        book.cover = get_image(info['cover_image'], ".jpg")
                    # end if
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
    # end for

# end if
