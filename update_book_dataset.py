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

    # Load or create collections
    book_collection = ds.BookCollection.create(args.output_dir)
    country_collection = ds.CountryCollection.create(args.output_dir)
    year_collection = ds.CountryCollection.create(args.output_dir)

    # Open category
    gutenberg_con = gb.GutenbergBookshelf()
    gutenberg_con.open(num=68, start_index=args.start_index, skip_book=args.skip_book)

    # For each book
    for index, book_informations in enumerate(gutenberg_con):
        # New book
        book = ds.Book(title=book_informations['title'])
        book_collection.add(book)

        # Wikipedia & Goodreads information
        wikipedia_info = wp.WikipediaBookInformation.get_book_information(book_informations['title'],
                                                                          book_informations['authors'][0])
        goodreads_info = gr.GoodReadsConnector.get_book_info(book_informations['title'])

        # Import data
        book.import_from_dict(book_informations, exclude=['authors', 'images', 'cover', 'content', 'genres'])
        book.import_from_dict(wikipedia_info, exclude=['images', 'country'])
        book.import_from_dict(goodreads_info, exclude=['small_image'])

        # For each authors
        for author_name in book_informations['authors']:
            # Author object
            author = ds.Author(name=author_name)
            author = book_collection.add(author)

            # Info
            author.import_from_dict(wp.WikipediaBookInformation.get_author_information(author_name))

            # Add to book's authors
            if author.id not in book.authors and author.id != book.author:
                book.authors += [author.id]
                book.n_authors += 1
            # end if

            # Add book to author's books
            if book.id not in author.books:
                author.books += [book.id]
                author.n_books += 1
            # end if
        # end for
        book.author = book.authors[0]

        # Country
        if 'country' not in wikipedia_info.keys():
            country_name = u"Unknown"
        else:
            country_name = wikipedia_info['country']
        # end if
        country = ds.Country(country_name)
        country = country_collection.add(country)
        country.books.append(book.id)
        country.n_books += 1
        book.country = country.id

        # Year
        if not book.wikipedia['found'] and not book.goodreads['found']:
            pub_year = -1
        elif not book.wikipedia['found'] and book.goodreads['found']:
            pub_year = book.goodreads['year']
        elif book.wikipedia['found'] and not book.goodreads['found']:
            pub_year = book.wikipedia['year']
        else:
            pub_year = book.wikipedia['year'] if book.wikipedia['year'] != -1 else book.goodreads['year']
        # end if
        year = ds.Year(year=pub_year)
        year = year_collection.add(year)
        year.books.append(book.id)
        year.n_books += 1
        book.year = pub_year

        # Save gutenberg images
        for (data, name) in book_informations['images']:
            book_collection.save_image(dataset.get_dataset_directory(), book_collection.get_next_book_id(), data, name)
        # end for

        # Save gutenberg images
        if wikipedia_info['wikipedia']['found']:
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
        if 'small_image' in goodreads_info.keys():
            book_collection.save_image(dataset.get_dataset_directory(), book_collection.get_next_book_id(),
                                           goodreads_info['small_image'][0], goodreads_info['small_image'][1])
            # end if

        # Save content
        if book.content_available:
            book_collection.save_content(dataset.get_dataset_directory(), book_collection.get_next_book_id(),
                                         book_informations['content'])
        # end if

        # Save collections
        book_collection.save(dataset.get_dataset_directory())
        country_collection.save(dataset.get_dataset_directory())
        year_collection.save(dataset.get_dataset_directory())
    # end for

# end if
