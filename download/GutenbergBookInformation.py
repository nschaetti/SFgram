# -*- coding: utf-8 -*-
#

# Import
import re
import urllib2
from urllib2 import urlopen
import logging
import bs4 as BeautifulSoup
from dateutil.parser import parse


# Access to Gutenberg book information
class GutenbergBookInformation(object):
    """
    Access to Gutenberg book information.
    """

    # Get book information
    @staticmethod
    def get_book_info(num):
        """
        Load Gutenberg book information
        :return:
        """
        # URL
        ebooks_url = u"http://www.gutenberg.org/ebooks/" + unicode(num)
        files_url = u"http://www.gutenberg.org/files/{}/"

        # Result
        info = dict()

        # Control variable
        success = False
        errors = 0
        html = ""

        # Try until done
        while not success:
            try:
                html = urlopen(ebooks_url).read()
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(ebooks_url, unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {}".format(ebooks_url))
                exit()
            # end if
        # end while

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find title and author
        title_author = soup.find('h1', attrs={'itemprop': u"name"}).text.split(" by ")
        info['#'] = num
        info['Title'] = title_author[0].strip()

        # Authors
        if len(title_author) > 1:
            info['Authors'] = GutenbergBookInformation.parse_authors(title_author[1].strip())
        else:
            info['Authors'] = list()
            for author_link in soup.find_all('a', attrs={'itemprop': u"creator"}):
                info['Authors'].append(re.search(r"([a-zA-Z\,\s]*)", author_link.text).groups()[0].strip())
            # end for
        # end if

        # Language
        info['Language'] = soup.find('tr', attrs={'itemprop': u"inLanguage"}).find('td').text.strip()

        # LoC class
        try:
            info['LoC Class'] = soup.find('tr', attrs={'datatype': u"dcterms:LCC"}).find('td').find(
                'a').text.strip()
        except AttributeError:
            info['LoC Class'] = ""
        # end try

        # Empty list of genres
        info['Genres'] = list()

        # Filter and add subject
        for subject in soup.find_all('td', attrs={'datatype': u"dcterms:LCSH"}):
            filtered_subject = GutenbergBookInformation.filter_subjects(subject.find('a').text.strip().split(" -- ")[0])
            if filtered_subject is not None:
                info['Genres'].append(filtered_subject.title())
            # end if
        # end for

        # Category
        info['Category'] = soup.find('td', attrs={'property': u"dcterms:type"}).text.strip()

        # Release date
        info['Release Date'] = parse(
            soup.find('td', attrs={'itemprop': u"datePublished"}).text.strip()).isoformat()

        # Copyright
        info['Copyright'] = soup.find('td', attrs={'property': u"dcterms:rights"}).text.strip()

        # Images
        info['Images'] = GutenbergBookInformation.explore_http_directory(files_url.format(num))

        # Cover art
        img_cover_art = soup.find('img', attrs={'class': u"cover-art"})
        if img_cover_art is not None:
            # Get URL
            cover_art_url = img_cover_art.attrs['src']

            # Add http:
            if cover_art_url[:5] != "http:":
                cover_art_url = "http:" + cover_art_url
            # end if

            # Save
            info['Cover-art'] = cover_art_url
        # end if

        return info
    # end get_book_info

    # Parse authors
    @staticmethod
    def parse_authors(author_text):
        """
        Parse authors' name.
        :param author_text: Text to parse.
        :return: Parsed author names.
        """
        return author_text.split(" and ")
    # end _parse_authors

    # Filter subjets
    @staticmethod
    def filter_subjects(subject):
        """
        Filter subjects
        :param subject:
        :return:
        """
        filter = ["Science fiction", "Fiction"]
        if subject not in filter:
            return subject
        # end if
        return None
    # end _filter_subjects

    ##########################################
    # Private
    ##########################################

    # Explore HTTP directory
    @staticmethod
    def explore_http_directory(http_directory):
        """
        Explore HTTP directory
        :param http_directory:
        :return:
        """
        # Images URL
        files_url = u"http://www.gutenberg.org/files/{}/"

        # Results
        result = list()

        # Control
        success = False
        count = 0

        # Load HTML
        while not success:
            try:
                html = urlopen(http_directory).read()
                success = True
            except urllib2.HTTPError as e:
                if e.code == 404 or e.code == 403:
                    return result
                # end if
                pass
            # end try

            # Count
            count += 1

            # Max
            if count >= 10:
                return result
            # end if
        # end while

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # For each file entry
        for file_entry in soup.find_all('tr'):
            try:
                file_type = file_entry.find('td', attrs={'valign': 'top'}).find('img')['alt']
                file_link = file_entry.find('a')['href']
                if file_type == "[DIR]":
                    images = GutenbergBookInformation.explore_http_directory(http_directory + file_link)
                    for im in images:
                        result.append(im)
                        # end for
                elif file_type == "[IMG]":
                    result.append(http_directory + file_link)
                    # end if
            except AttributeError:
                pass
                # end try
        # end for

        return result
    # end _explore_http_directory

# end GutenbergBookInformation
