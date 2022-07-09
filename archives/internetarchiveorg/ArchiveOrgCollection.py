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

        # Get result
        self._item_pos = 0
        self._n_items = 0
        self._results = internetarchive.search_items('collection:{}'.format(self._collection_name))
        self._items = list()
        for result in self._results:
            self._items.append(result)
            self._n_items += 1
        # end for
    # end __init__

    ######################################################
    # Public
    ######################################################

    ######################################################
    # Override
    ######################################################

    # Get item
    def __getitem__(self, item):
        """
        Get item
        :param item:
        :return:
        """
        return self._items[item]
    # end __getitem__

    # Get iterator
    def __iter__(self):
        """
        Get iterator
        :return: An iterator for the collection
        """
        return self
    # end __iter__

    # Next element
    def next(self):
        """
        Next element
        :return:
        """
        if self._item_pos >= self._n_items:
            self._item_pos = 0
            raise StopIteration
        # end if
        self._item_pos += 1
        return internetarchive.get_item(self._items[self._item_pos-1][u'identifier'])
    # end next

    ######################################################
    # Private
    ######################################################

    ######################################################
    # Static
    ######################################################

# end
