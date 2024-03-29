# -*- coding: utf-8 -*-
#

# Imports
import os


# Dataset
class Dataset(object):
    r"""A general sfgram dataset object.
    """

    # Properties
    _directories = ["book-covers", "book-images", "book-contents", "books", "authors"]

    # Constructor
    def __init__(self, dataset_dir):
        """
        Constructor
        :param dataset_dir:
        """
        self._dataset_directory = dataset_dir
    # end __init__

    # region PUBLIC

    # Check dataset directories
    def check_directories(self):
        """
        Check dataset directories
        :param dataset_dir:
        :return:
        """
        # Check each dir
        for directory in self._directories:
            if not os.path.exists(os.path.join(self._dataset_directory, directory)):
                os.mkdir(os.path.join(self._dataset_directory, directory))
            # end if
        # end for
    # end add

    # Get dataset directory
    def get_dataset_directory(self):
        """
        Get dataset directory
        :return:
        """
        return self._dataset_directory
    # end get_dataset_directory

    # Get book covers directory
    def get_book_covers_directory(self):
        """
        Get book covers directory
        :return:
        """
        return os.path.join(self._dataset_directory, self._directories[0])
    # end get_book_covers_directory

    # Get book images directory
    def get_book_images_directory(self):
        """
        Get book images directory
        :return:
        """
        return os.path.join(self._dataset_directory, self._directories[2])
    # end get_book_covers_directory

    # endregion PUBLIC

    # region STATIC

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
    def save_image(data, ext):
        """
        Save image
        :param data:
        :param ext:
        :return:
        """
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

    # enregion STATIC

# end Book
