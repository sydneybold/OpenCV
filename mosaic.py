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

def process_tiles(tiles):
    for i in range(len(tiles)):
        image = tiles[i]
        width = image.shape[1]
        height = image.shape[0]
        min_dimension = min(width, height)
        cropped = image[(height-min_dimension)//2:(height+min_dimension)//2, (width-min_dimension)//2:(width+min_dimension)//2]
        resized = cv2.resize(cropped, (50, 50), interpolation = cv2.INTER_AREA)
        tiles[i] = resized
    return tiles

def get_avg_color_of_each_tile(tiles):
    tile_colors = []
    for image in tiles:
        avg_color_per_row = np.average(image, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        tile_colors.append(avg_color)
    return tile_colors

def main():
    args = get_args()
    source_images = load_images_from_folder(args["source_images"])
    tiles = process_tiles(source_images)
    title_colors = get_avg_color_of_each_tile(tiles)


main()
