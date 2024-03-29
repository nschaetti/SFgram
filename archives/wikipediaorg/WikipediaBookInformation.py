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
import re
import time
import requests
from dateutil.parser import parse
from archives.tools.Tools import Tools
import wikipedia


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

        # Get HTML page
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Get infobox table
        infobox_table = soup.find('table', attrs={'class': u"infobox"})

        # For each row
        if infobox_table is not None:
            for row in infobox_table.find_all('tr'):
                field_header = row.find('th')
                if field_header is not None and "colspan" not in field_header.attrs:
                    try:
                        field_name = row.find('th').text.lower().strip().replace(u" ", u"-")
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
        return parse("2038-01-01")
    # end extract_date

    # Check wikipedia page summary
    @staticmethod
    def check_author_summary(summary):
        """
        Check Wikipedia page summary
        :param summary:
        :return:
        """
        summary = summary.lower()

        if u"writer" in summary or u"novelist" in summary:
            return True
        # end if

        return False
    # end check_summary

    # Get author information from URL
    @staticmethod
    def get_author_information_from_url(author_names, url):
        """
        Get author information from URL
        :param author_name:
        :param url:
        :return:
        """
        # Info
        info = {}

        # For each research
        for author_name in author_names:
            # Search for the book on wikipedia
            logging.getLogger(u"SFGram").info(u"Searching Wikipedia page for {}".format(author_name))
            searches = wikipedia.search(author_name)

            try:
                # For each response
                for page_title in searches:
                    try:
                        # Get page
                        try:
                            page = wikipedia.page(page_title)
                        except wikipedia.exceptions.DisambiguationError as e:
                            continue
                        except wikipedia.exceptions.PageError as e:
                            continue
                        # end try

                        # It the page we re looging for
                        if page.url == url:
                            # Get information in the box
                            wiki_info = WikipediaBookInformation.get_infobox(page.html())

                            # Born
                            if "born" in wiki_info:
                                info['born'] = WikipediaBookInformation.extract_date(wiki_info['born'])
                            # end if

                            # Died
                            if "died" in wiki_info:
                                info['died'] = WikipediaBookInformation.extract_date(wiki_info['died'])
                            # end if

                            # Death
                            if "death" in wiki_info:
                                info['died'] = WikipediaBookInformation.extract_date(wiki_info['death'])
                            # end if

                            # Summary
                            info['summary'] = page.summary

                            # Find biography
                            for section in ("Life", "Early life", "Career", "Personal life", "Death", "Biography"):
                                if page.section(section) is not None:
                                    if 'bio' not in info:
                                        info['bio'] = unicode(page.section(section))
                                    else:
                                        info['bio'] += u" " + unicode(page.section(section))
                                    # end if
                                # end if
                            # end for

                            # End
                            logging.getLogger(u"SFGram").info(u"Wikipedia page found at {}".format(page.url))
                            break
                        # end if
                    except wikipedia.exceptions.DisambiguationError:
                        logging.getLogger(u"SFGram").warning(u"Disambiguation error for page {}".format(page_title))
                        pass
                    # end try
                # end for
            except wikipedia.exceptions.PageError:
                logging.getLogger(u"SFGram").error(u"Cannot find Wikipedia page for {}".format(author_name))
            # end try
        # end if

        return info
    # end get_author_information

    # Get author information
    @staticmethod
    def get_author_information(author_name):
        """
        Get author name.
        :param author_name:
        :return:
        """
        # Info
        info = {'wikipedia': {'found': False}}

        # Search for the book on wikipedia
        logging.getLogger(u"SFGram").info(u"Searching Wikipedia page for {}".format(author_name))
        searches = wikipedia.search(author_name)

        try:
            # For each response
            for page_title in searches:
                if "disambiguation" not in page_title:
                    try:
                        # Get page
                        page = wikipedia.page(page_title)

                        if WikipediaBookInformation.check_author_summary(page.summary):
                            # Get information in the box
                            wiki_info = WikipediaBookInformation.get_infobox(page.html())

                            # Born
                            if "born" in wiki_info:
                                info['born'] = WikipediaBookInformation.extract_date(wiki_info['born'])
                            # end if

                            # Died
                            if "died" in wiki_info:
                                info['died'] = WikipediaBookInformation.extract_date(wiki_info['died'])
                            # end if

                            # Death
                            if "death" in wiki_info:
                                info['died'] = WikipediaBookInformation.extract_date(wiki_info['death'])
                            # end if

                            # Summary
                            info['summary'] = page.summary

                            # Find biography
                            for section in ("Life", "Early life", "Career", "Personal life", "Death", "Biography"):
                                if page.section(section) is not None:
                                    if 'bio' not in info:
                                        info['bio'] = unicode(page.section(section))
                                    else:
                                        info['bio'] += u" " + unicode(page.section(section))
                                    # end if
                                # end if
                            # end for

                            # Page
                            info['wikipedia']['url'] = page.url

                            # End
                            info['wikipedia']['found'] = True
                            logging.getLogger(u"SFGram").info(u"Wikipedia page found at {}".format(page.url))
                            break
                        # end if
                    except wikipedia.exceptions.DisambiguationError:
                        logging.getLogger(u"SFGram").warning(u"Disambiguation error for page {}".format(page_title))
                        pass
                    # end try
                # end if
            # end for
        except wikipedia.exceptions.PageError:
            logging.getLogger(u"SFGram").error(u"Cannot find Wikipedia page for {}".format(author_name))
        # end try

        return info
    # end get_author_information

    # Check wikipedia page summary
    @staticmethod
    def check_summary(summary, author):
        """
        Check Wikipedia page summary
        :param summary:
        :return:
        """
        summary = summary.lower()
        author_parts = author.lower().split(u' ')

        if u"novel" in summary or u"book" in summary or u"short story" in summary or u"short-story" in summary or u"novelette" in summary or u"novella" in summary:
            author_found = False
            for author_part in author_parts:
                if author_part in summary:
                    author_found = True
                # end if
            # end for
            return author_found
        # end if

        return False
    # end check_summary

    # Get book information from url
    @staticmethod
    def get_book_information_from_url(title, author, url):
        """
        Get book information from URL
        :param title:
        :param author:
        :param url:
        :return:
        """
        # Info
        info = {}

        # Searches
        searches = [title, title + u" " + author, title + u" novel", title + u" short story"]

        # Try each searches
        for title_search in searches:
            # Search
            search = wikipedia.search(title_search)

            # For each response
            for page_title in searches:
                # Get page
                try:
                    page = wikipedia.page(page_title)
                except wikipedia.exceptions.DisambiguationError as e:
                    continue
                except wikipedia.exceptions.PageError as e:
                    continue
                # end try

                # It is the page
                if page.url == url:
                    # Get information in the box
                    wiki_info = WikipediaBookInformation.get_infobox(page.html())

                    # Original title
                    info['original_title'] = page.original_title

                    # Image
                    info['images'] = WikipediaBookInformation.filter_wikipedia_images(page.images)

                    # Find plot
                    for section in ("Plot", "Plot summary", "Synopsis"):
                        if page.section(section) is not None:
                            info['plot'] = unicode(page.section(section))
                            # end if
                    # end for

                    # Summary
                    info['summary'] = page.summary

                    # Cover artist
                    if u'Cover\u00a0artist' in wiki_info:
                        info['cover_artist'] = wiki_info[u'Cover\u00a0artist']
                    # end if

                    # Publisher
                    if u'Publisher' in wiki_info:
                        info['publisher'] = wiki_info[u'Publisher']
                    # end if

                    # Published in
                    info['published_in'] = wiki_info[u'Published in'] \
                        if u'Published in' in wiki_info else None
                    break
                # end if
            # end for
        # end for

        return info
    # end get_book_information_from_url

    # Get book information
    @staticmethod
    def get_book_information(title, author, page_url=""):
        """
        Get book informations.
        :return:
        """
        # Info
        info = {'wikipedia': {'found': False}}

        # Searches
        searches = [title, title + u" " + author, title + u" novel", title + u" short story"]

        # Try each searches
        for title_search in searches:
            # Search for the book on wikipedia
            logging.getLogger(u"SFGram").info(u"Searching Wikipedia page for {}".format(title_search))

            # try
            try:
                searches = wikipedia.search(title_search)
            except wikipedia.exceptions.WikipediaException:
                logging.getLogger(u"SFGram").warning(u"Can't search on Wikipedia, wait for 10 minutes and retry")
                time.sleep(600)
                searches = wikipedia.search(title_search)
            # end try

            try:
                # For each response
                for page_title in searches:
                    if "disambiguation" not in page_title:
                        #print(page_title)
                        try:
                            count = 0
                            success = False
                            reference_problem = False
                            while count < 10:
                                # Get page
                                try:
                                    page = wikipedia.page(page_title)
                                    success = True
                                    break
                                except wikipedia.exceptions.WikipediaException as e:
                                    reference_problem = True
                                    success = True
                                    break
                                    pass
                                except requests.exceptions.SSLError as e:
                                    logging.getLogger(u"SFGram").warning(
                                        u"SSL exception {}, wait for 10 minutes and retry".format(e))
                                    time.sleep(600)
                                    count += 1
                                    pass
                                except requests.exceptions.ConnectionError as e:
                                    logging.getLogger(u"SFGram").warning(
                                        u"Connection exception {}, wait for 10 minutes and retry".format(e))
                                    time.sleep(600)
                                    count += 1
                                    pass
                                # end try
                            # end while

                            # CHeck
                            if not success:
                                logging.getLogger(u"SFGram").warning(
                                    u"Impossible to get Wikipedia page {}".format(page_title))
                            # end if

                            # Check page is ok
                            if success and not reference_problem and WikipediaBookInformation.check_summary(page.summary, author):
                                # Get information in the box
                                wiki_info = WikipediaBookInformation.get_infobox(page.html())

                                # Try to get the published date
                                if u"published" in wiki_info or u"published-in" in wiki_info or u"publication-date" in wiki_info:
                                    # Country
                                    if 'country' in wiki_info:
                                        info['country'] = wiki_info['country']
                                    # end if

                                    # Original title
                                    info['original_title'] = page.original_title

                                    # Image
                                    info['images'] = list()
                                    try:
                                        img_urls = WikipediaBookInformation.filter_wikipedia_images(page.images)
                                        for url in img_urls:
                                            info['images'].append(Tools.download_http_file(url))
                                        # end for
                                    except KeyError:
                                        pass
                                    # end try

                                    # Find plot
                                    for section in ("Plot", "Plot summary", "Synopsis"):
                                        if page.section(section) is not None:
                                            info['plot'] = unicode(page.section(section))
                                        # end if
                                    # end for

                                    # Summary
                                    info['summary'] = page.summary
                                    info['wikipedia']['url'] = page.url

                                    # Cover artist
                                    if u'Cover\u00a0artist' in wiki_info:
                                        info['cover_artist'] = wiki_info[u'Cover\u00a0artist']
                                    # end if

                                    # Publication date
                                    publication_date = WikipediaBookInformation.extract_publication_date(wiki_info)

                                    # If found
                                    if publication_date != -1:
                                        info['wikipedia']['year'] = WikipediaBookInformation.extract_publication_date(wiki_info)
                                    else:
                                        info['wikipedia']['year'] = -1
                                    # end if

                                    # Publisher
                                    if u'Publisher' in wiki_info:
                                        info['publisher'] = wiki_info[u'Publisher']
                                    # end if

                                    # Published in
                                    info['published_in'] = wiki_info[u'Published in']\
                                        if u'Published in' in wiki_info else None

                                    # Found
                                    info['wikipedia']['found'] = True
                                    logging.getLogger(u"SFGram").info(u"Wikipedia page found at {}".format(page.url))
                                    break
                                # end if
                            # end if
                        except wikipedia.exceptions.DisambiguationError:
                            logging.getLogger(u"SFGram").warning(u"Disambiguation error for page {}".format(page_title))
                            pass
                        # end try
                    # end if
                # end for
            except wikipedia.exceptions.PageError as e:
                logging.getLogger(u"SFGram").error(u"Cannot find Wikipedia page for {} : {}".format(title, e))
            # end try

            # Found?
            if info['wikipedia']['found']:
                break
            # end if
        # end for

        # Not found
        if not info['wikipedia']['found']:
            logging.getLogger(u"SFGram").error(u"Cannot find Wikipedia page for {}".format(title))
        # end if

        return info
    # end get_book_information

# end
