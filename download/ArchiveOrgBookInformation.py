# -*- coding: utf-8 -*-
#
# File : core/download/ArchiveOrgBookInformation.py
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

import internetarchive
import logging


# Extract book information from arcive.org
class ArchiveOrgBookInformation(object):
    """
    Extract book information from arcive.org
    """

    ####################################################
    # Static
    ####################################################

    @staticmethod
    def get_book_information(item_name):
        """
        Get the book information.
        :param item_name: Archive item's name
        :return: Item object.
        """
        internetarchive.get_item(item_name)
    # end get_book_information

# end
