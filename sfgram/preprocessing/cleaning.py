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
import os
import lxml
import xml.etree.ElementTree as ET


# Extract pages
def extract_archive_pages(
        # input_file: str,
        xml_file: str,
        output_dir: str
):
    r"""Extract pages from text file and XML OCR description.

    :param input_file:
    :param xml_file:
    :param output_dir:
    :return:
    """
    # Parse XML doc
    tree = ET.parse(xml_file)

    # Get the root of the document
    root = tree.getroot()

    # Get body of the document
    body = root.find(".//BODY")

    # Go through each page, paragraph, line and words
    for page_number, obj in enumerate(body.iter('OBJECT')):
        # Page height
        page_height = float(obj.attrib['height'])

        # Load a new file
        with open(os.path.join(output_dir, "page_{:03d}".format(page_number)), 'w') as page_file:
            # For each page
            for page_column in obj.iter('PAGECOLUMN'):
                for paragraph in page_column.iter('PARAGRAPH'):
                    # Paragraph text
                    para_text = ""

                    # For each line
                    for line in paragraph.iter('LINE'):
                        for word in line.iter('WORD'):
                            # Text size
                            text_bound = word.attrib['coords'].split(',')
                            text_height = (float(text_bound[2]) - float(text_bound[0])) / page_height

                            # Add to text
                            para_text += word.text + " "
                        # end for
                    # end for

                    # Write paragraph
                    page_file.write(para_text[:-1] + "\n")
                    page_file.write("\n")
                # end for
                page_file.write("\n")
            # end for
        # end with
    # end for
# end extract_pages
