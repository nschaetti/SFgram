# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
import download as dw
import os
import io
from db.Author import Author
from db.Book import Book


######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Export the database")

    # Argument
    parser.add_argument("--output", type=str, help="Output dataset directory", default=".", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # Main dir
    sfgram_dir = os.path.join(args.output, "sfgram")

    # Dirs
    dirs = dict()
    dirs["authors"] = os.path.exists(os.path.join(sfgram_dir, "authors"))
    dirs["books"] = os.path.exists(os.path.join(sfgram_dir, "books"))
    dirs["covers"] = os.path.exists(os.path.join(sfgram_dir, "covers"))
    dirs["posters"] = os.path.exists(os.path.join(sfgram_dir, "posters"))
    dirs["movies"] = os.path.exists(os.path.join(sfgram_dir, "movies"))
    dirs["genres"] = os.path.exists(os.path.join(sfgram_dir, "genres"))
    dirs["keywords"] = os.path.exists(os.path.join(sfgram_dir, "keywords"))
    dirs["countries"] = os.path.exists(os.path.join(sfgram_dir, "countries"))

    # Create authors dir
    for dir in dirs:
        if os.path.exists(dir):
            os.mkdir(dir)
        # end if
    # end for

    # Export author
    for author in Author.objects():
        with io.open(os.path.join(dirs["authors"], author.id + ".json"), 'w') as f:
            logging.info(u"Writing author {}...".format(author.name))
            f.write(author.to_json())
        # end with
    # end for

    # Export books
    for book in Book.objects():
        with io.open(os.path.join(dirs["books"], book.id + ".json"), 'w') as f:
            logging.info(u"Writing book {}...".format(book.title))
            f.write(book.to_json())
        # end with
    # end for

# end if
