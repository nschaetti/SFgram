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

import logging
from dateutil.parser import parse
import time
import internetarchive


# Collection for archive.org
class ArchiveOrgCollection(object):
    """
    Collection for archive.org
    """

    # Constructor
    def __init__(self, collection_name):
        # Properties
        self._collection_name = collection_name

        # Search on archive.org
        self._results = internetarchive.search_items('collection:{}'.format(collection_name))
    # end __init__

    ######################################################
    # Public
    ######################################################

    ######################################################
    # Override
    ######################################################

    # Get iterator
    def __iter__(self):
        """
        Get iterator
        :return: An iterator for the collection
        """
        return self._results
    # end __iter__

    ######################################################
    # Private
    ######################################################

    ######################################################
    # Static
    ######################################################

# end
