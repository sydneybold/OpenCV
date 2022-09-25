import numpy as np
import argparse
import cv2
import os
from os import listdir

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target_image", required = True, help = "Path to the target image")
    ap.add_argument("-s", "--source_images", required = True, help = "Path to the set of images")
    args = vars(ap.parse_args())
    return args

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        image = cv2.imread(os.path.join(folder, filename))
        if image is not None:
            images.append(image)
    return images

def main():
    args = get_args()
    source_images = load_images_from_folder(args["source_images"])


main()
