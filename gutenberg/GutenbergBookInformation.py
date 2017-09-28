# -*- coding: utf-8 -*-
#

# Import
import re
from dateutil.parser import parse
from tools.Tools import Tools
import logging


# Access to Gutenberg book information
class GutenbergBookInformation(object):
    """
    Access to Gutenberg book information.
    """

    # Get book information
    @staticmethod
    def get_book_info(num):
        """
        Load Gutenberg book information
        :return:
        """
        # URL
        ebooks_url = u"http://www.gutenberg.org/ebooks/" + unicode(num)
        files_url = u"http://www.gutenberg.org/files/{}/"

        # Result
        info = {'gutenberg': dict()}

        # Download HTML page
        logging.getLogger(u"SFGram").info(u"Gutenberg page found at {}".format(ebooks_url))
        soup = Tools.download_html(ebooks_url)

        # Find title and author
        title_author = soup.find('h1', attrs={'itemprop': u"name"}).text.split(" by ")
        info['gutenberg']['num'] = num
        info['title'] = title_author[0].strip()

        # URL
        info['gutenberg']['url'] = ebooks_url

        # Authors
        if len(title_author) > 1:
            info['authors'] = GutenbergBookInformation.parse_authors(title_author[1].strip())
        else:
            info['authors'] = list()
            for author_link in soup.find_all('a', attrs={'itemprop': u"creator"}):
                info['authors'].append(re.search(r"([a-zA-Z\,\s]*)", author_link.text).groups()[0].strip())
            # end for
        # end if

        # Author's name
        if len(info['authors']) > 0:
            info['author_name'] = info['authors'][0]
        # end if

        # Language
        info['language'] = soup.find('tr', attrs={'itemprop': u"inLanguage"}).find('td').text.strip()

        # LoC class
        try:
            info['loc_class'] = soup.find('tr', attrs={'datatype': u"dcterms:LCC"}).find('td').find(
                'a').text.strip()
        except AttributeError:
            info['loc_class'] = ""
        # end try

        # Empty list of genres
        info['genres'] = list()

        # Filter and add subject
        for subject in soup.find_all('td', attrs={'datatype': u"dcterms:LCSH"}):
            filtered_subject = GutenbergBookInformation.filter_subjects(subject.find('a').text.strip().split(" -- ")[0])
            if filtered_subject is not None:
                info['genres'].append(filtered_subject.title())
            # end if
        # end for

        # Category
        info['category'] = soup.find('td', attrs={'property': u"dcterms:type"}).text.strip()

        # Release date
        info['release_date'] = parse(
            soup.find('td', attrs={'itemprop': u"datePublished"}).text.strip()).isoformat()

        # Copyright
        info['copyright'] = soup.find('td', attrs={'property': u"dcterms:rights"}).text.strip()

        # Images
        info['images_urls'] = GutenbergBookInformation.explore_http_directory(files_url.format(num))

        # Cover art
        img_cover_art = soup.find('img', attrs={'class': u"cover-art"})
        if img_cover_art is not None:
            # Get URL
            cover_art_url = img_cover_art.attrs['src']

            # Add http:
            if cover_art_url[:5] != "http:":
                cover_art_url = "http:" + cover_art_url
            # end if

            # Save
            info['cover_art_url'] = cover_art_url
        # end if

        return info
    # end get_book_info

    # Parse authors
    @staticmethod
    def parse_authors(author_text):
        """
        Parse authors' name.
        :param author_text: Text to parse.
        :return: Parsed author names.
        """
        return author_text.split(" and ")
    # end _parse_authors

    # Filter subjets
    @staticmethod
    def filter_subjects(subject):
        """
        Filter subjects
        :param subject:
        :return:
        """
        filter = ["Science fiction", "Fiction"]
        if subject not in filter:
            return subject
        # end if
        return None
    # end _filter_subjects

    ##########################################
    # Private
    ##########################################

    # Explore HTTP directory
    @staticmethod
    def explore_http_directory(http_directory):
        """
        Explore HTTP directory
        :param http_directory:
        :return:
        """
        # Results
        result = list()

        # Download HTTP file
        soup = Tools.download_html(http_directory)

        # For each file entry
        for file_entry in soup.find_all('tr'):
            try:
                file_type = file_entry.find('td', attrs={'valign': 'top'}).find('img')['alt']
                file_link = file_entry.find('a')['href']
                if file_type == "[DIR]":
                    images = GutenbergBookInformation.explore_http_directory(http_directory + file_link)
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

# end GutenbergBookInformation
