# -*- coding: utf-8 -*-
#

import numpy as np
import argparse
import logging
import pygame
import pygame.camera
import time
import Image
import pytesseract

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
    parser = argparse.ArgumentParser(description="SFgram - Acquire images from webcam and digitilize texts.")

    # Argument
    parser.add_argument("--image", type=str, help="Image to extract text from", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    parser.add_argument("--lang", type=str, help="Language", default="eng")
    args = parser.parse_args()

    im = Image.open(args.image)
    print(im)
    print(pytesseract.image_to_string(im))

    # Logs
    """logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="SFgram")

    pygame.camera.init()
    pygame.camera.list_cameras()
    cam = pygame.camera.Camera("/dev/video0", (640, 480))
    cam.start()
    time.sleep(0.1)
    img = cam.get_image()
    pygame.image.save(img, "pygame.jpg")
    cam.stop()"""

# end if
