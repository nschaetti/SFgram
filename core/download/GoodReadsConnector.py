
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
from dateutil.parser import parse


# Connector for GoodReads
class GoodReadsConnector(object):

    # Constructor
    def __init__(self):
        self._base_url = "https://www.goodreads.com"
        self._search_url = "https://www.goodreads.com/search?utf8=%E2%9C%93&q={}%20-cd&search_type=books"
    # end __init__

    # Search for a book
    def search_book(self, title):
        """
        Search for a book
        :param title:
        :return:
        """
        # Load HTML
        print(self._search_url.format(title.replace(" ", "+")))
        html = urlopen(self._search_url.format(title.replace(" ", "+"))).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")
        print(soup.find('a', attrs={'class': u"bookTitle"}))
        # Find book title link
        book_link = soup.find('a', attrs={'class': u"bookTitle"}).attrs["href"]

        return self._base_url + book_link
    # end search_book

    # Get book's information
    def get_book_information(self, book_link):
        """
        Get book's information
        :param book_link:
        :return:
        """
        print(book_link)
        # Load HTML
        html = urlopen(book_link).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # First published
        return soup.find("nobr", attrs={'class': u"greyText"}).text
    # end get_book_information

# end GoodReadsConnector
