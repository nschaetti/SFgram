# -*- coding: utf-8 -*-
#

import argparse
import logging
from archives import dataset as ds
from archives.dataset import Country

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
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name=u"SFGram")

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)

    # Load or create collections
    book_collection = ds.BookCollection.create(args.dataset_dir)
    country_collection = ds.CountryCollection.create(args.dataset_dir)
    year_collection = ds.YearCollection.create(args.dataset_dir)

    # Show all countries
    for country in country_collection.get_countries():
        print(country.name)
    # end for

    # For each book
    for book in book_collection.get_books():
        # Load country
        country = country_collection.get_by_id(book.country)

        # Load author
        author = book_collection.get_author_by_id(book.author)

        # If country unknown
        if country.name == "Unknown":
            # Author's country
            author_country = None
            if author.country != -1:
                author_country = country_collection.get_by_id(author.country)
            # end if

            # If we don't know the author's country
            if author_country is None:
                # Ask true country
                print(u"{} {} {}".format(book.title, author.name, book.year))
                new_country_name = raw_input(u"New country: ")

                # Get country
                new_country_obj = country_collection.get_by_name(new_country_name)

                # If doesn't exists
                if new_country_obj is None:
                    new_country_obj = Country(new_country_name)
                    country_collection.add(new_country_obj)
                # end if

                # Set country
                book.country = new_country_obj.id

                # Add book to new country
                new_country_obj.books.append(book.id)
                new_country_obj.n_books += 1

                # Remove from previous country
                country.books.remove(book.id)
                country.n_books -= 1

                # Set author's country
                author.country = new_country_obj.id

                # Continue, save, quit?
                next_action = raw_input(u"Continue (c or nothing)? Save(s)? Save and quit(q)?").lower()

                # Execute
                if next_action == 'c' or next_action == '':
                    pass
                elif next_action == 'q':
                    # Save collections
                    book_collection.save(dataset.get_dataset_directory())
                    country_collection.save(dataset.get_dataset_directory())
                    year_collection.save(dataset.get_dataset_directory())
                    exit()
                elif next_action == 's':
                    # Save collections
                    book_collection.save(dataset.get_dataset_directory())
                    country_collection.save(dataset.get_dataset_directory())
                    year_collection.save(dataset.get_dataset_directory())
                # end if
            elif author_country.name != "Unknown":
                # Set country
                book.country = author_country.id

                # Add book to new country
                author_country.books.append(book.id)
                author_country.n_books += 1

                # Remove from previous country
                country.books.remove(book.id)
                country.n_books -= 1
            # end if
        elif author.country == -1:
            # Set author's country
            author.country = country.id
        # end if
    # end for

    # Save collections
    book_collection.save(dataset.get_dataset_directory())
    country_collection.save(dataset.get_dataset_directory())
    year_collection.save(dataset.get_dataset_directory())

# end if
