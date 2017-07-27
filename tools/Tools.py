# -*- coding: utf-8 -*-
#

# Import
import os
import urllib2
import logging


# Download error
class DownloadErrorException(Exception):
    """
    Download error exception
    """
    pass
# end DownloadErrorException


# Toolbox
class Tools(object):

    @staticmethod
    def download_http_file(url):
        """
        Download HTTP file
        :param url:
        :return:
        """
        # Get ext
        ext = os.path.splitext(url.split("/")[-1])[1]

        # Control
        success = False
        count = 0

        # Try
        while not success:
            try:
                logging.debug(u"Downloading HTTP file {}".format(url))
                f = urllib2.urlopen(url)
                success = True
            except urllib2.URLError:
                pass
            # end try

            # Count
            count += 1

            # Limit
            if count >= 10:
                logging.fatal(u"Impossible to download {}".format(url))
                raise DownloadErrorException(u"Impossible to download {}".format(url))
                # end if
        # end while

        return ext, f.read()
    # end download_http_file

# end Tools
