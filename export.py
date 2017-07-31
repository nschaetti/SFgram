# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
import download as dw
import os
import io
import json
from db.Author import Author
from db.Book import Book
from db.Image import Image


######################################################
# Main
######################################################


# Transform Mongo list to unicode
def list_to_unicode(mongo_list):
    """
    Transform Mongo list to unicode
    :param mongo_list:
    :return:
    """
    result = list()
    for element in mongo_list:
        result.append(unicode(element))
    # end for
    return result
# end list_to_unicode

######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Export the database")

    # Argument
    parser.add_argument("--database", type=str, help="Database name", default="sfgram")
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

    # Create main dir
    if not os.path.exists(sfgram_dir):
        os.mkdir(sfgram_dir)
    # end if

    # Dirs
    dirs = dict()
    dirs["authors"] = os.path.join(os.path.join(sfgram_dir, "authors"))
    dirs["books"] = os.path.join(os.path.join(sfgram_dir, "books"))
    dirs["movies"] = os.path.join(os.path.join(sfgram_dir, "movies"))
    dirs["genres"] = os.path.join(os.path.join(sfgram_dir, "genres"))
    dirs["keywords"] = os.path.join(os.path.join(sfgram_dir, "keywords"))
    dirs["countries"] = os.path.join(os.path.join(sfgram_dir, "countries"))
    dirs["texts"] = os.path.join(os.path.join(sfgram_dir, "texts"))
    dirs["images"] = os.path.join(os.path.join(sfgram_dir, "images"))

    # Create authors dir
    for dir in dirs.keys():
        if not os.path.exists(dirs[dir]):
            os.mkdir(dirs[dir])
        # end if
    # end for

    # Export author
    for author in Author.objects():
        with io.open(os.path.join(dirs["authors"], str(author.id) + ".json"), 'wb') as f:
            logging.info(u"Writing author {}...".format(author.name))
            author_dict = author.to_mongo().to_dict()
            author_dict['id'] = unicode(author_dict['_id'])
            author_dict.pop('_id')
            author_dict['books'] = list_to_unicode(author_dict['books'])
            json.dump(author_dict, f)
        # end with
    # end for

    # Export books
    for book in Book.objects():
        with io.open(os.path.join(dirs["books"], str(book.id) + ".json"), 'w') as f:
            logging.info(u"Writing book {}...".format(book.title))
            book_dict = book.to_mongo().to_dict()

            # ID
            book_dict['id'] = unicode(book_dict['_id'])
            book_dict.pop('_id')

            # Authors
            book_dict['authors'] = list_to_unicode(book_dict['authors'])

            # Author
            book_dict['author'] = unicode(book_dict['author'])

            # No content
            book_dict.pop('content')

            # Genres
            book_dict['genres'] = list_to_unicode(book_dict['genres'])
            book_dict.pop('genres')

            # Similar books
            book_dict['similar_books'] = list_to_unicode(book_dict['similar_books'])

            # Country
            if 'country' in book_dict.keys():
                book_dict['country'] = unicode(book_dict['country'])
            # end if

            # Cover
            if 'cover' in book_dict:
                book_dict['cover'] = unicode(book_dict['cover'])
            # end if

            if 'covert_art' in book_dict:
                book_dict['covert_art'] = unicode(book_dict['covert_art'])
            # end if

            if 'small_image' in book_dict:
                book_dict['small_image'] = unicode(book_dict['small_images'])
            # end if

            # Images
            if 'images' in book_dict:
                book_dict['images'] = unicode(book_dict['images'])
            # end if

            # Write JSON
            f.write(unicode(json.dumps(book_dict, ensure_ascii=False)))

            # Write content
            with io.open(os.path.join(dirs['texts'], str(book.id) + ".txt"), 'w') as cf:
                logging.info(u"Writing books content {}...".format(book.title))
                cf.write(book.content)
            # end with
        # end with
    # end for

    # Export images
    for image in Image.objects():
        with io.open(os.path.join(dirs["images"], str(image.id) + image.extension), 'wb') as f:
            f.write(image.image.read())
        # end with
    # end for

# end if
