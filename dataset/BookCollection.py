# -*- coding: utf-8 -*-
#

# Imports
import os
import logging
import pickle
from .Book import Book
from .Author import Author


# A collection of book in the dataset
class BookCollection(object):
    """
    A collection of book in the dataset
    """

    _next_book_id = 0
    _next_author_id = 0
    _books = list()
    _authors = list()

    ####################################################
    # Public
    ####################################################

    # Exists
    def exists(self, element):
        """
        Book exists
        :param book_title:
        :param book_author:
        :return:
        """
        if type(element) is Book:
            for book in self._books:
                if book.title == element.title:
                    return True
                # end if
            # end for
        elif type(element) is Author:
            for author in self._authors:
                if author.name == element.name:
                    return True
                # end if
            # end for
        # end if
        return False
    # end book_exists

    # Add a book
    def add(self, element):
        """
        Add a book
        :param book:
        :return:
        """
        if not self.exists(element):
            if type(element) is Book:
                # Log
                logging.getLogger(u"SFGram").info(u"New book found {}".format(element.title))

                # Set ID
                element.id = self._next_book_id

                # Add
                self._books.append(element)

                # Next id
                self._next_book_id += 1
            elif type(element) is Author:
                # Log
                logging.getLogger(u"SFGram").info(u"New author found {}".format(element.name))

                # Set ID
                element.id = self._next_author_id

                # Add
                self._authors.append(element)

                # Next id
                self._next_author_id += 1
            # end if
        # end if

        return element
    # end add

    # Get next book id
    def get_next_book_id(self):
        """
        Get next book
        :return:
        """
        return self._next_book_id
    # end get_next_book_id

    # Save the collection
    def save(self, dataset_directory):
        """
        Save the collection
        :param dataset_directory:
        :return:
        """
        # Save books
        self._save_dict(self._books, dataset_directory, "books.p", "books")

        # Save authors
        self._save_dict(self._authors, dataset_directory, "authors.p", "authors")
    # end save

    ####################################################
    # Static
    ####################################################

    # Save variable
    def _save_dict(self, d, dataset_directory, filename, directory):
        """
        Save dictionary
        :param dict:
        :param filename:
        :param directory:
        :return:
        """
        # Collection file
        collection_filename = os.path.join(dataset_directory, filename)

        # Collection directory
        collection_directory = os.path.join(dataset_directory, directory)

        # Log
        logging.getLogger(u"SFGram").info(u"Saving collection to {}".format(collection_filename))

        # Save
        with open(collection_filename, 'wb') as f:
            pickle.dump(d, f)
        # end with

        # For each book
        for element in d:
            element_filename = os.path.join(collection_directory, directory + unicode(element.id).zfill(5) + ".p")
            with open(element_filename, 'wb') as f:
                pickle.dump(element, f)
                # end with
        # end for
    # end _save_dict

    ####################################################
    # Static
    ####################################################

    # Load book collection
    @staticmethod
    def load(dataset_directory):
        """
        Load book collection
        :param filename:
        :return:
        """
        # Collection file
        collection_filename = os.path.join(dataset_directory, "books.p")

        # Log
        logging.getLogger(u"SFGram").info(u"Loading collection from {}".format(collection_filename))

        # Load
        with open(collection_filename, 'rb') as f:
            return pickle.load(collection_filename)
        # end with
    # end load

    # Save image in subdir
    @staticmethod
    def save_image_in_dir(directory, subdirectory, book_id, data, name):
        """
        Save image in subdir
        :param directory:
        :param subdirectory:
        :param book_id:
        :param data:
        :param name:
        :return:
        """
        # Filename
        filename = u"book" + unicode(book_id).zfill(5) + u"-" + name

        # Content directory
        content_directory = os.path.join(directory, subdirectory)

        # No image exists
        if not os.path.exists(os.path.join(content_directory, filename)):
            image_filename = os.path.join(content_directory, filename)
            logging.getLogger(u"SFGram").info(u"New book {} at {}".format(subdirectory, image_filename))
            with open(image_filename, 'wb') as f:
                f.write(data)
            # end with
        # end if
    # end save_image_in_dir

    # Save cover
    @staticmethod
    def save_cover(directory, book_id, data, name):
        """
        Save cover
        :param data:
        :param ext:
        :return:
        """
        BookCollection.save_image_in_dir(directory, "book-covers", book_id, data, name)
    # end save_cover

    # Save cover art
    @staticmethod
    def save_cover_art(directory, book_id, data, name):
        """
        Save cover art
        :param data:
        :param ext:
        :return:
        """
        BookCollection.save_image_in_dir(directory, "book-cover-arts", book_id, data, name)
    # end save_cover_art

    # Save image
    @staticmethod
    def save_image(directory, book_id, data, name):
        """
        Save image
        :param directory:
        :param book_id:
        :param data:
        :param ext:
        :return:
        """
        BookCollection.save_image_in_dir(directory, "book-images", book_id, data, name)
    # end save_image

    # Save content
    @staticmethod
    def save_content(directory, book_id, data):
        """
        Save content
        :param data:
        :param ext:
        :return:
        """
        # Filename
        filename = u"book" + unicode(book_id).zfill(5) + u".txt"

        # Content directory
        content_directory = os.path.join(directory, u"book-contents")

        # No image exists
        if not os.path.exists(os.path.join(content_directory, filename)):
            content_filename = os.path.join(content_directory, filename)
            logging.getLogger(u"SFGram").info(u"New book content at {}".format(content_filename))
            with open(content_filename, 'wb') as f:
                f.write(data)
            # end with
        # end if
    # end save_content

# end Book
