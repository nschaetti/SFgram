# -*- coding: utf-8 -*-
#
# File : core/download/GoodReadsConnector.py
#
# This file is part of pySpeeches.  pySpeeches is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Nils Schaetti, University of Neuchâtel <nils.schaetti@unine.ch>

import bs4 as BeautifulSoup
import logging
import time
from urllib2 import urlopen
import requests
from requests.utils import quote
import goodreads
from goodreads import client
from tools.Tools import Tools


# Connector for GoodReads
class GoodReadsConnector(object):

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self._base_url = u"https://www.goodreads.com"
    # end __init__

    # Search for a book
    @staticmethod
    def search_book(title):
        """
        Search for a book
        :param title:
        :return:
        """
        # Search
        search_url = u"https://www.goodreads.com/search?utf8=%E2%9C%93&q={}%20-cd&search_type=books"
        base_url = u"https://www.goodreads.com"

        # Load HTML
        logging.getLogger(name="SFGram").debug(u"Retrieving GoodReads URL from %s" %
                                               search_url.format(quote(title, safe='')))
        html = urlopen(search_url.format(quote(title, safe=''))).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find book title link
        book_link = soup.find('a', attrs={'class': u"bookTitle"}).attrs["href"]

        return base_url + book_link
    # end search_book

    # Get book's info
    @staticmethod
    def get_book_info(title):
        """
        Get book's information
        :param title: Link to the page
        :return:
        """
        # Result
        info = {'goodreads': {'found': False}}

        # Goodreads client
        goodreads_client = client.GoodreadsClient("3H4jhs695dsDscTWMjKmw",
                                                  "IGxF8r6Gg4FWPCQlPBpwkmQU2nZJWa6ZXCDRW7FtT5c")

        # Empty genre list
        info['classes'] = list()

        # Search books
        ok = False
        while not ok:
            try:
                success = False
                while not success:
                    try:
                        books = goodreads_client.search_books(title)
                        success = True
                    except requests.exceptions.ConnectionError:
                        time.sleep(60)
                        pass
                    # end try
                # end while

                # Continue
                ok = True
            except goodreads.request.GoodreadsRequestException:
                logging.getLogger(name=u"SFGram").warning(u"Error when retrieving information from Goodreads for {}"
                                                         .format(title))
                # end if
                time.sleep(10)
                pass
            except TypeError:
                logging.getLogger(name=u"SFGram").warning(u"Book \"{}\" not found on GoodReads".format(title))
                info['goodreads']['found'] = False
                return info
            # end try
        # end while
        time.sleep(10)

        # No ebooks
        book = books[0]
        for b in books:
            if not book.is_ebook:
                book = b
            # end if
        # end for

        # Get informations
        info['isbn13'] = book.isbn13
        info['isbn'] = book.isbn
        info['similar_books'] = list()
        info['cover'] = book.image_url
        info['small_image'] = Tools.download_http_file(book.small_image_url)
        info['goodreads']['url'] = book.link
        info['description'] = book.description

        # Book rating
        if book.average_rating is not None:
            info['average_rating'] = float(book.average_rating)
        # end if

        # Language code
        info['language_code'] = book.language_code

        # Book rating
        if book.ratings_count is not None:
            info['rating_count'] = int(book.ratings_count)
        # end if

        # Number of pages
        if book.num_pages is not None:
            info['pages'] = int(book.num_pages)
        # end if

        # Book format
        info['format'] = book.format

        # Publication date
        if '#text' in book.work['original_publication_year']:
            info['goodreads']['year'] = int(book.work['original_publication_year']['#text'])
        else:
            info['goodreads']['year'] = -1
        # end if

        # Similar books
        try:
            for b in book.similar_books:
                info['similar_books'].append(b.title)
            # end for
        except KeyError:
            info['similar_books'] = list()
        # end try

        # Genres
        try:
            for shelf in book.popular_shelves:
                info['classes'].append(shelf.name)
            # end
        except TypeError:
            info['classes'] = list()
        # end try

        # Found
        info['goodreads']['found'] = True
        logging.getLogger(name=u"SFGram").info(u"Goodreads page found at {}".format(book.link))

        return info
    # end get_book_information

    # Get genres
    @staticmethod
    def get_genres(soup):
        """
        Get genres
        :param soup:
        :return:
        """
        result = list()

        # Filters
        filters = [u"Science Fiction", u"Fiction", u"Literature", u"Audiobook"]

        # Right container
        right_container = soup.find('div', attrs={'class': u"rightContainer"})
        for page_genre_link in right_container.find_all('a', attrs={'class': u"bookPageGenreLink"}):
            if 'greyText' not in page_genre_link['class']:
                element_name = page_genre_link.text.strip()
                if element_name not in filters:
                    result.append(element_name.title())
                # end if
            # end if
        # end for
        return result
    # end _get_genres

    # Get DataBox information
    @staticmethod
    def get_databox_information(soup):
        """
        Get DataBox information.
        :param soup:
        :return:
        """
        result = dict()

        # Data box
        databox_div = soup.find('div', attrs={'id': u"bookDataBox"})

        # Foreach clearFloats
        for entry in databox_div.find_all('div', attrs={'class': u"clearFloats"}):
            field_name = entry.find('div', attrs={'infoBoxRowTitle'}).text.strip()
            field_value = entry.find('div', attrs={'infoBoxRowItem'}).text.strip()
            result[field_name] = field_value
        # end for
        return result
    # end _get_databox_information

# end GoodReadsConnector
