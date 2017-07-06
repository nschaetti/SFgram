# -*- coding: utf-8 -*-
#

import bs4 as BeautifulSoup
import logging
import os
import urllib2
from urllib2 import urlopen
import spacy
from GoodReadsConnector import GoodReadsConnector
from GutenbergBookInformation import GutenbergBookInformation
from WikipediaBookInformation import WikipediaBookInformation
from cleaning.TextCleaner import TextCleaner
from db.Author import Author
from db.Book import Book
from db.Country import Country
from db.Genre import Genre
from db.Image import Image


# Download error
class DownloadErrorException(Exception):
    """
    Download error exception
    """
    pass
# end DownloadErrorException


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

    ####################################################
    # Public
    ####################################################

    # Open the category for listing
    def open(self, num, start_index=1, skip_book=0):
        """
        Open a category for listing
        :param num: The category number.
        :param start_index:
        """
        # Final URL
        self._url += str(num)

        # Start index
        self._start_index = start_index

        # Skip book
        self._skip_book = skip_book
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

        # Get authors of create them
        authors = list()
        for a in gutenberg_info['Authors']:
            authors.append(GutenbergBookshelf.get_author(a))
        # end for

        # Get book or create one
        new_book = Book.get_by_title(gutenberg_info['Title'])
        if new_book is None:
            new_book = Book()
            new_book.save()
        # end if

        # Save/update each authors
        for book_author in authors:
            book_author.n_books += 1
            book_author.books.append(new_book)
            book_author.save()
        # end for

        # Gutenberg information
        new_book = self._save_gutenberg_information(new_book, gutenberg_info, authors)

        # Goodreads informations
        if goodreads_info['goodreads_found']:
            new_book = self._save_goodreads_information(new_book=new_book, goodreads_info=goodreads_info)
        # end if

        # Wikipedia information
        if wikipedia_info['wikipedia_found']:
            new_book = self._save_wikipedia_information(new_book, wikipedia_info, authors)
        # end if

        # Publication date
        if 'Publication date' in wikipedia_info:
            new_book.publication_date = wikipedia_info['Publication date']
        elif 'Publication date' in goodreads_info:
            new_book.publication_date = goodreads_info['Publication date']
        # end if

        # Save book in DB
        new_book.save()

        # Remove from the list
        self._books.remove(book_url)

        return new_book
    # end next

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return: object.
        """
        return self
    # end __iter__

    # Get or create author
    @staticmethod
    def get_author(author_name):
        """
        Get or create author
        :return:
        """
        # Check if exists
        if Author.exists(author_name=author_name):
            return Author.get_by_name(author_name)
        else:
            # Get info from Wikipedia
            wikipedia_info = WikipediaBookInformation.get_author_information(author_name)

            # New author
            author = Author(name=author_name)

            # If found in Wikipedia
            if wikipedia_info['wikipedia_found']:
                # Born
                if 'Born' in wikipedia_info:
                    author.birth_date = wikipedia_info['Born']
                # end if

                # Died
                if 'Died' in wikipedia_info:
                    author.death_date = wikipedia_info['Died']
                # end if

                # Bio
                if 'Bio' in wikipedia_info:
                    author.bio = wikipedia_info['Bio']
                # end if

                # Bio
                if 'Summary' in wikipedia_info:
                    author.summary = wikipedia_info['Summary']
                # end if

                # URL
                author.wikipedia_page = wikipedia_info['URL']

                # Ambigue?
                author.ambiguation = wikipedia_info['Ambiguation']
            # end if

            # Log
            logging.info(u"New author {} ({} - {})".format(author.name, author.birth_date, author.death_date))

            # Return
            return author
        # end if
    # end _get_author

    ####################################################
    # Private
    ####################################################

    # Save Gutenberg information
    def _save_gutenberg_information(self, new_book, gutenberg_info, authors):
        """

        :param new_book:
        :param gutenberg_info:
        :param authors:
        :return:
        """
        # Text file URL
        plaintext_url = u"http://www.gutenberg.org/ebooks/{}.txt.utf-8"

        #
        # Gutenberg information
        #
        new_book.num = gutenberg_info['#']
        new_book.title = gutenberg_info['Title']
        new_book.author = authors[0]
        new_book.authors = authors
        new_book.category = gutenberg_info['Category']
        new_book.copyright = gutenberg_info['Copyright']
        new_book.language = gutenberg_info['Language']
        new_book.loc_class = gutenberg_info['LoC Class']
        new_book.release_date = gutenberg_info['Release Date']

        # Add genres
        self._save_genres(gutenberg_info['Genres'], new_book)

        # Save images
        GutenbergBookshelf.download_images(gutenberg_info['Images'], new_book.images)

        # Save content
        GutenbergBookshelf.download_content(plaintext_url.format(gutenberg_info['#']), new_book)

        # Covert-art
        if 'Cover-art' in gutenberg_info:
            try:
                new_book.covert_art = GutenbergBookshelf.download_image(gutenberg_info['Cover-art'])
            except DownloadErrorException:
                pass
            # end try
        # end if

        return new_book
    # end _save_gutenberg_information

    # Download content
    @staticmethod
    def download_content(content_url, new_book):
        """
        Download content
        :param content_url:
        :param new_book:
        :return:
        """
        # Try
        try:
            # Download
            ext, data = GutenbergBookshelf.download_http_file(content_url)

            # Clean content
            cleaner = TextCleaner()
            cleaned_text, cleaned = cleaner(data.decode('utf8', errors='ignore'))
            new_book.cleaned = cleaned

            # Add  content
            new_book.content = cleaned_text
            new_book.content_available = True

            # New parser
            if new_book.language.lower() == u"english":
                nlp = spacy.load('en')
                words = nlp(cleaned_text)
                new_book.content_tokens = len(words)
            # end if
        except DownloadErrorException as e:
            logging.fatal(u"Impossible to download {}".format(content_url))
            new_book.content_available = False
            pass
        # end try
    # end download_content

    # Download images
    @staticmethod
    def download_images(images_url, images):
        """
        Download images
        :param images_url:
        :param images:
        :return:
        """
        for url in images_url:
            # Add
            try:
                images.append(GutenbergBookshelf.download_image(url))
            except DownloadErrorException:
                pass
            # end try
        # end for
    # end _download_images

    # Download an image
    @staticmethod
    def download_image(image_url):
        """
        Down an image
        :param image_url:
        :return:
        """
        # Get/create image
        if not Image.exists(image_url):
            # New image
            image = Image()

            # Data
            ext, data = GutenbergBookshelf.download_http_file(image_url)

            # Info
            image.image.put(data)
            image.url = image_url
            image.extension = ext

            # Save
            image.save()
            return image
        else:
            return Image.get_by_url(image_url)
        # end if
    # end _download_image

    # Save Goodreads information
    def _save_goodreads_information(self, new_book, goodreads_info, ):
        """

        :param new_book:
        :param goodreads_info:
        :return:
        """
        # General
        new_book.average_rating = goodreads_info['Average Rating']
        new_book.description = goodreads_info['Description']
        new_book.format = goodreads_info['Format']
        new_book.pages = goodreads_info['Pages'] if 'Pages' in goodreads_info else None
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

        # Add genres
        self._save_genres(goodreads_info['Genres'], new_book)

        # Download images
        new_book.cover = GutenbergBookshelf.download_image(goodreads_info['Cover'])
        new_book.small_image = GutenbergBookshelf.download_image(goodreads_info['Small Image'])

        return new_book
    # end _save_gutenberg_information

    # Save Wikipedia information
    def _save_wikipedia_information(self, new_book, wikipedia_info, authors):
        """

        :param new_book:
        :param wikipedia_information:
        :return:
        """
        # Original Title
        if 'Original Title' in wikipedia_info:
            new_book.original_title = wikipedia_info['Original Title']
        # end if

        # Get country
        if 'Country' in wikipedia_info:
            country_name = wikipedia_info['Country']
        else:
            country_name = "Unknown"
        # end if

        # Create or get
        if Country.exists(country_name):
            country = Country.get_by_name(country_name)
        else:
            # New country
            country = Country(name=country_name)
            logging.info(u"New country {}".format(country.name))
        # end if

        # Increments books
        country.n_books += 1

        # Set country
        new_book.country = country

        # Add book to country
        country.books.append(new_book)

        # Add authors to country
        for book_author in authors:
            country.authors.append(book_author)
        # end for

        # Save book
        logging.debug(u"Saving/updating country {}".format(country.name))
        country.save()

        # Wikipedia information
        new_book.cover_artist = wikipedia_info['Cover artist'] if 'Cover artist' in wikipedia_info else None
        new_book.wikipedia_publication_date = wikipedia_info['Publication date'] \
            if 'Publication date' in wikipedia_info else None
        new_book.wikipedia_url = wikipedia_info['wikipedia_url']
        new_book.wikipedia_found = wikipedia_info['wikipedia_found']

        # Ambigue?
        new_book.ambiguation = wikipedia_info['Ambiguation']

        # Save images
        GutenbergBookshelf.download_images(wikipedia_info['Images'], new_book.images)

        return new_book
    # end _save_wikipedia_information

    # Save genres
    def _save_genres(self, genres, new_book):
        """
        Save genres
        :param genres:
        :param new_book:
        :return:
        """
        # Add genres
        for book_genre in genres:
            if Genre.exists(book_genre):
                genre = Genre.get_by_name(book_genre)
            else:
                genre = Genre(name=book_genre)
            # end if

            # Add
            new_book.genres.append(genre)
            genre.books.append(new_book)

            # Save
            genre.save()
        # end for
    # end _save_genres

    # Load elements
    def _load(self):
        """
        Load the elements of the current page.
        """
        # Load HTML
        try:
            logging.info(u"Downloading page " + self._url + u"?start_index=" + unicode(self._start_index))
            html = urlopen(self._url + u"?start_index=" + unicode(self._start_index)).read()
        except urllib2.URLError:
            raise StopIteration
        # end try

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find all 'booklink'
        book_links = soup.find_all('li', attrs={"class": u"booklink"})

        # For all book link
        skip = 0
        for book_link in book_links:
            if skip >= self._skip_book:
                self._books.append(self._parse_book_link(book_link))
            else:
                skip += 1
            # end if
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

    # Dowload HTTP file
    @staticmethod
    def download_http_file(url):
        """
        Download HTTP file
        :param url:
        :return:
        """
        # Get ext
        ext = os.path.splitext(url.split("/")[-1])[1]

        # Control
        success = False
        count = 0

        # Try
        while not success:
            try:
                logging.debug(u"Downloading HTTP file {}".format(url))
                f = urllib2.urlopen(url)
                success = True
            except urllib2.URLError:
                pass
            # end try

            # Count
            count += 1

            # Limit
            if count >= 10:
                logging.fatal(u"Impossible to download {}".format(url))
                raise DownloadErrorException(u"Impossible to download {}".format(url))
            # end if
        # end while

        return ext, f.read()
    # end download_http_file

# end GutenbergBookshelf
