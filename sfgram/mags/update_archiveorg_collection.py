# -*- coding: utf-8 -*-
#

import argparse
from mongoengine import *
from archives import internetarchiveorg as ia, dataset as ds, isfdb
from tools.Tools import Tools


######################################################
#
# Functions
#
######################################################


# Get an author
def get_author(author_name):
    """
    Get an author
    :param author_name:
    :return:
    """
    # Check if exists
    if Author.exists(author_name=author_name):
        return Author.get_by_name(author_name)
    else:
        return Author(name=author_name)
    # end if
# end create_author


# Get image data
def get_image(image_url):
    """
    Get image data
    :param image_url:
    :return:
    """
    # Get/create image
    if image_url != "":
        # Download
        xt, d = Tools.download_http_file(image_url)
        return xt, d
    # end if

    return None
# end get_image


######################################################
#
# Main
#
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram archive.org collection in the dataset")

    # Argument
    parser.add_argument("--output-dir", type=str, help="Output directory", required=True)
    parser.add_argument("--collection", type=str, help="Collection's name", required=True)
    parser.add_argument("--author", type=str, help="Author's name", required=True)
    parser.add_argument("--country", type=str, help="Country's name", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.output_dir)
    dataset.check_directories()

    # Load or create collections
    book_collection = ds.BookCollection.create(args.output_dir)
    country_collection = ds.CountryCollection.create(args.output_dir)
    year_collection = ds.YearCollection.create(args.output_dir)

    # Country
    if country_collection.get_by_name(args.country) is None:
        country = ds.Country(country_name=args.country)
    else:
        country = country_collection.get_by_name(args.country)
    # end if

    # AI collection
    collection = ia.ArchiveOrgCollection(args.collection)

    # Get collection information
    collection_info = ia.ArchiveOrgCollectionInformation.get_item_information(args.collection)

    # Create author
    if book_collection.get_author_by_name(name=collection_info['name']) is None:
        author = ds.Author(name=collection_info['name'])
        author = book_collection.add(author)
    else:
        author = book_collection.get_author_by_name(name=collection_info['name'])
    # end if

    # Authors books
    author_books = dict()

    # List items
    for item in collection:
        # Get informations
        info = ia.ArchiveOrgBookInformation.get_item_information(item)

        try:
            isfdb_info = isfdb.ISFDbBookInformation.get_book_information(info['isfdb_link'])
        except KeyError:
            print(u"Error retrieving ISFDB info")
            continue
        # end try

        # If there is text
        if not info['content_error']:
            # Book's name
            book_title = args.author + u" " + isfdb_info['Date'].strftime("%B") + u" " + unicode(isfdb_info['Date'].year)

            # Create of get book
            if not book_collection.exists(book_title):
                print(u"New book {}".format(book_title))

                # New book object
                book = ds.Book(title=book_title, author_name=author.name)
                book_collection.add(book)

                # For each content
                for book_content in info['contents']:
                    # Info
                    content_title = book_content['name']
                    content_author = book_content['author']

                    # Add author
                    if book_collection.get_author_by_name(name=content_author) is not None:
                        add_author = book_collection.get_author_by_name(content_author)
                    else:
                        add_author = ds.Author(name=content_author)
                        book_collection.add(add_author)
                    # end if

                    # Add book to author's books
                    if book.id not in add_author.books:
                        add_author.books.append(book.id)
                    # end if

                    # Add author to book's authors
                    if add_author.id not in book.authors:
                        book.authors.append(add_author.id)
                    # end if

                    # Add to contents
                    if {'title': content_title, 'author': add_author.id} not in book.contents:
                        book.contents.append({'title': content_title, 'author': add_author.id})
                    # end if
                # end for

                # Properties
                book.author = author.id
                if book.id not in author.books:
                    author.books.append(book.id)
                # end if
                if author.id not in book.authors:
                    book.authors.append(author.id)
                # end if

                # Year
                book.year = isfdb_info['Date'].year

                # Create or get year
                if year_collection.get_year(book.year) is not None:
                    year_object = year_collection.get_year(book.year)
                else:
                    year_object = ds.Year(year=book.year)
                    year_collection.add(year_object)
                # end if

                # Add book to year
                if book.id not in year_object.books:
                    year_object.books.append(book.id)
                # end if

                # Add book to country
                if book.id not in country.books:
                    country.books.append(book.id)
                # end if

                # Add country to book
                if country.id not in book.countries:
                    book.countries.append(country.id)
                # end if

                # Add author to country
                if author.id not in country.books:
                    country.authors.append(author.id)
                # end if

                # Get IA cover image
                if not info['cover_error']:
                    image_data = get_image(info['cover_image'])
                    if image_data is not None:
                        data, ext = image_data
                        book_collection.save_cover(dataset.get_dataset_directory(), book.id, data, u"cover.jpg")
                    # end if
                    book.cover = info['cover_image']
                # end if

                # Get ISFDb cover image
                #book.covert_art = get_image(isfdb_info['cover'])
                book.cover_art = isfdb_info['cover']

                # Content
                book_collection.save_content(dataset.get_dataset_directory(), book.id, info['content'])
                #book.content = info['content']

                # Save collections
                if book.id % 10 == 0:
                    print(u"Saving collection")
                    book_collection.save(dataset.get_dataset_directory())
                    country_collection.save(dataset.get_dataset_directory())
                    year_collection.save(dataset.get_dataset_directory())
                # end if
                print(u"")
            # end if
        # end if

        # Space
        print(u"")
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
