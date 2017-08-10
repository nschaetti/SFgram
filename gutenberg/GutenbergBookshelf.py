# -*- coding: utf-8 -*-
#

import logging
from GutenbergBookInformation import GutenbergBookInformation
from cleaning.TextCleaner import TextCleaner
from tools.Tools import Tools
import spacy
from dataset.Book import Book


# Download error
class DownloadErrorException(Exception):
    """
    Download error exception
    """
    pass
# end DownloadErrorException


# Class to list a Gutenberg category
class GutenbergBookshelf(object):
    """
    Tool class to list a Gutenberg bookshelf.
    """

    # Properties
    _skip_book = list()

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self._url = u"http://www.gutenberg.org/ebooks/bookshelf/"
        self._plaintext_url = u"http://www.gutenberg.org/ebooks/{}.txt.utf-8"
        self._start_index = 1
        self._step = 25
        self._books = list()
    # end __init__

    ####################################################
    # Public
    ####################################################

    # Open the category for listing
    def open(self, num, start_index=1, skip_book=0):
        """
        Open a category for listing
        :param num: The category number.
        :param start_index: Start page index
        :param skip_book: How many book to skip
        """
        # Final URL
        self._url += str(num)

        # Start index
        self._start_index = start_index

        # Skip book
        self._skip_book = skip_book
    # end open

    ####################################################
    # Override
    ####################################################

    # Next element
    def next(self):
        """
        Next element
        """
        # If book list is empty, we reload
        if len(self._books) == 0:
            self._load()
        # end if

        # Current book
        book_url = self._books[0]

        # Gutenberg information
        book_informations = GutenbergBookInformation.get_book_info(book_url)

        # Get images
        book_informations['images'] = GutenbergBookshelf.download_images(book_informations['images-urls'])

        # Get content
        try:
            # Download HTTP
            content_ext, content_data = Tools.download_http_file(self._plaintext_url.format(book_informations['#']))

            # Clean content
            cleaned_content, cleaned = GutenbergBookshelf.clean_content(content_data)

            # Save
            book_informations['content'] = cleaned_content
            book_informations['content-extension'] = content_ext
            book_informations['content-cleaned'] = cleaned
        except DownloadErrorException as e:
            logging.getLogger(u"SFGram").error(
                u"Error downloading book content {} : {}".format(book_informations['title'], e))
            pass
        # end try

        # Get cover art
        try:
            # Download HTTP file
            cover_art_ext, cover_art_data = Tools.download_http_file(book_informations['cover-art-url'])

            # Save
            book_informations['cover-art'] = cover_art_data
            book_informations['cover-art-extension'] = cover_art_ext
        except KeyError:
            pass
        except DownloadErrorException as e:
            logging.getLogger(u"SFGram").error(
                u"Error downloading book cover art for {} : {}".format(book_informations['title'], e))
            pass
        # end try

        # Remove from the list
        self._books.remove(book_url)

        # Return current book info
        return book_informations
    # end next

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return: object.
        """
        return self
    # end __iter__

    ####################################################
    # Private
    ####################################################

    # Load elements
    def _load(self):
        """
        Load the elements of the current page.
        """
        # URL
        book_url = u"{}?start_index={}".format(self._url, self._start_index)

        # Get and parse HTML
        try:
            soup = Tools.download_html(book_url)
        except DownloadErrorException:
            logging.getLogger(u"SFGram").fatal(u"Can't get HTML page {}".format(book_url))
            exit()
        # end try

        # Find all 'booklink'
        book_links = soup.find_all('li', attrs={"class": u"booklink"})

        # For all book link
        skip = 0
        for book_link in book_links:
            if skip >= self._skip_book:
                self._skip_book = 0
                self._books.append(GutenbergBookshelf._parse_book_link(book_link))
            else:
                skip += 1
            # end if
        # end for

        # Next page
        self._start_index += self._step
    # end _load

    ####################################################
    # Static
    ####################################################

    # Parse book link
    @staticmethod
    def _parse_book_link(book_link):
        """
        Parse book link and return book number.
        :param book_link: The Gutenberg URL of the book.
        :return: Book number.
        """
        book_url = book_link.find('a').attrs['href']
        return int(book_url[book_url.rfind("/") + 1:])
    # end _parse_book_link

    # Download content
    @staticmethod
    def download_content(content_url):
        """
        Download content
        :param content_url:
        :return:
        """
        # Download
        return Tools.download_http_file(content_url)
    # end download_content

    # Clean content
    @staticmethod
    def clean_content(content):
        """
        Clean content
        :param content:
        :return:
        """
        # Clean content
        cleaner = TextCleaner()
        return cleaner(content.decode('utf8', errors='ignore'))
    # end clean_content

    # Get number of tokens
    @staticmethod
    def get_n_tokens(content, language):
        """
        Get number of tokens
        :param content:
        :param language:
        :return:
        """
        # New parser
        if language.lower() == u"english":
            nlp = spacy.load('en')
            words = nlp(content)
            return len(words)
        elif language.lower() == u"french":
            nlp = spacy.load('fr')
            words = nlp(content)
            return len(words)
        # end if
        return 0
    # end get_n_tokens

    # Download images
    @staticmethod
    def download_images(urls):
        """
        Download images
        :param urls:
        :return:
        """
        # All images
        images = list()

        # For each image url
        for url in urls:
            # Add
            try:
                images.append(Tools.download_http_file(url))
            except DownloadErrorException as e:
                logging.getLogger(u"SFGram").error(u"Error downloading image {} : {}".format(url, e))
                pass
            # end try
        # end for
        return images
    # end _download_images

# end GutenbergBookshelf
