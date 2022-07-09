#
# -*- coding: utf-8 -*-
#
# File : sfgram/medias/images.py
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
import subprocess
import os


# Convert jpeg2000
def convert_jp2(
        input_image: str,
        output_image: str
) -> str:
    r"""Convert JPEG-2000.

    :param input_image:
    :param output_image:
    """
    # Image Magick command line
    cmd = f"convert {input_image} {output_image}"

    # Execute convert command
    subprocess.call(cmd, shell=True)
# end convert_jp2


# Convert JP2 directory
def convert_jp2_directory(
        input_directory: str,
        remove: bool
) -> None:
    r"""Convert directory of jpeg-2000 images.

    :param remove:
    :param input_directory: Input directory with JPEG-2000 images.
    """
    # List directory
    for file_name in os.listdir(input_directory):
        # Only fp2 filepath
        if file_name[-3:] == "jp2":
            # Full path
            fp2_file_path = os.path.join(input_directory, file_name)

            # Output file name
            output_file_name = file_name[:-3] + "png"

            # Output full file path
            output_file_path = os.path.join(input_directory, output_file_name)

            # Convert JP2
            print(f"Converting JP2 file {fp2_file_path} to {output_file_path}")
            convert_jp2(fp2_file_path, output_file_path)

            # Remove JP2?
            if remove:
                print(f"Removing file {fp2_file_path}")
                os.remove(fp2_file_path)
            # end if
        # end if
    # end for
# end convert_jp2_directory


