# -*- coding: utf-8 -*-
#

import argparse
import logging
import os
import wikipediaorg as wp
import dataset as ds
import goodreadscom as gr
import gutenberg as gb

######################################################
# Functions
#######################################################


# Create author
def create_author(author_name):
    """
    Create author
    :param author_name:
    :return:
    """
    # Info
    author_infos = wp.WikipediaBookInformation.get_author_information(author_name)

    # Author object
    author = ds.Author()
    author.name = author_name

    # Infos
    if author_infos['found']:
        if 'bio' in author_infos.keys():
            author.bio = author_infos['bio']
        # end if
        if 'born' in author_infos.keys():
            author.birth_date = author_infos['born']
        # end if
        if 'died' in author_infos.keys():
            author.death_date = author_infos['died']
        # end if
        author.summary = author_infos['summary']
        author.wikipedia['found'] = True
        author.wikipedia['url'] = author_infos['url']
        author.wikipedia['ambiguation'] = author_infos['ambiguation'] if 'ambiguation' in author_infos.keys() else False
    # end if

    # Add to book collection
    author = book_collection.add(author)

    return author
# end if

######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram book dataset")

    # Argument
    parser.add_argument("--output-dir", type=str, help="Output directory", required=True)
    parser.add_argument("--start-index", type=int, help="Start page index", default=1)
    parser.add_argument("--skip-book", type=int, help="Number of books to skip", default=0)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name=u"SFGram")

    # Dataset
    dataset = ds.Dataset(args.output_dir)
    dataset.check_directories()

    # Load or create book collection
    if os.path.exists(os.path.join(args.output_dir, "books.json")):
        book_collection = ds.BookCollection.load(os.path.join(args.output_dir, "books.json"))
    else:
        book_collection = ds.BookCollection()
    # end if

    # Open category
    gutenberg_con = gb.GutenbergBookshelf()
    gutenberg_con.open(num=68, start_index=args.start_index, skip_book=args.skip_book)

    # For each book
    for index, book_informations in enumerate(gutenberg_con):
        # New book
        book = ds.Book()

        # Gutenberg properties
        book.gutenberg['num'] = book_informations['#']
        book.title = book_informations['title']
        book.language = book_informations['language']
        book.loc_class = book_informations['loc-class']
        book.category = book_informations['category']
        book.release_date = book_informations['release-date']
        book.copyright = book_informations['copyright']
        book.images_urls = book_informations['images-urls']
        book.cover_art_url = book_informations['cover-url'] if 'cover-url' in book_informations.keys() else None
        book.content_available = book_informations['content-available']

        # For each authors
        for author in book_informations['authors']:
            author_obj = create_author(author)
            if author_obj.id not in book.authors and author_obj.id != book.author:
                book.authors += [author_obj.id]
            # end if
            if book.id not in author_obj.books:
                author_obj.books += [book.id]
                author_obj.n_books += 1
            # end if
        # end for
        book.author = book.authors[0]

        # Wikipedia information
        wikipedia_info = wp.WikipediaBookInformation.get_book_information(book_informations['title'],
                                                                          book_informations['authors'][0])

        # Wikipedia properties
        book.wikipedia['found'] = wikipedia_info['found']
        if wikipedia_info['found']:
            book.wikipedia['ambiguation'] = True if 'ambiguation' in wikipedia_info.keys() else False
            book.original_title = wikipedia_info['original-title']
            if 'plot' in wikipedia_info.keys():
                book.plot = wikipedia_info['plot']
            # end if
            book.summary = wikipedia_info['summary']
            book.wikipedia['url'] = wikipedia_info['url']
            if 'cover-artist' in wikipedia_info.keys():
                book.cover_artist = wikipedia_info['cover-artist']
            # end if
            if 'publication-year' in wikipedia_info.keys():
                book.wikipedia['year'] = wikipedia_info['publication-year']
            # end if
            if 'publisher' in wikipedia_info.keys():
                book.publisher = wikipedia_info['publisher']
            # end if
            if 'published-in' in wikipedia_info.keys():
                book.published_in = wikipedia_info['published-in']
            # end if
        # end if

        # Goodreads information
        goodreads_info = gr.GoodReadsConnector.get_book_info(book_informations['title'])

        # Goodreads properties
        book.goodreads['found'] = goodreads_info['found']
        if goodreads_info['found']:
            book.ISBN13 = goodreads_info['isbn13']
            book.ISBN = goodreads_info['isbn']
            book.similar_books = goodreads_info['similar-books']
            book.goodreads['url'] = goodreads_info['url']
            book.description = goodreads_info['description']
            book.average_rating = goodreads_info['average-rating']
            book.language_code = goodreads_info['language-code']
            book.rating_count = goodreads_info['rating-count']
            if 'pages' in goodreads_info.keys():
                book.pages = goodreads_info['pages']
            # end if
            book.format = goodreads_info['format']
            if 'publication-year' in goodreads_info.keys():
                book.goodreads['year'] = goodreads_info['publication-year']
            # end if
        # end if

        # Save gutenberg images
        for (data, name) in book_informations['images']:
            book_collection.save_image(dataset.get_dataset_directory(), book_collection.get_next_book_id(), data, name)
        # end for

        # Save gutenberg images
        if wikipedia_info['found']:
            for (data, name) in wikipedia_info['images']:
                book_collection.save_image(dataset.get_dataset_directory(), book_collection.get_next_book_id(), data,
                                           name)
            # end for
        # end if

        # Save cover-art
        if 'cover' in book_informations.keys():
            book_collection.save_cover(dataset.get_dataset_directory(), book_collection.get_next_book_id(),
                                           book_informations['cover'][0], book_informations['cover'][1])
        # end if

        # Save small image
        if 'small-image' in goodreads_info.keys():
            book_collection.save_image(dataset.get_dataset_directory(), book_collection.get_next_book_id(),
                                           goodreads_info['small-image'][0], goodreads_info['small-image'][1])
            # end if

        # Save content
        if book.content_available:
            book_collection.save_content(dataset.get_dataset_directory(), book_collection.get_next_book_id(),
                                         book_informations['content'])
        # end if

        # Add to book collection
        book_collection.add(book)

        # Save book collection
        book_collection.save(dataset.get_dataset_directory())
    # end for

# end if
