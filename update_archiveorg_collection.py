# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
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


def get_author(author_name):
    # Check if exists
    if Author.exists(author_name=author_name):
        return Author.get_by_name(author_name)
    else:
        return Author(name=author_name)
    # end if
# end create_author


def get_image(image_url):
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
            image.extension = ext

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
    parser.add_argument("--author", type=str, help="Corresponding author's name", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # AI collection
    collection = dw.ArchiveOrgCollection(args.collection)

    # Create or get author
    if Author.exists(author_name=args.author):
        author = Author.get_by_name(args.author)
    else:
        author = Author(name=args.author)
        author.save()
    # end if

    # List items
    for item in collection:
        # Get informations
        info = dw.ArchiveOrgBookInformation.get_item_information(item)
        isfdb_info = dw.ISFDbBookInformation.get_book_information(info['isfdb_link'])

        # If there is text
        if not info['content_error']:
            # Book's name
            book_title = isfdb_info['Title Reference'] + u" " + isfdb_info['Date'].strftime("(%B)")

            # Create of get book
            if Book.exists(book_title):
                book = Book.get_by_title(book_title)
            else:
                logging.info(u"New book {}".format(book_title))
                book = Book(title=book_title)
                book.save()
            # end if

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
            # end for

            # Get IA cover image
            if not info['cover_error']:
                book.cover = get_image(info['cover_image'])
            # end if

            # Get ISFDb cover image
            book.covert_art = get_image(isfdb_info['cover'])

            # Content
            book.content = info['content']

            # Save
            book.save()
            author.save()
        # end if
    # end for

# end if
