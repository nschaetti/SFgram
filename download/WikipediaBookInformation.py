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
import wikipedia
import re
from dateutil.parser import parse


# Connector for Wikipedia
class WikipediaBookInformation(object):

    # Get Wikipedia info box
    @staticmethod
    def get_infobox(html):
        """
        Get Wikipedia info box
        :param html:
        :return:
        """
        # Result
        result = dict()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Get infobox table
        infobox_table = soup.find('table', attrs={'class': u"infobox"})

        # For each row
        if infobox_table is not None:
            for row in infobox_table.find_all('tr'):
                field_header = row.find('th')
                if field_header is not None and "colspan" not in field_header.attrs:
                    try:
                        field_name = row.find('th').text.strip()
                        field_value = row.find('td').text.strip()
                        result[field_name] = field_value
                    except AttributeError:
                        pass
                    # end try
                # end if
            # end for
        # end if
        return result
    # end _get_wikipedia_infobox

    # Filter Wikipedia images
    @staticmethod
    def filter_wikipedia_images(images):
        """
        Filter Wikipedia images
        :param images:
        :return:
        """
        result = list()
        for im in images:
            if "logo" not in im and ".svg" not in im:
                result.append(im)
            # end if
        # end for
        return result
    # end _filter_wikipedia_images

    # Extract publication date
    @staticmethod
    def extract_publication_date(wiki_info):
        """
        Extract publication date
        :param wiki_info:
        :return:
        """
        try:
            # Publication date
            if "Publication date" in wiki_info:
                year = re.search(r"([12][0-9]{3})", wiki_info['Publication date']).groups()[0]
                return int(year)
            elif "Published" in wiki_info:
                year = re.search(r"([12][0-9]{3})", wiki_info['Published']).groups()[0]
                return int(year)
            else:
                return -1
            # end if
        except AttributeError:
            return -1
            pass
        # end try
    # end extract_publication_date

    # Extract date
    @staticmethod
    def extract_date(date_string):
        """
        Extract date
        :param date_string:
        :return:
        """
        for regex in [r"([12][0-9]{3}\-[0-9]{2}\-[0-9]{2})", r"([12][0-9]{3})"]:
            try:
                date_found = re.search(regex, date_string).groups()[0]
                return parse(date_found)
            except AttributeError:
                pass
            # end try
        # end for
        return parse(0000-00-00)
    # end extract_date

    # Get author information
    @staticmethod
    def get_author_information(author_name):
        """
        Get author name.
        :param author_name:
        :return:
        """
        # Info
        info = {'wikipedia_found': False, 'Ambiguation': False}

        # Search for the book on wikipedia
        logging.debug(u"Searching Wikipedia page for {}".format(author_name))
        searches = wikipedia.search(author_name)

        try:
            # For each response
            for page_title in searches:
                if "disambiguation" not in page_title:
                    try:
                        # Get page
                        page = wikipedia.page(page_title)

                        # Get information in the box
                        wiki_info = WikipediaBookInformation.get_infobox(page.html())

                        # Born
                        if "Born" in wiki_info:
                            info['Born'] = WikipediaBookInformation.extract_date(wiki_info['Born'])
                        # end if

                        # Died
                        if "Died" in wiki_info:
                            info['Died'] = WikipediaBookInformation.extract_date(wiki_info['Died'])
                        # end if

                        # Death
                        if "Death" in wiki_info:
                            info['Died'] = WikipediaBookInformation.extract_date(wiki_info['Death'])
                        # end if

                        # Summary
                        info['Summary'] = page.summary

                        # Find biography
                        for section in ("Life", "Early life", "Career", "Personal life", "Death", "Biography"):
                            if page.section(section) is not None:
                                if 'Bio' not in info:
                                    info['Bio'] = unicode(page.section(section))
                                else:
                                    info['Bio'] += u" " + unicode(page.section(section))
                                # end if
                            # end if
                        # end for

                        # Page
                        info['URL'] = page.url

                        # End
                        info['wikipedia_found'] = True
                        break
                    except wikipedia.exceptions.DisambiguationError:
                        info['Ambiguation'] = True
                        logging.warning(u"Disambiguation error for page {}".format(page_title))
                        pass
                    # end try
                # end if
            # end for
        except wikipedia.exceptions.PageError:
            logging.error(u"Cannot find Wikipedia page for {}".format(title))
        # end try

        return info
    # end get_author_information

    # Get book information
    @staticmethod
    def get_book_information(title, author):
        """
        Get book informations.
        :return:
        """
        # Info
        info = {'wikipedia_found': False, 'Ambiguation': False}

        # Search for the book on wikipedia
        logging.debug(u"Searching Wikipedia page for {}".format(title + u" " + author))
        searches = wikipedia.search(title)

        try:
            # For each response
            for page_title in searches:
                if "disambiguation" not in page_title:
                    try:
                        # Get page
                        page = wikipedia.page(page_title)

                        # Get information in the box
                        wiki_info = WikipediaBookInformation.get_infobox(page.html())

                        # Try to get the published date
                        if u"Published" in wiki_info or u"Published in" in wiki_info or u"Publication date" in wiki_info:

                            # Country
                            if 'Country' in wiki_info:
                                info['Country'] = wiki_info['Country']
                            # end if

                            # Original title
                            info['Original Title'] = page.original_title

                            # Image
                            try:
                                info['Images'] = WikipediaBookInformation.filter_wikipedia_images(page.images)
                            except KeyError:
                                info['Images'] = []
                                pass
                            # end try

                            # Find plot
                            for section in ("Plot", "Plot summary", "Synopsis"):
                                if page.section(section) is not None:
                                    info['Plot'] = unicode(page.section(section))
                                # end if
                            # end for

                            # Summary
                            info['Summary'] = page.summary
                            info['wikipedia_url'] = page.url

                            # Cover artist
                            if u'Cover\u00a0artist' in wiki_info:
                                info['Cover artist'] = wiki_info[u'Cover\u00a0artist']
                            # end if

                            # Publication date
                            publication_date = WikipediaBookInformation.extract_publication_date(wiki_info)

                            # If found
                            if publication_date != -1:
                                info['Publication date'] = WikipediaBookInformation.extract_publication_date(wiki_info)
                            # end if

                            # Publisher
                            if u'Publisher' in wiki_info:
                                info['Publisher'] = wiki_info[u'Publisher']
                            # end if

                            # Published in
                            info['Published in'] = wiki_info[u'Published in']\
                                if u'Published in' in wiki_info else None

                            # End
                            info['wikipedia_found'] = True
                            break
                        # end if
                    except wikipedia.exceptions.DisambiguationError:
                        info['Ambiguation'] = True
                        logging.warning(u"Disambiguation error for page {}".format(page_title))
                        pass
                    # end try
                # end if
            # end for
        except wikipedia.exceptions.PageError:
            logging.error(u"Cannot find Wikipedia page for {}".format(title))
        # end try

        return info
    # end get_book_information

# end
