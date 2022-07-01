# -*- coding: utf-8 -*-
#
# File : core/download/__init__.py
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
from .ArchiveOrgBookInformation import ArchiveOrgBookInformation
from .ArchiveOrgCollection import ArchiveOrgCollection
from .ArchiveOrgCollectionInformation import ArchiveOrgCollectionInformation
from .ArchiveOrgConnector import ArchiveOrgConnector

# ALL
__all__ = [
    "ArchiveOrgBookInformation", "ArchiveOrgCollection", "ArchiveOrgCollectionInformation", "ArchiveOrgConnector"
]
