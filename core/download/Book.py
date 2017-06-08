
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
from dateutil.parser import parse


# A book
class Book(object):

    # Constructor
    def __init__(self, num):
        """
        Constructor
        :param num:
        """
        self._ebooks_url = "http://www.gutenberg.org/ebooks/"
        self._num = num
        self._title = ""
        self._authors = ""
        self._language = ""
        self._loc_class = ""
        self._subjects = list()
        self._category = ""
        self._release_date = ""
        self._copyright = ""

        # Load info
        self._load_gutenberg_informations()
    # end __init__

    # Get book's title
    def get_title(self):
        """
        Get book's title
        :return:
        """
        return self._title
    # end get_title

    # Load Gutenberg informations
    def _load_gutenberg_informations(self):
        # Load HTML
        html = urlopen(self._ebooks_url + str(self._num)).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find title and author
        title_author = soup.find('h1', attrs={'itemprop': u"name"}).text.split(" by ")
        self._title = title_author[0].strip()
        self._authors = self._parse_authors(title_author[1].strip())

        # Language
        self._language = soup.find('tr', attrs={'itemprop': u"inLanguage"}).find('td').text.strip()

        # LoC class
        self._loc_class = soup.find('tr', attrs={'datatype': u"dcterms:LCC"}).find('td').find('a').text.strip()

        # Subject
        #self._subject = soup.find('td', attrs={'datatype': u"dcterms:LCSH"}).find('td').find('a').text
        for subject in soup.find_all('td', attrs={'datatype': u"dcterms:LCSH"}):
            self._subjects.append(subject.find('a').text.strip())
        # end for

        # Category
        self._category = soup.find('td', attrs={'property': u"dcterms:type"}).text.strip()

        # Release date
        self._release_date = parse(soup.find('td', attrs={'itemprop': u"datePublished"}).text.strip())

        # Copyright
        self._copyright = soup.find('td', attrs={'property': u"dcterms:rights"}).text.strip()
    # end _load_gutenberg_informations

    # Parse authors
    def _parse_authors(self, author_text):
        """
        Parse authors
        :param author_text:
        :return:
        """
        return author_text.split(" and ")
    # end _parse_authors

    # To string
    def __str__(self):
        return str({'title': self._title, 'authors': self._authors, "language": self._language,
                    "LoC Class": self._loc_class, "subjects": self._subjects, "category": self._category,
                    "release_date": self._release_date, "copyright": self._copyright})
    # end __str__

# end Book
