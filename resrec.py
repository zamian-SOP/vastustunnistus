import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="Give path to image as argument.")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
