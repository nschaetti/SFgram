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
#
# Main
#
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
        book.cover_art_url = book_informations['cover-art-url'] if 'cover-art-url' in book_informations.keys() else None

        # Wikipedia information
        wikipedia_info = wp.WikipediaBookInformation.get_book_information(book_informations['title'],
                                                                          book_informations['authors'][0])

        # Wikipedia properties
        book.wikipedia['found'] = wikipedia_info['found']
        if wikipedia_info['found']:
            book.wikipedia['ambiguation'] = wikipedia_info['ambiguation']
            book.original_title = wikipedia_info['original-title']
            book.plot = wikipedia_info['plot']
            book.summary = wikipedia_info['summary']
            book.wikipedia['url'] = wikipedia_info['url']
            book.cover_artist = wikipedia_info['cover-artist']
            book.wikipedia['year'] = wikipedia_info['publication-year']
            book.publisher = wikipedia_info['publisher']
            book.published_in = wikipedia_info['published-in']
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
            book.pages = goodreads_info['pages']
            book.format = goodreads_info['format']
            book.goodreads['year'] = goodreads_info['publication-date']
        # end if

        # Save gutenberg images
        for (data, ext) in book_informations['images']:
            book_collection.save_image(dataset.get_book_images_directory(), book_collection.get_next_book_id(), data, ext)
        # end for

        """"# Save cover
        book_collection.save_cover(book_informations['cover'][0], book_informations['cover'][1])

        # Save cover-art
        book_collection.save_cover(book_informations['cover-art'][0], book_informations['cover-art'][1])

        # Save content
        if book.content_available:
            book_collection.save_content(book_informations['content'][0], book_informations['content'][1])
        # end if
        """

        # Add to book collection
        book_collection.add(book)

        # Save book collection
        # book_collection.save()
        print(book)
    # end for

# end if
