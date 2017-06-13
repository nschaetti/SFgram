
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
        html = urlopen(self._search_url.format(title.replace(" ", "+"))).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

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
        # Fields
        result = dict()

        # Load HTML
        html = urlopen(book_link).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # URL
        result['url'] = book_link

        # Book title
        result['Title'] = soup.find("h1", attrs={'id': u"bookTitle"}).text.strip()

        # Author
        result['Author'] = soup.find("a", attrs={'class': u"authorName"})\
            .find("span", attrs={'itemprop': u"name"}).text.strip()

        # Cover image
        cover_image = soup.find("img", attrs={'id': u"coverImage"})
        if cover_image is not None:
            result['Cover'] = cover_image['src']
        # end if

        # Description
        description_div = soup.find("div", attrs={'id': u"description"})
        if description_div is not None:
            result['Description'] = description_div.text.strip()
        # end if

        # First published
        grey_text_nobr = soup.find("nobr", attrs={'class': u"greyText"})
        if grey_text_nobr is not None:
            result['First published'] = grey_text_nobr.text.strip()
        # end if

        # DataBox fields
        databox_info = self._get_databox_information(soup)
        for field in databox_info:
            result[field] = databox_info[field]
        # end for

        # Genres
        result['Genres'] = self._get_genres(soup)

        return result
    # end get_book_information

    # Get genres
    def _get_genres(self, soup):
        """
        Get genres
        :param soup:
        :return:
        """
        result = list()

        # Filters
        filters = ["Science Fiction", "Fiction", "Literature", "Audiobook"]

        # Right container
        right_container = soup.find('div', attrs={'class': u"rightContainer"})
        for page_genre_link in right_container.find_all('a', attrs={'class': u"bookPageGenreLink"}):
            if 'greyText' not in page_genre_link['class']:
                element_name = page_genre_link.text.strip()
                if element_name not in filters:
                    result.append(element_name)
                # end if
            # end if
        # end for
        return result
    # end _get_genres

    # Get DataBox information
    def _get_databox_information(self, soup):
        result = dict()

        # Data box
        databox_div = soup.find('div', attrs={'id': u"bookDataBox"})

        # Foreach clearFloats
        for entry in databox_div.find_all('div', attrs={'class': u"clearFloats"}):
            field_name = entry.find('div', attrs={'infoBoxRowTitle'}).text.strip()
            field_value = entry.find('div', attrs={'infoBoxRowItem'}).text.strip()
            result[field_name] = field_value
        # end for
        return result
    # end _get_databox_information

# end GoodReadsConnector
