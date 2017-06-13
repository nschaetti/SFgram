
import urllib2
from urllib2 import urlopen
import bs4 as BeautifulSoup
from dateutil.parser import parse
import wikipedia
import re
import json
from .GoodReadsConnector import GoodReadsConnector


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
        self._attrs = dict()

        # Load info
        self._load_gutenberg_information()
        self._load_wikipedia_information()
        self._load_goodreads_information()
    # end __init__

    ###################################################
    #
    # PUBLIC
    #
    ###################################################

    # Get book's title
    def get_title(self):
        """
        Get book's title
        :return:
        """
        return self._attrs["Title"]
    # end get_title

    # Get book's author
    def get_author(self):
        """
        Get book's author
        :return:
        """
        return self._attrs["Authors"]
    # end get_author

    # Get book's attributes
    def get_attrs(self):
        """
        Get book's attributes
        :return: Book's attributes
        """
        return self._attrs
    # end get_attrs

    ###################################################
    #
    # PRIVATE
    #
    ###################################################

    # Get Wikipedia info box
    def _get_wikipedia_infobox(self, html):
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
                    field_name = row.find('th').text.strip()
                    field_value = row.find('td').text.strip()
                    result[field_name] = field_value
                # end if
            # end for
        # end if
        return result
    # end _get_wikipedia_infobox

    # Load GoodReads information
    def _load_goodreads_information(self):
        """
        Get GoodReads information
        """

        # GoodReads connector
        goodreads_con = GoodReadsConnector()

        # Get information
        gr_info = goodreads_con.get_book_information(goodreads_con.search_book(self._attrs["Title"] + " " +
                                                                               self._attrs["Authors"][0]))

        # Fields
        self._attrs['Genres'] = gr_info['Genres']
        if "ISBN" in gr_info:
            try:
                self._attrs['ISBN'] = re.search(r"(\d{13})", gr_info['ISBN']).groups()[0]
            except AttributeError:
                self._attrs['ISBN'] = re.search(r"(\d{10})", gr_info['ISBN']).groups()[0]
            # end try
        # end if
        if "ASIN" in gr_info:
            self._attrs['ASIN'] = re.search(r"([A-Z0-9]{10})", gr_info['ASIN']).groups()[0]
        self._attrs['GoodReads URL'] = gr_info['url']
        if "Cover" in gr_info:
            self._attrs['Cover'] = gr_info['Cover']
        # end if
    # end _load_goodreads_information

    # Add field
    def _add_attr_field(self, dic, field_name, final_name):
        """
        Add field
        :param dic:
        :param field_name:
        :return:
        """
        if field_name in dic.keys():
            self._attrs[final_name] = dic[field_name]
        # end if
    # end _add_attr_field

    # Filter Wikipedia images
    def _filter_wikipedia_images(self, images):
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
    def _extract_publication_date(self, wiki_info):
        """
        Extract publication date
        :param wiki_info:
        :return:
        """
        # Published
        if "Published" in wiki_info:
            year = re.search(r"([12][0-9]{3})", wiki_info['Published']).groups()[0]
            self._attrs['Publication date'] = int(year)
        # end if
        # Publication date
        if "Publication date" in wiki_info:
            year = re.search(r"([12][0-9]{3})", wiki_info['Publication date']).groups()[0]
            self._attrs['Publication date'] = int(year)
        # end if
    # end _extract_publication_date

    # Load information from wikipedia
    def _load_wikipedia_information(self):
        """
        Load information from Wikipedia
        """
        # Search for the book on wikipedia
        searches = wikipedia.search(self._attrs['Title'] + " " + self._attrs['Authors'][0])

        # For each response
        for page_title in searches:
            if "disambiguation" not in page_title:
                try:
                    page = wikipedia.page(page_title)
                    wiki_info = self._get_wikipedia_infobox(page.html())
                    if u"Published" in wiki_info or u"Published in" in wiki_info or u"Publication date" in wiki_info:
                        self._add_attr_field(wiki_info, 'Country', 'Country')
                        self._attrs['Original title'] = page.original_title
                        try:
                            self._attrs['Images'] = self._filter_wikipedia_images(page.images)
                        except KeyError:
                            pass
                        self._attrs['Summary'] = page.summary
                        self._attrs['Wikipedia URL'] = page.url
                        self._add_attr_field(wiki_info, u'Cover\u00a0artist', 'Cover artist')
                        self._extract_publication_date(wiki_info)
                        self._add_attr_field(wiki_info, u'Publisher', 'Publisher')
                        self._add_attr_field(wiki_info, u'Published in', 'Published in')
                        return
                    # end if
                except wikipedia.exceptions.DisambiguationError:
                    pass
                # end try
            # end if
        # end for
    # end _load_wikipedia_info

    # Load Gutenberg informations
    def _load_gutenberg_information(self):
        """
        Load Gutenberg informations
        :return:
        """
        # Load HTML
        html = urlopen(self._ebooks_url + str(self._num)).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find title and author
        title_author = soup.find('h1', attrs={'itemprop': u"name"}).text.split(" by ")
        self._attrs['Title'] = title_author[0].strip()
        self._attrs['Authors'] = self._parse_authors(title_author[1].strip())

        # Language
        self._attrs['Language'] = soup.find('tr', attrs={'itemprop': u"inLanguage"}).find('td').text.strip()

        # LoC class
        try:
            self._attrs['LoC Class'] = soup.find('tr', attrs={'datatype': u"dcterms:LCC"}).find('td').find('a').text.strip()
        except AttributeError:
            self._attrs['LoC Class'] = ""
        # end try

        # Subject
        self._attrs['Subjects'] = list()
        for subject in soup.find_all('td', attrs={'datatype': u"dcterms:LCSH"}):
            self._attrs['Subjects'].append(subject.find('a').text.strip().split(" -- ")[0])
        # end for

        # Category
        self._attrs['Category'] = soup.find('td', attrs={'property': u"dcterms:type"}).text.strip()

        # Release date
        self._attrs['Release Date'] = parse(soup.find('td', attrs={'itemprop': u"datePublished"}).text.strip()).isoformat()

        # Copyright
        self._attrs['Copyright'] = soup.find('td', attrs={'property': u"dcterms:rights"}).text.strip()
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
        return json.dumps(self._attrs)
    # end __str__

# end Book
