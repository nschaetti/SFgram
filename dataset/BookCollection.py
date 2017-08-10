# -*- coding: utf-8 -*-
#

# Imports
import os
import logging


# A collection of book in the dataset
class BookCollection(object):
    """
    A collection of book in the dataset
    """

    _next_book_id = 0

    ####################################################
    # Public
    ####################################################

    # Add a book
    def add(self, book):
        """
        Add a book
        :param book:
        :return:
        """
        # Next id
        self._next_book_id += 1
    # end add

    # Get next book id
    def get_next_book_id(self):
        """
        Get next book
        :return:
        """
        return self._next_book_id
    # end get_next_book_id

    ####################################################
    # Static
    ####################################################

    # Load book collection
    @staticmethod
    def load(filename):
        """
        Load book collection
        :param filename:
        :return:
        """
        pass
    # end load

    # Save cover
    @staticmethod
    def save_cover(data, ext):
        """
        Save cover
        :param data:
        :param ext:
        :return:
        """
        pass
    # end save_cover

    # Save cover art
    @staticmethod
    def save_cover_art(data, ext):
        """
        Save cover art
        :param data:
        :param ext:
        :return:
        """
        pass
    # end save_cover_art

    # Save image
    @staticmethod
    def save_image(directory, book_id, data, ext):
        """
        Save image
        :param directory:
        :param book_id:
        :param data:
        :param ext:
        :return:
        """
        # Extensions
        extensions = [".png", ".jpg", ".jpeg", ".gif"]

        # Find an index
        for i in range(1000):
            # Filename
            filename = u"book" + str(book_id) + u"-" + str(i)

            # Check no image file exists
            exists = False
            for ex in extensions:
                if os.path.exists(os.path.join(directory, filename + ex)):
                    exists = True
                # end if
            # end for

            # No image exists
            if not exists:
                image_filename = os.path.join(directory, filename + ext)
                logging.getLogger(u"SFGram").info(u"New book image at {}".format(image_filename))
                with open(image_filename, 'wb') as f:
                    f.write(data)
                # end with
                    break
            # end if
        # end for
        pass
    # end save_image

    # Save small image
    @staticmethod
    def save_small_image(data, ext):
        """
        Save small image
        :param data:
        :param ext:
        :return:
        """
        pass
    # end save_small_image

    # Save content
    @staticmethod
    def save_content(data, ext):
        """
        Save content
        :param data:
        :param ext:
        :return:
        """
        pass
    # end save_content

# end Book
