# -*- coding: utf-8 -*-
#

import bs4 as BeautifulSoup
import codecs
import json
import logging
import os
import re
import time
import urllib2
from dateutil.parser import parse
from urllib2 import urlopen

import requests
import wikipedia

import goodreads
from cleaning.TextCleaner import TextCleaner
from goodreads import client


# A book
class Book(object):

    # Constructor
    def __init__(self, num):
        """
        Constructor
        :param num:
        """
        self._ebooks_url = u"http://www.gutenberg.org/ebooks/"
        self._plaintext_url = u"http://www.gutenberg.org/ebooks/{}.txt.utf-8"
        self._files_url = u"http://www.gutenberg.org/files/{}/"
        self._num = num
        self._attrs = self._get_default_values()
        self._attrs['Genres'] = list()
        self._goodreads_client = client.GoodreadsClient("3H4jhs695dsDscTWMjKmw",
                                                        "IGxF8r6Gg4FWPCQlPBpwkmQU2nZJWa6ZXCDRW7FtT5c")

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

    # Get book's number
    def get_num(self):
        return self._num
    # end get_num

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

    # Get book's attribute
    def get_attr(self, key):
        return self._attrs[key]
    # end get_attr

    # Save book information
    def save(self, dataset_directory):
        """
        Save book information
        :param dataset_directory:
        :return:
        """

        # Create the directory
        target_directory = os.path.join(dataset_directory, u"books", unicode(self._num))
        try:
            if not os.path.exists(os.path.join(dataset_directory, u"books")):
                os.mkdir(os.path.join(dataset_directory, u"books"))
            # end if
            os.mkdir(target_directory)
        except OSError as e:
            logging.getLogger(name="SFGram").warning(u"Error while creating directory %s : %s" % (target_directory, unicode(e)))
            pass
        # end try

        # Download the file
        logging.getLogger(name="SFGram")\
            .debug(u"Download plaintext file to %s" % os.path.join(target_directory, u"content.txt"))
        self.download(os.path.join(target_directory, u"content.txt"))

        # Save JSON info file
        logging.getLogger(name="SFGram").debug(u"Saving JSON file to %s" % os.path.join(target_directory, u"info.json"))
        with open(os.path.join(target_directory, u"info.json"), 'w') as f:
            json.dump(self._attrs, f, sort_keys=True, indent=4)
        # end with

        # Create directory and download images
        image_directory = os.path.join(target_directory, u"images")
        try:
            os.mkdir(image_directory)
        except OSError:
            pass
        # end try
        self.download_images(image_directory)
    # end save

    # Book downloaded
    def downloaded(self, dataset_directory):
        """
        Is book downloaded?
        :param dataset_path: Dataset path
        :return: True or False
        """
        # Book directory
        target_directory = os.path.join(dataset_directory, u"books", unicode(self._num), u"content.txt")
        return os.path.exists(target_directory)
    # end downloaded

    # Download the file
    def download(self, content_file):
        """
        Download the file
        :param content_file:
        :return:
        """
        # Load URL
        try:
            # Open URL
            text = urlopen(self._plaintext_url.format(self._num)).read().decode("utf-8", errors='ignore')

            #  Clean text
            cleaner = TextCleaner()
            cleaned_text, cleaned = cleaner(text)
            self._attrs['Cleaned'] = cleaned

            # Save to file
            with codecs.open(content_file, 'w', 'utf-8') as f:
                f.write(cleaned_text)
            # end with
        except urllib2.HTTPError as e:
            logging.getLogger(name="SFGram").error(u"HTTP Error when downloading %s : %s" %
                                                   (self._plaintext_url.format(self._num), unicode(e)))
            pass
        # end try
    # end download

    # Download images
    def download_images(self, images_directory):
        # Get all images
        images = self._explore_http_directory(self._files_url.format(self._num))

        # Download all images from Gutenberg
        index = 0
        for image in images:
            image_filename = image.split('/')[-1]
            logging.getLogger(name="SFGram")\
                .debug(u"Downloading image %s to %s" % (image, os.path.join(images_directory, image_filename)))
            self._download_http_file(image, os.path.join(images_directory, image_filename))
            index += 1
        # end for

        # Download all images from Wikipedia
        if 'Images' in self._attrs:
            for image in self._attrs['Images']:
                image_filename = image.split('/')[-1]
                logging.getLogger(name="SFGram") \
                    .debug(u"Downloading image %s to %s" % (image, os.path.join(images_directory, image_filename)))
                self._download_http_file(image, os.path.join(images_directory, image_filename))
            # end for
        # end if

        # Download cover
        if 'Cover' in self._attrs:
            image_filename = self._attrs['Cover'].split('/')[-1]
            file_ext = os.path.splitext(image_filename)[-1]
            self._download_http_file(self._attrs['Cover'], os.path.join(images_directory, "cover" + file_ext))
        # end if
    # end download_images

    ###################################################
    #
    # PRIVATE
    #
    ###################################################

    # Get default attribute values
    def _get_default_values(self):
        """
        Get default attribute values
        :return:
        """
        return {'Publication date': -1}
    # end _get_default_values

    # Dowload HTTP file
    def _download_http_file(self, url, filename):
        """
        Download HTTP file
        :param url:
        :param filename:
        :return:
        """
        f = urllib2.urlopen(url)
        data = f.read()
        with open(filename, "wb") as code:
            code.write(data)
        # end with
    # end _download_http_file

    # Explore HTTP directory
    def _explore_http_directory(self, http_directory):
        """
        Explore HTTP directory
        :param http_directory:
        :return:
        """
        result = list()

        # Load HTML
        html = urlopen(http_directory).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # For each file entry
        for file_entry in soup.find_all('tr'):
            try:
                file_type = file_entry.find('td', attrs={'valign': 'top'}).find('img')['alt']
                file_link = file_entry.find('a')['href']
                if file_type == "[DIR]":
                    images = self._explore_http_directory(http_directory + file_link)
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

    # Load GoodReads information
    def _load_goodreads_information(self):
        """
        Get GoodReads information
        """
        # Search books
        ok = False
        while not ok:
            try:
                if "Original Title" in self._attrs:
                    books = self._goodreads_client.search_books(self._attrs["Original Title"])
                else:
                    success = False
                    while not success:
                        try:
                            books = self._goodreads_client.search_books(self._attrs["Title"])
                            success = True
                        except requests.exceptions.ConnectionError:
                            time.sleep(60)
                            pass
                        # end try
                    # end while
                # end if
                ok = True
            except goodreads.request.GoodreadsRequestException:
                if "Original Title" in self._attrs:
                    logging.getLogger(name="SFGram").warning("Error when retrieving information from Goodreads for {}"
                                                             .format(self._attrs['Original Title']))
                else:
                    logging.getLogger(name="SFGram").warning("Error when retrieving information from Goodreads for {}"
                                                             .format(self._attrs['Title']))
                # end if
                time.sleep(10)
                pass
            except TypeError:
                if "Original Title" in self._attrs:
                    logging.getLogger(name="SFGram").warning("Book \"{}\" not found on GoodReads"
                                                             .format(self._attrs['Original Title']))
                else:
                    logging.getLogger(name="SFGram").warning("Book \"{}\" not found on GoodReads"
                                                             .format(self._attrs['Title']))
                # end if
                self._attrs['GoodReads Not Found'] = True
                return
            # end try
        # end while
        time.sleep(10)

        # No ebooks
        book = books[0]
        for b in books:
            if not book.is_ebook:
                book = b
            # end if
        # end for

        # Get informations
        self._attrs['ISBN13'] = book.isbn13
        self._attrs['ISBN'] = book.isbn
        self._attrs['Similar Books'] = list()
        self._attrs['Cover'] = book.image_url
        self._attrs['Small Image'] = book.small_image_url
        self._attrs['GoodReads URL'] = book.link
        self._attrs['Description'] = book.description
        if book.average_rating is not None:
            self._attrs['Average Rating'] = float(book.average_rating)
        # end if
        self._attrs['Language Code'] = book.language_code
        if book.rating_dist is not None:
            self._attrs['Rating Count'] = int(book.ratings_count)
        # end if
        if book.num_pages is not None:
            self._attrs['Pages'] = int(book.num_pages)
        # end if
        self._attrs['Format'] = book.format

        # Publication date
        if '#text' in book.work['original_publication_year']:
            if self._attrs['Publication date'] == -1:
                self._attrs['Publication date'] = int(book.work['original_publication_year']['#text'])
            # end if
            self._attrs['GoodReads Publication date'] = int(book.work['original_publication_year']['#text'])
        # end if

        # Similar books
        try:
            for b in book.similar_books:
                self._attrs['Similar Books'].append(b.title)
            # end for
        except KeyError:
            self._attrs['Similar Books'] = list()
        # end try

        # Genres
        try:
            for shelf in book.popular_shelves:
                self._attrs['Genres'].append(shelf.name)
            # end
        except TypeError:
            self._attrs['Similar Books'] = list()
        # end try
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
        try:
            # Publication date
            if "Publication date" in wiki_info:
                year = re.search(r"([12][0-9]{3})", wiki_info['Publication date']).groups()[0]
                self._attrs['Publication date'] = int(year)
                self._attrs['Wikipedia Publication date'] = int(year)
            elif "Published" in wiki_info:
                year = re.search(r"([12][0-9]{3})", wiki_info['Published']).groups()[0]
                self._attrs['Publication date'] = int(year)
                self._attrs['Wikipedia Publication date'] = int(year)
            else:
                self._attrs['Publication date'] = -1
            # end if
        except AttributeError:
            self._attrs['Publication date'] = -1
            pass
        # end try
    # end _extract_publication_date

    # Load information from wikipedia
    def _load_wikipedia_information(self):
        """
        Load information from Wikipedia
        """
        # Search for the book on wikipedia
        searches = wikipedia.search(self._attrs['Title'] + u" " + self._attrs['Authors'][0])

        try:
            # For each response
            for page_title in searches:
                if "disambiguation" not in page_title:
                    try:
                        page = wikipedia.page(page_title)
                        wiki_info = self._get_wikipedia_infobox(page.html())
                        if u"Published" in wiki_info or u"Published in" in wiki_info or u"Publication date" in wiki_info:
                            # Country
                            self._add_attr_field(wiki_info, 'Country', 'Country')

                            # Original title
                            self._attrs['Original Title'] = page.original_title

                            # Image
                            try:
                                self._attrs['Images'] = self._filter_wikipedia_images(page.images)
                            except KeyError:
                                pass
                            # end try

                            # Find plot
                            for section in ("Plot", "Plot summary", "Synopsis"):
                                if page.section(section) is not None:
                                    self._attrs['Plot'] = unicode(page.section(section))
                                # end if
                            # end for

                            # Other
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
        except wikipedia.exceptions.PageError:
            logging.getLogger(name="SFGram").error("Cannot find Wikipedia page for {}".format(self._attrs['Title']))
            self._attrs['Wikipedia Not Found'] = True
        # end try
    # end _load_wikipedia_info

    def _filter_subjects(self, subject):
        """
        Filter subjects
        :param subjects:
        :return:
        """
        filter = ["Science fiction", "Fiction"]
        if subject not in filter:
            return subject
        # end if
        return None
    # end _filter_subjects

    # Load Gutenberg information
    def _load_gutenberg_information(self):
        """
        Load Gutenberg information
        :return:
        """
        # Load HTML
        success = False
        errors = 0
        while not success:
            try:
                html = urlopen(self._ebooks_url + unicode(self._num)).read()
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(self._ebooks_url + unicode(self._num), unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {} : {}".format(self._ebooks_url + unicode(self._num), unicode(e)))
                exit()
        # end while

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
        self._attrs['Genres'] = list()
        for subject in soup.find_all('td', attrs={'datatype': u"dcterms:LCSH"}):
            filtered_subject = self._filter_subjects(subject.find('a').text.strip().split(" -- ")[0])
            if filtered_subject is not None:
                self._attrs['Genres'].append(filtered_subject.title())
            # end if
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
