# -*- coding: utf-8 -*-
#

# Imports
import os
import logging
import pickle
import datetime
import json
from .Book import Book
from .Author import Author
from outputs.JsonEncoder import JsonEncoder


# A collection of book in the dataset
class BookCollection(object):
    """
    A collection of book in the dataset
    """

    _next_book_id = 0
    _next_author_id = 0
    _books = list()
    _authors = list()

    # Constructor
    def __init__(self, books=list(), authors=list()):
        """
        Constructor
        :param books: Books
        :param authors: Authors
        """
        self._books = books
        self._authors = authors

        # Search next book/author id
        self._next_book_id = self._get_next_id(books)
        self._next_author_id = self._get_next_id(authors)
    # end __init__

    ####################################################
    # Public
    ####################################################

    # Get authors
    def get_authors(self):
        """
        Get authors
        :return:
        """
        return self._authors
    # end get_authors

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
                if book.title == element.title and book.author_name == element.author_name:
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
                # Set ID
                element.id = self._next_book_id

                # Log
                logging.getLogger(u"SFGram").info(u"New book found {} ({}) with ID {}".format(element.title, element.author_name, element.id))

                # Add
                self._books.append(element)

                # Next id
                self._next_book_id += 1
            elif type(element) is Author:
                # Set ID
                element.id = self._next_author_id

                # Log
                logging.getLogger(u"SFGram").info(u"New author found {} with ID {}".format(element.name, element.id))

                # Add
                self._authors.append(element)

                # Next id
                self._next_author_id += 1
            # end if
        else:
            if type(element) is Book:
                return self.get_book_by_title(element.title)
            else:
                return self.get_author_by_name(element.name)
            # end if
        # end if

        return element
    # end add

    # Get book by title
    def get_book_by_title(self, title):
        """
        Get country by name
        :param title:
        :return:
        """
        for book in self._books:
            if book.title == title:
                return book
                # end if
        # end for
        return None
    # end get_by_name

    # Get book by ID
    def get_book_by_id(self, book_id):
        """
        Get country by name
        :param title:
        :return:
        """
        for book in self._books:
            if book.id == book_id:
                return book
                # end if
        # end for
        return None
        # end get_by_name

    # Get author by name
    def get_author_by_name(self, name):
        """
        Get country by name
        :param name:
        :return:
        """
        for author in self._authors:
            if author.name == name:
                return author
            # end if
        # end for
        return None
    # end get_by_name

    # Get author by ID
    def get_author_by_id(self, author_id):
        """
        Get author by ID
        :param author_id:
        :return:
        """
        for author in self._authors:
            if author.id == author_id:
                return author
            # end if
        # end for
        return None
    # end get_author_by_id

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

    # To dictionary
    def to_dict(self, collection_type):
        """
        To dictionary
        :return:
        """
        result = dict()

        # Collection
        if collection_type == 'books':
            collection = self._books
        else:
            collection = self._authors
        # end if

        # Books
        result[collection_type] = list()
        for element in collection:
            result[collection_type].append(element.to_dict())
        # end for

        return result
    # end to_dict

    # Get all books
    def get_books(self):
        """
        Get all books
        :return:
        """
        return self._books
    # end get_books

    ####################################################
    # Static
    ####################################################

    # Get next id
    def _get_next_id(self, collection):
        """
        Get next id
        :param collection:
        :return:
        """
        # Search next id
        max_id = 0
        for element in collection:
            if element.id > max_id:
                max_id = element.id
                # end if
        # end for
        return max_id + 1
    # end _get_next_id

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
        collection_json_filename = os.path.join(dataset_directory, directory + ".json")

        # Collection directory
        collection_directory = os.path.join(dataset_directory, directory)

        # Log
        logging.getLogger(u"SFGram").info(u"Saving collection to {}".format(collection_filename))

        # Save
        with open(collection_filename, 'wb') as f:
            pickle.dump(d, f)
        # end with

        # Save JSON
        with open(collection_json_filename, 'w') as f:
            json.dump(self.to_dict(directory), f, indent=4)
        # end with

        # For each book
        for element in d:
            element_filename = os.path.join(collection_directory, directory + unicode(element.id).zfill(5) + ".p")
            element_json_filename = os.path.join(collection_directory, directory + unicode(element.id).zfill(5) + ".json")

            # Save Pickle
            with open(element_filename, 'wb') as f:
                pickle.dump(element, f)
            # end with

            # Save JSON
            with open(element_json_filename, 'w') as f:
                json.dump(element.to_dict(), f, indent=4)
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
        book_collection_filename = os.path.join(dataset_directory, "books.p")
        author_collection_filename = os.path.join(dataset_directory, "authors.p")

        # Log
        logging.getLogger(u"SFGram").info(u"Loading book collection from {}".format(book_collection_filename))
        logging.getLogger(u"SFGram").info(u"Loading author collection from {}".format(author_collection_filename))

        # Load
        books = pickle.load(open(book_collection_filename, 'rb'))
        authors = pickle.load(open(author_collection_filename, 'rb'))

        # Return
        return books, authors
    # end load

    # Create collection
    @staticmethod
    def create(dataset_directory):
        """
        Create or load the collection
        :param dataset_directory:
        :return:
        """
        # Load or create book collection
        if os.path.exists(os.path.join(dataset_directory, "books.p")) and os.path.exists(
                os.path.join(dataset_directory, "authors.p")):
            books, authors = BookCollection.load(dataset_directory)
            return BookCollection(books=books, authors=authors)
        else:
            return BookCollection()
        # end if
    # end create

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
