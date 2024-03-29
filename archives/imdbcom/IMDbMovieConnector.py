# -*- coding: utf-8 -*-
#

# Import
import bs4 as BeautifulSoup
import logging
import os
import re
import socket
import time
import urllib2
from urllib2 import urlopen

import imdb
from archives.db.Country import Country
from archives.db.Keyword import Keyword
from archives.db.Movie import Movie
from archives.db.Poster import Poster


# IMDb connector
class IMDbMovieConnector(object):

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        self._url = u"http://www.imdb.com/search/title?genres={}&title_type=feature&sort=year,asc&page={}&ref_=adv_nxt"
        self._page_index = 1
        self._movies = list()
        self._genre = ""
        self._ia = imdb.IMDb()
    # end __init__

    ####################################################
    # Public
    ####################################################

    # Open the genre for listing
    def open(self, genre, page_index=1):
        """
        Open a category for listing
        :param genre: The category number.
        :param page_index:
        """
        # Start index & genre
        self._page_index = page_index
        self._genre = genre
    # end open

    # Next element
    def next(self):
        """
        Next element
        """
        # If book list is empty, we reload
        if len(self._movies) == 0:
            self._load()
        # end if

        # Movie title
        movie_title = self._movies[0]

        # Remove
        self._movies.remove(movie_title)

        # Return
        return movie_title
    # end next

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return: object.
        """
        return self
    # end __iter__

    ####################################################
    # Private
    ####################################################

    # Extract poster source
    def _extract_poster_source(self, url):
        """
        Extract poster source
        :param url:
        :return:
        """
        # Load HTML
        logging.debug(u"Downloading page " + url)
        errors = 0
        success = False
        while not success:
            try:
                html = urlopen(url).read()
                time.sleep(2)
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(url, unicode(e)))
                errors += 1
                pass
            except socket.timeout as e:
                logging.error(u"Socket error trying to retrieve {} : {}".format(url, unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {}".format(url))
                exit()
            # end if
        # end while

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Poster source
        poster_source = soup.find('meta', attrs={"property": u"og:image"}).attrs['content']

        # Poster img
        return poster_source.split("_V1_")[0] + "_V1_.jpg"
    # end _extract_poster_source

    # Extract poster link
    def _extract_poster_link(self, url):
        """
        Extract poster link
        :param url:
        :return:
        """
        # Load HTML
        logging.debug(u"Downloading page " + url)

        # Get HTML code
        errors = 0
        success = False
        while not success:
            try:
                html = urlopen(url).read()
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(url, unicode(e)))
                errors += 1
                pass
            except socket.timeout as e:
                logging.error(u"Socket error trying to retrieve {} : {}".format(url, unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {}".format(url))
                exit()
            # end if
        # end while

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Poster div
        poster_div = soup.find('div', attrs={"class": u"poster"})

        # if poster exists
        if poster_div is not None:
            # Poster link
            try:
                poster_page_link = u"http://www.imdb.com/" + poster_div.find('a').attrs['href']
            except AttributeError:
                return None
            # end try

            # Extract poster source
            return self._extract_poster_source(poster_page_link)
        else:
            return None
        # end if
    # end _extract_poster_link

    # Extract year
    def _extract_year(self, year_string):
        """
        Extract year
        :param year_string:
        :return:
        """
        try:
            year = re.search(r"([12][0-9]{3})", year_string).groups()[0]
            return int(year)
        except:
            return 0
        # end try
    # end _extract_year

    # Extract plot
    def _extract_plot(self, movie_id):
        """
        Extract plot
        :param movie_id:
        :return:
        """
        # Default
        plot = ""

        # Movie URL
        plot_url = u"http://www.imdb.com/title/tt{}/plotsummary?ref_=tt_stry_pl".format(movie_id)

        # Get HTML
        logging.debug(u"Downloading page " + plot_url)

        # Get HTML code
        errors = 0
        success = False
        while not success:
            try:
                html = urlopen(plot_url).read()
                time.sleep(2)
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(plot_url, unicode(e)))
                errors += 1
                pass
            except socket.timeout as e:
                logging.error(u"Socket error trying to retrieve {} : {}".format(plot_url, unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {}".format(plot_url))
                exit()
            # end if
        # end while

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find all text block
        for plot_p in soup.find_all('p', attrs={"class": u"plotSummary"}):
            plot += " " + plot_p.text
        # end for

        # Clean text
        plot = plot.replace(u"\n", u"")
        for i in range(10):
            plot = plot.replace(u"  ", u" ")
        # end for

        return plot.strip()
    # end _extract_plot

    # Extract information
    def _extract_information(self, movie_id):
        """
        Extract country
        :param movie_id:
        :return:
        """
        # Default
        country = ""
        language = ""
        gross = None
        budget = None

        # Movie URL
        movie_url = u"http://www.imdb.com/title/tt{}/?ref_=adv_li_tt".format(movie_id)

        # Get movie HTML
        logging.debug(u"Downloading page " + movie_url)
        # Get HTML code
        errors = 0
        success = False
        while not success:
            try:
                html = urlopen(movie_url).read()
                success = True
            except urllib2.HTTPError as e:
                logging.error(u"HTTP error trying to retrieve {} : {}".format(movie_url, unicode(e)))
                errors += 1
                pass
            except socket.timeout as e:
                logging.error(u"Socket error trying to retrieve {} : {}".format(movie_url, unicode(e)))
                errors += 1
                pass
            # end try
            if errors >= 10:
                logging.fatal(u"Fatal HTTP error trying to retrieve {}".format(movie_url))
                exit()
            # end if
        # end while
        time.sleep(2)

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find all text block
        for text_block in soup.find_all('div', attrs={"class": u"txt-block"}):
            try:
                text_block_key = text_block.find('h4').text
                if text_block_key == u"Language:":
                    language = text_block.find('a').text
                elif text_block_key == u"Country:":
                    country = text_block.find('a').text
                elif text_block_key == u"Gross:":
                    gross_text = re.search(r"(\$(\d{1,3}(\,\d{1,3})*))",
                                           text_block.text).groups()[0]
                    gross = int(gross_text.replace(u'$', u'').replace(u',', u''))
                elif text_block_key == u"Budget:":
                    budget_text = re.search(r"(\$(\d{1,3}(\,\d{1,3})*))",
                                            text_block.text).groups()[0]
                    budget = int(budget_text.replace(u'$', u'').replace(u',', u''))
                # end if
            except AttributeError as e:
                print(e)
                pass
            # end try
        # end for

        return country, language, gross, budget
    # end _extract_information

    # Load elements
    def _load(self):
        """
        Load the elements of the current page.
        """
        # Page url
        page_url = self._url.format(self._genre, self._page_index)

        # Load HTML
        try:
            logging.info(u"Accessing page index {}".format(self._page_index))
            logging.debug(u"Downloading page " + page_url)
            html = urlopen(page_url).read()
            time.sleep(2)
        except urllib2.URLError:
            raise StopIteration
        # end try

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Find all 'booklink'
        movie_title_headers = soup.find_all('h3', attrs={"class": u"lister-item-header"})

        # For all book link
        for movie_title_header in movie_title_headers:
            # Title & link
            movie_title = movie_title_header.find('a').text
            movie_link = u"http://www.imdb.com/" + movie_title_header.find('a').attrs['href']

            # Year
            year_text = movie_title_header.find('span', attrs={"class": u"lister-item-year"}).text
            if len(year_text) > 0:
                movie_year = self._extract_year(year_text)
            else:
                continue
            # end if

            # Search
            found_movies = self._ia.search_movie(movie_title + " " + str(movie_year))

            # Select the good one
            for found_movie in found_movies:
                try:
                    if found_movie['year'] == movie_year and found_movie['kind'] == "movie":
                        # Movie does not exists
                        if not Movie.id_exists(found_movie.movieID):
                            # New movie
                            movie = Movie(movie_id=str(found_movie.movieID), title=found_movie['title'], year=movie_year)
                            movie.save()
                        else:
                            movie = Movie.get_by_id(found_movie.movieID)
                        # end if

                        # Country, language
                        country, language, gross, budget = self._extract_information(found_movie.movieID)

                        # Plot
                        plot = self._extract_plot(found_movie.movieID)

                        # Gross and budget
                        movie.gross = gross
                        movie.budget = budget

                        # ID and URL
                        movie.url = movie_link

                        # Language
                        try:
                            movie.language = found_movie['language']
                        except KeyError:
                            movie.language = language
                        # end try

                        # Plot
                        movie.plot = plot

                        # Poster
                        poster_link = self._extract_poster_link(movie_link)

                        # Only with poster
                        if poster_link is not None:
                            # Add/create poster
                            if Poster.exists(poster_link):
                                poster = Poster.get_by_url(poster_link)
                            else:
                                # New poster
                                poster = Poster()
                                poster.url = poster_link

                                # Download image
                                ext, data = IMDbMovieConnector.download_http_file(poster_link)
                                poster.image.put(data)
                            # end if

                            # Save poster
                            poster.save()
                            movie.poster = poster
                        # end if

                        # Save each keywords
                        for keyword in IMDbMovieConnector.get_keywords(found_movie.movieID):
                            if Keyword.exists(keyword_name=keyword):
                                keyword_object = Keyword.get_by_name(keyword_name=keyword)
                            else:
                                keyword_object = Keyword(name=keyword)
                            # end if

                            # Add movie and increment
                            """keyword_object.movies.append(movie)
                            keyword_object.n_movies += 1
                            print("9.3")"""
                            # Save keyword
                            keyword_object.save()

                            # Add
                            movie.keywords.append(keyword_object)
                        # end for

                        # Country
                        try:
                            the_country = found_movie['country']
                        except KeyError:
                            the_country = country
                        # end try

                        # If country not found, get Unknown
                        if the_country == "":
                            the_country = "Unknown"
                        # endif

                        # Create or get country
                        if Country().exists(the_country):
                            country_object = Country().get_by_name(the_country)
                        else:
                            country_object = Country(name=the_country)
                        # end if
                        country_object.movies.append(movie)
                        country_object.n_movies += 1
                        country_object.save()
                        movie.country = country_object

                        # Save movie
                        movie.save()

                        # Add
                        self._movies.append(movie)

                        break
                    # end if
                except KeyError:
                    pass
                # end try
            # end for
        # end for

        # Next page
        self._page_index += 1
    # end _load

    # Get keywords
    @staticmethod
    def get_keywords(movie_id):
        """
        Get genres
        :param movie_id:
        :return:
        """
        # Results
        keywords = list()

        # URL
        keywords_url = u"http://www.imdb.com/title/tt{}/keywords?ref_=tt_stry_kw".format(movie_id)

        # Download HTML
        logging.debug(u"Downloading page " + keywords_url)
        html = urlopen(keywords_url).read()
        time.sleep(2)

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Get keywords
        sodatext_divs = soup.find_all('div', attrs={"class": u"sodatext"})

        # For each div
        for sodatext in sodatext_divs:
            # Get keyword text
            keyword_text = sodatext.find('a').text

            # Add
            keywords.append(keyword_text)
        # end for

        return keywords
    # end get_keywords

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
                logging.debug(u"urllib2.URLError downloading HTTP file {}".format(url))
                pass
            # end try

            # Count
            count += 1

            # Limit
            if count >= 10:
                logging.fatal(u"Impossible to download {}".format(url))
                exit()
                # end if
        # end while

        return ext, f.read()
    # end download_http_file

# end IMDbMovieConnector
