# -*- coding: utf-8 -*-
#
# File : core/download/ArchiveOrgBookInformation.py
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


# URLs
ARCHIVEORG_ITEM_URL = "https://archive.org/details/"
ARCHIVEORG_COVER_URL = "https://{}/BookReader/BookReaderImages.php?zip={}/{}_jp2.zip" \
                       "&file={}_jp2/{}_0000.jp2&scale=0&rotate=0"
ARCHIVEORG_TEXT_URL = "https://archive.org/stream/{}/{}_djvu.txt"

# Error messages
ERROR_RETRIEVE = "HTTP error trying to retrieve {} : {}"

# Fatal messages
FATAL_HTTP_ERROR_RETRIEVE = "Fatal HTTP error trying to retrieve {}"


