#
# -*- coding: utf-8 -*-
#
# File : sfgram/acquisition/archiveorg/ArchiveOrgBookInformation.py
#
# This file is part of the SFGram distribution (https://github.com/nschaetti/SFgram).
# Copyright (c) 2022 Nils Schaetti.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Copyright Nils Schaetti, University of Neuchâtel <nils.schaetti@unine.ch>
# University of Geneva <nils.schaetti@unige.ch>, <n.schaetti@gmail.com>

# Imports
import click
from archives import internetarchiveorg as ia, dataset as ds, isfdb
from sfgram.acquisition import archiveorg as ao


@click.group('main')
@click.pass_context
def main(ctx):
    """
    Manage and analyse outputs of machine learning experiments
    :param ctx: Context
    """
    pass
# end main


# Update the archiveorg collection.
@main.command("update_archiveorg_collection")
@click.argument("output_dir", required=True, type=str, help="Output SFGram directory")
@click.argument("collection_name", required=True, type=str, help="Collection's name to be updated")
@click.argument("author_name", required=True, type=str, help="TODO")
@click.argument("country_name", required=True, type=str, help="TODO")
@click.pass_obj
def update_archiveorg_collection(
        output_dir: str,
        collection_name: str,
        author_name: str,
        country_name: str
):
    r"""Update the archiveorg collection.

    :param output_dir:
    :param collection_name:
    :param author_name:
    :param country_name:
    :return:
    """
    # Dataset
    dataset = ds.Dataset(output_dir)
    dataset.check_directories()

    # Load or create collections
    book_collection = ds.BookCollection.create(output_dir)
    country_collection = ds.CountryCollection.create(output_dir)
    year_collection = ds.YearCollection.create(output_dir)

    # Country
    if country_collection.get_by_name(country_name) is None:
        country = ds.Country(country_name=country_name)
    else:
        country = country_collection.get_by_name(country_name)
    # end if

    # AI collection
    collection = ao.ArchiveOrgCollection(collection_name)

    # Get collection information
    collection_info = ia.ArchiveOrgCollectionInformation.get_item_information(collection_name)

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
            book_title = args.author + u" " + isfdb_info['Date'].strftime("%B") + u" " + unicode(
                isfdb_info['Date'].year)

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
                # book.covert_art = get_image(isfdb_info['cover'])
                book.cover_art = isfdb_info['cover']

                # Content
                book_collection.save_content(dataset.get_dataset_directory(), book.id, info['content'])
                # book.content = info['content']

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
# end update_archiveorg_collection


# Main
if __name__ == '__main__':
    main()
# end if
