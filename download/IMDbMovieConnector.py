# -*- coding: utf-8 -*-
#

# Import
import os
import imdb
import urllib2
from urllib2 import urlopen
import logging
import bs4 as BeautifulSoup
import imdb
from dateutil.parser import parse
import re
import time
from db.Movie import Movie
from db.Poster import Poster


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
        html = urlopen(url).read()
        time.sleep(2)

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
        html = urlopen(url).read()

        # Parse HTML
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")

        # Poster div
        poster_div = soup.find('div', attrs={"class": u"poster"})

        # if poster exists
        if poster_div is not None:
            # Poster link
            poster_page_link = u"http://www.imdb.com/" + poster_div.find('a').attrs['href']

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

    # Load elements
    def _load(self):
        """
        Load the elements of the current page.
        """
        # Page url
        page_url = self._url.format(self._genre, self._page_index)

        # Load HTML
        try:
            logging.info(u"Downloading page " + page_url)
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
                    if found_movie['year'] == movie_year:
                        # Movie does not exists
                        if not Movie.exists(movie_title, movie_year):
                            # New movie
                            movie = Movie(movie_id=str(found_movie.movieID), title=found_movie['title'], year=movie_year)

                            # ID and URL
                            movie.url = movie_link

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

                                # Save movie
                                movie.save()

                                # Add
                                self._movies.append(movie)
                            # end if
                            break
                        # end if
                    # end if
                except KeyError:
                    pass
                # end try
            # end for
        # end for

        # Next page
        self._page_index += 1
    # end _load

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
                exit()
                # end if
        # end while

        return ext, f.read()
    # end download_http_file

# end IMDbMovieConnector
