# -*- coding: utf-8 -*-
#

import logging
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
from GutenbergBookInformation import GutenbergBookInformation
from GoodReadsConnector import GoodReadsConnector
from WikipediaBookInformation import WikipediaBookInformation
from db.Book import Book


# Class to list a Gutenberg category
class GutenbergBookshelf(object):
    """
    Tool class to list a Gutenberg bookshelf.
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self._url = u"http://www.gutenberg.org/ebooks/bookshelf/"
        self._start_index = 1
        self._step = 25
        self._books = list()
    # end __init__

    # Open the category for listing
    def open(self, num):
        """
        Open a category for listing
        :param num: The category number.
        """
        # Final URL
        self._url += str(num)
    # end open

    # Next element
    def next(self):
        """
        Next element
        """
        # If book list is empty, we reload
        if len(self._books) == 0:
            self._load()
        # end if

        # Current book
        book_url = self._books[0]

        # Gutenberg information
        gutenberg_info = GutenbergBookInformation.get_book_info(book_url)

        # Wikipedia information
        wikipedia_info = WikipediaBookInformation.get_book_information(gutenberg_info['Title'],
                                                                       gutenberg_info['Authors'][0])

        # Goodreads information
        goodreads_info = GoodReadsConnector.get_book_info(gutenberg_info['Title'])

        # New book
        new_book = Book()

        #
        # Gutenberg information
        #
        new_book.num = gutenberg_info['#']
        new_book.title = gutenberg_info['Title']
        new_book.category = gutenberg_info['Category']
        new_book.copyright = gutenberg_info['Copyright']
        new_book.language = gutenberg_info['Language']
        new_book.loc_class = gutenberg_info['LoC Class']
        new_book.release_date = gutenberg_info['Release Date']

        #
        # Goodreads informations
        #
        if goodreads_info['goodreads_found']:
            # General
            new_book.average_rating = goodreads_info['Average Rating']
            new_book.cover_artist = wikipedia_info['Cover artist']
            new_book.description = goodreads_info['Description']
            new_book.format = goodreads_info['Format']
            new_book.pages = goodreads_info['Pages']
            new_book.rating_count = goodreads_info['Rating Count']

            # Goodreads publication date
            if 'Publication date' in goodreads_info:
                new_book.goodreads_publication_date = goodreads_info['Publication date']
            # end if

            # Goodreads URL
            new_book.goodreads_url = goodreads_info['Goodreads URL']
            new_book.goodreads_found = goodreads_info['goodreads_found']

            # Information
            new_book.ISBN = goodreads_info['ISBN']
            new_book.ISBN13 = goodreads_info['ISBN13']
            new_book.language_code = goodreads_info['Language Code']
            new_book.similar_books = goodreads_info['Similar Books']
        # end if

        #
        # Wikipedia information
        #
        if wikipedia_info['wikipedia_found']:
            # Original Title
            if 'Original Title' in wikipedia_info:
                new_book.original_title = wikipedia_info['Original Title']
            # end if

            # Wikipedia information
            new_book.wikipedia_publication_date = wikipedia_info['Publication date']
            new_book.wikipedia_url = wikipedia_info['wikipedia_url']
            new_book.wikipedia_found = wikipedia_info['wikipedia_found']
        # end if

        # Publication date
        if 'Publication date' in wikipedia_info:
            new_book.publication_date = wikipedia_info['Publication date']
        elif 'Publication date' in goodreads_info:
            new_book.publication_date = goodreads_info['Publication date']
        # end if

        # Save
        logging.info(u"Saving book {} ({}), {} in database".format(new_book.title, new_book.publication_date,
                                                                   new_book.author))
        new_book.save()

        # Remove from the list
        self._books.remove(book_url)

        return book_url
    # end next

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return: object.
        """
        return self
    # end __iter__

    # Load elements
    def _load(self):
        """
        Load the elements of the current page.
        """
        # Load HTML
        try:
            logging.debug(u"Downloading page " + self._url + u"?start_index=" + unicode(self._start_index))
            html = urlopen(self._url + u"?start_index=" + unicode(self._start_index)).read()
        except urllib2.URLError:
            raise StopIteration
        # end try

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find all 'booklink'
        book_links = soup.find_all('li', attrs={"class": u"booklink"})

        # For all book link
        for book_link in book_links:
            self._books.append(self._parse_book_link(book_link))
        # end for

        # Next page
        self._start_index += self._step
    # end _load

    # Parse bookl link
    def _parse_book_link(self, book_link):
        """
        Parse book link and return book number.
        :param book_link: The Gutenberg URL of the book.
        :return: Book number.
        """
        book_url = book_link.find('a').attrs['href']
        return int(book_url[book_url.rfind("/")+1:])
    # end _parse_book_link

# end GutenbergBookshelf
