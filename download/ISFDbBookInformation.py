# -*- coding: utf-8 -*-
#
# File : core/download/ISFDbBookInformation.py
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
import wikipedia
import re
from dateutil.parser import parse
import time
from urllib2 import urlopen
import urllib2


# Extract book information from isfdb.org
class ISFDbBookInformation(object):
    """
    Extract book information from isfdb.org
    """

    @staticmethod
    def get_book_information(book_url):
        """
        Get the book information.
        :param book_id: Book's ID
        :return: Array of information.
        """
        # Dict result
        result = dict()

        # Get HTML code
        errors = 0
        success = False
        while not success:
            try:
                html = urlopen(book_url).read()
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(book_url, unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {}".format(book_url))
                exit()
                # end if
        # end while

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # For all header information
        pub_header = soup.find('td', attrs={'class': u"pubheader"})
        for li in pub_header.find('ul').find_all('li', recursive=False):
            key = li.find('b').text.strip()[:-1]
            if key == "Date":
                value = parse(li.text.replace(key + u":", u"").strip()[:-3] + u"-01")
            elif key == "Pages":
                value = int(li.text.replace(key + u":", u"").strip())
            else:
                value = li.text.replace(key+u":", u"").replace(u"\n", u" ").strip()
            # end if
            result[key] = value
        # end for

        # Cover
        result['cover'] = soup.find('tr', attrs={'class': u"scan"}).find('img').attrs['src']

        return result
    # end get_book_information

# end
