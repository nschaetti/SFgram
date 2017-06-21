# -*- coding: utf-8 -*-
#

# Import
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
        info['Authors'] = GutenbergBookInformation.parse_authors(title_author[1].strip())

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

# end GutenbergBookInformation
