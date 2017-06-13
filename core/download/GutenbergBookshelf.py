
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
from .Book import Book


# Class to list a Gutenberg category
class GutenbergBookshelf(object):

    # Constructor
    def __init__(self):
        """
        Constructor
        :param num:
        """
        self._url = "http://www.gutenberg.org/ebooks/bookshelf/"
        self._start_index = -24
        self._end_index = 0
        self._step = 25
        self._current = 0
        self._books = list()
    # end __init__

    # Open the category for listing
    def open(self, num):
        # Final URL
        self._url += str(num)

        # Load elements
        self._load()
    # end open

    # Next element
    def next(self):
        self._current += 1
        if self._current >= self._end_index:
            self._load()
        # end if
        if self._current-1 < self._end_index:
            return Book(self._books[self._current-1])
        else:
            raise StopIteration()
        # end if
    # end next

    # Iterator
    def __iter__(self):
        return self
    # end __iter__

    # Load elements
    def _load(self):

        # Load HTML
        try:
            html = urlopen(self._url + "?start_index=" + str(self._start_index + self._step)).read()
        except urllib2.URLError:
            return
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
        self._end_index += self._step
    # end _load

    # Parse bookl link
    def _parse_book_link(self, book_link):
        """
        Parse book link
        :param book_link:
        :return:
        """
        book_url = book_link.find('a').attrs['href']
        return int(book_url[book_url.rfind("/")+1:])
    # end _parse_book_link

# end GutenbergBookshelf
