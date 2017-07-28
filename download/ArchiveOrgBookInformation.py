# -*- coding: utf-8 -*-
#
# File : core/download/ArchiveOrgBookInformation.py
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

import internetarchive
import logging
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup


# Extract book information from arcive.org
class ArchiveOrgBookInformation(object):
    """
    Extract book information from arcive.org
    """

    ####################################################
    # Static
    ####################################################

    # Get item information
    @staticmethod
    def get_item_information(item):
        """
        Get item information
        :param identifier:
        :return:
        """
        # Dict result
        result = dict()

        # URL
        item_url = u"https://archive.org/details/{}".format(item.identifier)
        cover_url = u"https://{}/BookReader/BookReaderImages.php?zip={}/{}_jp2.zip" \
                    u"&file={}_jp2/{}_0000.jp2&scale=0&rotate=0"
        text_url = u"https://archive.org/stream/{}/{}_djvu.txt"

        # Get HTML code
        errors = 0
        success = False
        while not success:
            try:
                html = urlopen(item_url).read()
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(item_url, unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {}".format(item_url))
                exit()
            # end if
        # end while

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Get author
        result['authors'] = list()
        descript = soup.find('div', attrs={'id': u'descript'})
        try:
            for li in descript.find_all('li'):
                result['authors'].append(li.text.split(u"by")[1].strip())
            # end for
        except AttributeError:
            pass
        # end try

        # Get cover
        cover_url = cover_url.format(item.server, item.dir, item.identifier, item.identifier, item.identifier)

        # Get cover
        try:
            data = urlopen(cover_url).read()
            result['cover_error'] = False
        except urllib2.HTTPError as e:
            logging.error(u"HTTP error trying to retrieve cover {} : {}".format(cover_url, unicode(e)))
            result['cover_error'] = True
            pass
        # end try

        # Check if error
        if not result['cover_error'] and u'error' not in data.decode('utf-8', errors='ignore'):
            result['cover_image'] = cover_url.format(item.server, item.dir, item.identifier, item.identifier,
                                                     item.identifier)
        # end if

        # Search ISFDB link
        for link in soup.find_all('a'):
            if link.text.strip() == u"The Internet Speculative Fiction Database":
                result['isfdb_link'] = link.attrs['href']
                break
            # end if
        # end for

        # Get text page
        try:
            text_url = text_url.format(item.identifier, item.identifier)
            html = urlopen(text_url).read()
            soup = BeautifulSoup.BeautifulSoup(html, "lxml")
            text = soup.find('div', attrs={'class': u"container"}).find('pre')\
                .text.replace(u"\n", u". ").replace(u"..", u".").replace(u"  ", u" ").strip()
            for i in range(10):
                text = text.replace(u". . ", u". ")
            # end for
            result['content'] = text
            result['content_error'] = False
        except AttributeError:
            logging.error(u"Text not found for {}".format(item.identifier))
            result['content_error'] = True
            pass
        # end try

        # Delete
        del soup
        del html

        return result
    # end get_item_information

    # Get internet archive item
    @staticmethod
    def get_item(item_name):
        """
        Get the book information.
        :param item_name: Archive item's name
        :return: Item object.
        """
        internetarchive.get_item(item_name)
    # end get_book_information

# end
