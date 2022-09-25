import numpy as np
import argparse
import cv2

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target_image", required = True, help = "Path to the target image")
    ap.add_argument("-s", "--source_images", required = True, help = "Path to the set of images")
    args = vars(ap.parse_args())
    return args

def main():
    args = get_args()

main()
