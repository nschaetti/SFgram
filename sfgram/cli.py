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
import zipfile
import json

# Local
from sfgram.acquisition import download_archive_collection
from sfgram.preprocessing import extract_archive_pages
from sfgram.media import convert_jp2 as conv_jp2
from sfgram.media import convert_jp2_directory as conv_jp2_dir
from sfgram.media import load_sqlite_metadata as load_sql_met
from sfgram.media import load_xml_metadata as load_xml_met


@click.group('main')
@click.pass_context
def main(ctx):
    """
    Manage and analyse outputs of machine learning experiments
    :param ctx: Context
    """
    pass
# end main


# Read metadata file (SQLite or XML)
@main.command("read-metadata")
@click.option("-i", "--input-file", required=True, type=str, help="Input file containing metadata (sql3 or XML)")
def read_metadata(
        input_file: str
) -> None:
    r"""Read metadata file (SQLite or XML)

    :return:
    """
    if input_file[-6:] == "sqlite":
        print(load_sql_met(
            sqlite3_file=input_file
        ))
    elif input_file[-3:] == "xml":
        print(load_xml_met(
            xml_file=input_file
        ))
    else:
        raise Exception(f"Unknown file type (input: {input_file})")
    # end if
# end read_metadata


# Extract metadata
@main.command("extract-metadata")
@click.option("-i", "--input-file", required=True, type=str, help="Input XML file containing metadata (XML)")
@click.option("-o", "--output-file", required=True, type=str, help="Output JSON file containing metadata")
def extract_metadata(
        input_file: str,
        output_file: str
) -> None:
    r"""Extract metadata.

    :param input_file:
    :param output_file:
    :return:
    """
    # Load metadata from XML
    metadata = load_xml_met(
        xml_file=input_file
    )

    # Write JSON file
    with open(output_file, 'w') as out_file:
        json.dump(metadata, out_file, sort_keys=True, indent=4)
    # end with
# end extract_metadata


# Transform jpeg-2000 to PNG
@main.command("convert-jp2")
@click.option("-i", "--input-file", required=True, type=str, help="Input image file")
@click.option("-o", "--output-file", required=True, type=str, help="Output image file")
def convert_jp2(
        input_file: str,
        output_file: str
) -> None:
    r"""Transform jpeg-2000 to PNG.

    :param input_file: Input image file (jpeg2000 .jp2)
    :param output_file: Output PNG file.
    """
    conv_jp2(
        input_image=input_file,
        output_image=output_file
    )
# end jpeg2000_to_png


# Convert directory of jpeg-2000 images
@main.command("convert-jp2-directory")
@click.option("-i", "--input-directory", required=True, type=str, help="Input directory with JPEG-2000 images")
@click.option("--remove/--no-remove", default=False, is_flag=True)
def convert_jp2_directory(
        input_directory: str,
        remove: bool
) -> None:
    r"""Convert directory of jpeg-2000 images.

    :param remove:
    :param input_directory: Input directory with JPEG-2000 images.
    """
    conv_jp2_dir(
        input_directory=input_directory,
        remove=remove
    )
# end convert_jp2_directory


# Unpack image zip
@main.command("unpack-images-zip")
@click.option("-z", "--input-zip-file", required=True, type=str, help="Input zip containing jp2 image files")
@click.option("-o", "--output-directory", required=True, type=str, help="Output directory")
@click.option("--convert/--no-convert", default=True, is_flag=True)
@click.option("--remove/--no-remove", default=False, is_flag=True)
def unpack_images_zip(
        input_zip_file: str,
        output_directory: str,
        convert: bool,
        remove: bool
) -> None:
    r"""Unpack images ZIP file.

    :param output_directory:
    :param input_zip_file: Input zip containing jp2 image file
    :param convert: Convert JP2 files?
    :param remove: Remove JP2 files after conversion?
    """
    # Extract all image files
    with zipfile.ZipFile(input_zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_directory)
    # end with

    # Convert image
    if convert:
        conv_jp2_dir(
            input_directory=output_directory,
            remove=remove
        )
    # end if
# end unpack_images_zip


# Download a collection from archive.org
@main.command("extract-pages")
@click.option("-x", "--xml-file", required=True, type=str, help="Input text file")
@click.option("-o", "--output-dir", required=True, type=str, help="Output directory")
def extract_pages(
        # input_file: str,
        xml_file: str,
        output_dir: str
) -> None:
    extract_archive_pages(
        # input_file=input_file,
        xml_file=xml_file,
        output_dir=output_dir
    )
# end extract_pages


# Download a collection from archive.org
@main.command("download-collection")
@click.option("-o", "--output-dir", required=True, type=str, help="TODO")
@click.option("-c", "--collection-name", required=True, type=str, help="Collection's name to be updated")
@click.option("--checksum/--no-checksum", is_flag=True, default=True)
@click.option("-r", "--retries", type=int, default=5)
@click.option("--ignore-errors/--no-ignore-errors", default=False, is_flag=True)
@click.option("--on-the-fly/--no-on-the-fly", default=False, is_flag=True)
@click.option("--verbose/--no-vebose", default=False, is_flag=True)
@click.option("-s", "--sleep", type=int, default=2)
def download_collection(
        output_dir: str,
        collection_name: str,
        checksum: bool = True,
        retries: int = 5,
        ignore_errors: bool = False,
        on_the_fly: bool = False,
        verbose: bool = False,
        sleep: int = 2
) -> None:
    r"""Download a collection from archive.org.

    :param sleep:
    :param output_dir:
    :param collection_name:
    :param checksum:
    :param retries:
    :param ignore_errors:
    :param on_the_fly:
    :param verbose:
    :return:
    """
    download_archive_collection(
        output_dir=output_dir,
        collection_name=collection_name,
        checksum=checksum,
        retries=retries,
        ignore_errors=ignore_errors,
        on_the_fly=on_the_fly,
        verbose=verbose,
        sleep=sleep
    )
# end download_collection


# Main
if __name__ == '__main__':
    main()
# end if
