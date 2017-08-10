# -*- coding: utf-8 -*-
#

import argparse
import logging

import download as dw

######################################################
#
# Functions
#
######################################################


######################################################
#
# Main
#
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - List items in an internet archive collection")

    # Argument
    parser.add_argument("--name", type=str, help="Collection's name", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logs
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    # AI collection
    collection = dw.ArchiveOrgCollection(args.name)

    # List items
    for item in collection:
        info = dw.ArchiveOrgBookInformation.get_item_information(item)
        print(info)
        isfdb_info = dw.ISFDbBookInformation.get_book_information(info['isfdb_link'])
        print(isfdb_info)
        print("")
        #exit()
    # end for
# end if
