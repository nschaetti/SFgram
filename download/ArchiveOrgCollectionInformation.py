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


# Extract collection information from archive.org
class ArchiveOrgCollectionInformation(object):
    """
    Extract collection information from archive.org
    """

    ####################################################
    # Static
    ####################################################

    # Get item information
    @staticmethod
    def get_item_information(item_name):
        """
        Get item information
        :param item_name:
        :return:
        """
        # Dict result
        result = dict()

        # URL
        item_url = u"https://archive.org/details/{}&tab=about".format(item_name)

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

        # Get name
        result['name'] = soup.find('div', attrs={'class': u"welcome-left"}).find('h1').text.strip()

        # Get description
        result['description'] = soup.find('div', attrs={'class': u"about-box"}).text.replace(u"DESCRIPTION",
                                                                                             u"").strip()

        return result
    # end get_item_information

# end
