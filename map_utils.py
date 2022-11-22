import os
import sys
import time
from math import log, exp, tan, atan
import cv2
import numpy as np
from selenium import webdriver

import utils_draw_polygons

tau = 6.283185307179586

DEGREE = tau / 360

ZOOM_OFFSET = 0


def latlon2pixels(lat, lon, zoom):
    mx = lon
    my = log(tan((lat + tau / 4) / 2))
    res = 2 ** (zoom + ZOOM_OFFSET) / tau
    px = mx * res
    py = my * res
    return px, py


def pixels2latlon(px, py, zoom):
    res = 2 ** (zoom + ZOOM_OFFSET) / tau
    mx = px / res
    my = py / res
    lon = mx
    lat = 2 * atan(exp(my)) - tau / 4
    return lat, lon


def take_screenshot_of_map(map_name, output_name):
    #os.environ['MOZ_HEADLESS'] = '1'
    mapUrl = 'file://{0}/{1}'.format(os.getcwd(), map_name)
    driver = webdriver.Firefox()
    driver.get(mapUrl)
    time.sleep(0.2)
    driver.save_screenshot('outputs/' + output_name)
    driver.quit()


def find_min_max(polygon):
    max_x = 0
    min_x = sys.maxsize
    max_y = 0
    min_y = sys.maxsize

    for x, y in polygon:
        if x > max_x:
            max_x = x

        if y > max_y:
            max_y = y

        if x < min_x:
            min_x = x

        if y < min_y:
            min_y = y
    return min_x, min_y, max_x, max_y


def create_image_for_classification(original_image, image_with_poly, output_name):
    img_with_poly = cv2.imread("outputs/" + image_with_poly)
    img_org = cv2.imread("outputs/" + original_image)
    mask = cv2.inRange(img_with_poly, np.array([0, 0, 255]), np.array([0, 0, 255]))

    polygons = utils_draw_polygons.mask_to_polygons(mask)
    min_x, min_y, max_x, max_y = find_min_max(polygons[0])
    mask = mask // 255

    print(f"Größe: {max_x-min_x} {max_y-min_y}")

    red_channel = mask * img_org[:, :, 0]
    green_channel = mask * img_org[:, :, 1]
    blue_channel = mask * img_org[:, :, 2]

    merged = cv2.merge([red_channel, green_channel, blue_channel])

    height = max_x - min_x
    width = max_y-min_y
    if height > width:
        merged = merged[min_y:min_y+height, min_x:max_x]
    else:
        merged = merged[min_y:max_y, min_x:min_x+width]
    #
    # if height < width:
    #     merged = merged[min_y:min_y+height, min_x:max_x]
    # else:
    #     merged = merged[min_y:max_y, min_x:min_x+width]
    merged = cv2.resize(merged, (100, 100))
    cv2.imwrite("outputs/" + output_name, merged)
