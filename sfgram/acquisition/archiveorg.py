# -*- coding: utf-8 -*-
#
# File : core/download/ArchiveOrgConnector.py
#
# This file is part of pySpeeches.  pySpeeches is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Nils Schaetti, University of Neuchâtel <nils.schaetti@unine.ch>
# <nils.schaetti@unige.ch>, <n.schaetti@gmail.com>


# Imports
import internetarchive as ia


# Download a collection from archive.org.
import requests


def download_archive_collection(
        output_dir: str,
        collection_name: str,
        checksum: bool = True,
        retries: int = 5,
        ignore_errors: bool = False,
        on_the_fly: bool = False,
        verbose: bool = False,
        sleep: int = 2
):
    r"""Download a collection from archive.org.

    :param output_dir:
    :param collection_name:
    :param checksum:
    :param retries:
    :param ignore_errors:
    :param on_the_fly:
    :param verbose:
    :param sleep:
    :return:
    """
    # For all items in the collection.
    for item in ia.search_items(f'collection:{collection_name}').iter_as_items():
        # Item identifier
        item_identifier = item.item_metadata['metadata']['identifier']

        # Log
        print(f">>> Downloading archive.org item {item_identifier}")

        # Try downloading
        n_tries = 0
        downloaded = False
        while not downloaded and n_tries < retries:
            try:
                # Download the item to the target directory
                ia.download(
                    identifier=item_identifier,
                    destdir=output_dir,
                    checksum=checksum,
                    retries=retries,
                    on_the_fly=on_the_fly,
                    ignore_errors=ignore_errors,
                    verbose=verbose
                )

                # Downloaded
                downloaded = True
            except requests.exceptions.ConnectionError as exc:
                print(f"Error while downloading {item_identifier}: {exc}, retrying")
                n_tries += 1
                pass
            # end try
        # end while

        # Log
        print(f"<<< {item_identifier} downloaded")
        print("")
    # end for
# end download_collection

