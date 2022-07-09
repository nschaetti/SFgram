#
# -*- coding: utf-8 -*-
#
# File : sfgram/media/meta.py
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

# Import
from typing import Dict
import sqlite3
import xml.etree.ElementTree as ET


# Load meta-data from sqlite3
def load_sqlite_metadata(
        sqlite3_file: str
) -> None:
    r"""Load meta-data from sqlite3.

    :param sqlite3_file: Path to the SQLite file.
    :return:
    """
    # Load DB
    meta_db = sqlite3.connect(sqlite3_file)

    cursorObj = meta_db.cursor()
    cursorObj.execute('SELECT * from s3api_per_key_metadata')
    for row in cursorObj.fetchall():
        print(row)
    # end for
# end load_sqlite_metadata


# Read metadata from XML file
def load_xml_metadata(
        xml_file: str
) -> Dict:
    r"""Read metadata from XML file.

    :param xml_file: Input XML file containing metadata.
    :return:
    """
    # Parse XML doc
    tree = ET.parse(xml_file)

    # Get the root of the document
    root = tree.getroot()

    # Metadata directory
    metadata = dict()

    # Iterate over metadata
    for obj in root.iter():
        if obj.tag != "metadata":
            if obj.tag not in metadata:
                metadata[obj.tag] = obj.text
            else:
                if type(metadata[obj.tag]) is list:
                    metadata[obj.tag].append(obj.text)
                else:
                    metadata[obj.tag] = [metadata[obj.tag]]
                # end if
            # end if
        # end if
    # end for

    return metadata
# end load_xml_metadata
