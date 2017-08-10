# -*- coding: utf-8 -*-
#

# Import
import os
import logging
import bs4 as BeautifulSoup
import urllib2
from urllib2 import urlopen
import socket


# Download error
class DownloadErrorException(Exception):
    """
    Download error exception
    """
    pass
# end DownloadErrorException


# Toolbox
class Tools(object):
    """
    Toolbox
    """

    @staticmethod
    def download_html(url, limit=10):
        """
        Download HTML
        :param url: Page's URL
        :param limit: Limit of try
        :return: BeautifulSoup parsed HTML
        """
        # Control
        errors = 0
        last_error = None

        # Try downloading
        while errors < limit:
            try:
                logging.getLogger(u"SFGram").debug(u"Downloading HTML page {}".format(url))
                html = urlopen(url).read()
                return BeautifulSoup.BeautifulSoup(html, "lxml")
            except urllib2.HTTPError as e:
                logging.getLogger(u"SFGram").error(u"HTTP error trying to retrieve {} : {}".format(url, unicode(e)))
                last_error = e
                pass
            except socket.error as e:
                logging.getLogger(u"SFGram").error(u"Socket error trying to retrieve {} : {}".format(url, unicode(e)))
                last_error = e
                pass
            # end try
            errors += 1
        # end while

        # Limit
        raise DownloadErrorException(u"Impossible to download {} : {}".format(url, last_error))
    # end download_html

    @staticmethod
    def download_http_file(url, limit=10):
        """
        Download HTTP file
        :param url: Page's URL
        :param limit: Limit of try
        :return: Content
        """
        # Get ext
        ext = os.path.splitext(url.split("/")[-1])[1]

        # Control
        errors = 0
        last_error = None

        # Try
        while errors < limit:
            try:
                logging.debug(u"Downloading HTTP file {}".format(url))
                f = urllib2.urlopen(url)
                return ext, f.read()
            except urllib2.HTTPError as e:
                logging.getLogger(u"SFGram").error(u"HTTP error trying to retrieve {} : {}".format(url, unicode(e)))
                last_error = e
                pass
            except socket.error as e:
                logging.getLogger(u"SFGram").error(u"Socket error trying to retrieve {} : {}".format(url, unicode(e)))
                last_error = e
            # end try
            errors += 1
        # end while

        # Limit
        raise DownloadErrorException(u"Impossible to download HTTP file {}".format(url))
    # end download_http_file

# end Tools
