# -*- coding: utf-8 -*-
#

import argparse
import logging
import os
import wikipediaorg as wp
import dataset as ds
import goodreadscom as gr
import gutenberg as gb
import tools

######################################################
# Functions
#######################################################


######################################################
# Main
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Update the SFGram book dataset")

    # Argument
    parser.add_argument("--dataset-dir", type=str, help="Dataset directory", required=True)
    args = parser.parse_args()

    # Dataset
    dataset = ds.Dataset(args.dataset_dir)
    dataset.check_directories()

    # Covers directory
    covers_path = os.path.join(dataset.get_dataset_directory(), "book-covers")

    # For each image
    for filename in os.listdir(covers_path):
        # Image path
        image_path = os.path.join(covers_path, filename)

        # If not image
        if "bcc042a9c91a29c1d680899eff700a03.png" in image_path:
            os.remove(image_path)
        # end if
    # end for
# end if
