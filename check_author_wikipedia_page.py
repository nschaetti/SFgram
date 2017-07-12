# -*- coding: utf-8 -*-
#

import argparse
import logging
from mongoengine import *
import download as dw
from db.Author import Author
from db.Country import Country
from db.Book import Book
from db.Movie import Movie
import wikipedia
from dateutil.parser import parse

######################################################
#
# Functions
#
######################################################

######################################################
#
# Main
#
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Check all books with unknown country")

    # Argument
    parser.add_argument("--database", type=str, help="Database name", default="sfgram", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # Connection to MongoDB
    connect(args.database)

    # For each author
    for author in Author.objects():
        # Ambiguation?
        if author.ambiguation:
            print(u"Author {}".format(author.name))
            print(u"Years {} to {}".format(author.birth_date, author.death_date))
            print(u"Summary {}".format(author.summary))
            print(u"Wikipedia page {}".format(author.wikipedia_page))
            action = raw_input("Action: ")
            if action == "":
                continue
            elif action == "none":
                author.wikipedia_page = ""
                author.bio = ""
                author.summary = ""
                birth_date = raw_input("Birth date : ")
                author.birth_date = parse(birth_date)
                death_date = raw_input("Death date : ")
                author.death_date = parse(death_date)
                author.save()
            else:
                # Get page
                page = wikipedia.page(action)

                # Get information in the box
                wiki_info = dw.WikipediaBookInformation.get_infobox(page.html())

                # Born
                if "Born" in wiki_info:
                    author.birth_date = dw.WikipediaBookInformation.extract_date(wiki_info['Born'])
                # end if

                # Died
                if "Died" in wiki_info:
                    author.death_date = dw.WikipediaBookInformation.extract_date(wiki_info['Died'])
                # end if

                # Death
                if "Death" in wiki_info:
                    author.death_date = dw.WikipediaBookInformation.extract_date(wiki_info['Death'])
                # end if

                # Summary
                author.summary = page.summary

                # Find biography
                bio = ""
                for section in ("Life", "Early life", "Career", "Personal life", "Death", "Biography"):
                    if page.section(section) is not None:
                        bio += u" " + unicode(page.section(section))
                    # end if
                # end for
                author.bio = bio

                # Page
                author.wikipedia_page = page.url

                # Save
                author.save()
            # end if
        # end if
    # end for

# end if
