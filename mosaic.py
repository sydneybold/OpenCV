import numpy as np
import argparse
import cv2
import os
from os import listdir

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target_image", required = True, help = "Path to the target image")
    ap.add_argument("-s", "--source_images", required = True, help = "Path to the set of images")
    ap.add_argument("-ts", "--tile_size", type = int, default = 10, help = "Controls detail of mosaic")
    args = vars(ap.parse_args())
    return args
#------------------------------------------------------------------------------#
def get_tiles(folder, tile_size):
    tiles = []
    for filename in os.listdir(folder):
        image = cv2.imread(os.path.join(folder, filename))
        if image is not None:
            tile = process_tile(image, tile_size)
            tile_color = get_avg_color_of_tile(tile)
            tiles.append([tile, tile_color])

    return tiles

def process_tile(image, tile_size):
    (height, width) = image.shape[:2]
    min_dimension = min(width, height)
    cropped = image[(height-min_dimension)//2:(height+min_dimension)//2, (width-min_dimension)//2:(width+min_dimension)//2]
    resized = cv2.resize(cropped, (tile_size, tile_size), interpolation = cv2.INTER_AREA)
    return resized

def get_avg_color_of_tile(tile):
    avg_color_per_row = np.average(tile, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color
#------------------------------------------------------------------------------#
def process_target_image(target_image, tile_size):
    (height, width) = target_image.shape[:2]
    dim = ((width//tile_size) * tile_size, (height//tile_size) * tile_size)
    resized = cv2.resize(target_image, dim, interpolation = cv2.INTER_AREA)
    return resized
#------------------------------------------------------------------------------#
def get_mosaic_tiles(target_image, tiles, tile_size):
    pixel_and_tile = []
    (height, width) = target_image.shape[:2]
    for x in range(0, width-tile_size, tile_size):
        for y in range(0, height-tile_size, tile_size):
            avg_color = get_avg_color_of_pixel_bunch(target_image, tile_size, x, y)
            best_tile = get_best_tile(tiles, avg_color)
            pixel_and_tile.append([x, y, best_tile])

    return pixel_and_tile

def get_avg_color_of_pixel_bunch(target_image, tile_size, x, y):
    cropped = target_image[y:y+tile_size, x:x+tile_size]
    avg_color_per_row = np.average(cropped, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color

def get_best_tile(tiles, avg_color):
    min_diff = 765
    for i in range(len(tiles)):
        diff = get_tile_and_pixel_bunch_diff(tiles[i][1], avg_color, min_diff)
        if diff < min_diff:
            min_diff = diff
            min_index = i
    return tiles[min_index][0]

def get_tile_and_pixel_bunch_diff(tile_color, image_color, bail_out_value):
    diff = 0
    for i in range(len(tile_color)):
        diff += abs(tile_color[i] - image_color[i])
        if diff > bail_out_value:
            return round(diff, 4)
    return round(diff, 4)
#------------------------------------------------------------------------------#
def build_mosaic(target_image, mosaic_tiles, tile_size):
    canvas = np.zeros(target_image.shape, dtype=np.uint8)
    canvas.fill(255)
    for pixel in mosaic_tiles:
        x = pixel[0]
        y = pixel[1]
        canvas[y:y+tile_size, x:x+tile_size] = pixel[2]

    return canvas
#------------------------------------------------------------------------------#
def main():
    args = get_args()
    image = cv2.imread(args["target_image"])
    tile_size = args["tile_size"]

    tiles = get_tiles(args["source_images"], tile_size)
    target_image = process_target_image(image, tile_size)

    mosaic_tiles = get_mosaic_tiles(image, tiles, tile_size)
    mosaic = build_mosaic(image, mosaic_tiles, tile_size)
    cv2.imwrite("mosaic.jpg", mosaic)
    cv2.imshow("Mosaic", mosaic)
    cv2.waitKey(0)


main()
