# -*- coding: utf-8 -*-
#

import argparse
import wikipediaorg as wp
from archives import dataset as ds

######################################################
# Functions
######################################################

######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Check author's wikipedia page")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    parser.add_argument("--start", type=int, help="Starting index", default=1)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)

    # Author attributes
    author_attrs = ['born', 'died', 'summary', 'bio']

    # For each author
    for author in book_collection.get_authors():
        if author.id >= args.start:
            # Show
            print(u"Author {} name {} date {}/{}".format(author.id, author.name, author.born, author.died))
            if 'url' in author.wikipedia:
                print(u"Wikipedia page : {}".format(author.wikipedia['url']))
            else:
                print(u"Wikipedia page : none")
            # end if
            print(u"Summary : {}".format(author.summary))

            # Ask
            print(u"Right page? (empty=keep, c=clear, other=new page) ")
            page_answer = raw_input(u"Page? ").strip()

            # No page
            if page_answer == u"c":
                # Set not found
                author.wikipedia = {'found': False}

                # Delete useless attributes
                for attr in author_attrs:
                    if hasattr(author, attr):
                        try:
                            delattr(author, attr)
                        except AttributeError:
                            pass
                        # end try
                    # end if
                # end for
            elif page_answer == u"":
                pass
            else:
                # Searches
                author_research = \
                    [
                        author.name,
                        page_answer[page_answer.rfind(u'/')+1:].replace(u'_', u' ').replace(u'(', u'').replace(u')', u''),
                        page_answer[page_answer.rfind(u'/')+1:].replace(u'_', u' ')
                    ]

                # Wikipedia informations
                wikipedia_info = wp.WikipediaBookInformation.get_author_information_from_url(author_research, page_answer)

                # Wikipedia part
                author.wikipedia['url'] = page_answer
                author.wikipedia['found'] = True

                # For each attributes
                for attr in author_attrs:
                    try:
                        setattr(author, attr, wikipedia_info[attr])
                    except KeyError:
                        try:
                            delattr(author, attr)
                        except AttributeError:
                            pass
                            # end try
                    # end try
                # end for
            # end if

            # Save
            book_collection.save(dataset.get_dataset_directory())
            print(u"")
        # end if
    # end for

# end if
