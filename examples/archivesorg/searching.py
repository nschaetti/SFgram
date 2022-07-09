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
import inspect
import internetarchive as ia


# Identifier
for item in ia.search_items('collection:nasa').iter_as_items():
    print(item)
    print(type(item))
    print(item.item_metadata['metadata'])
    print(inspect.getfile(item.__class__))
# end for

