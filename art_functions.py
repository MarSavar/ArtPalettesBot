import numpy as np
import urllib
import cv2
import random
import requests
import json
from consts import *


def clamp(x):
    return max(0, min(int(x), 255))


def get_random_work():
    """
    Select a random work of art from Wikiart.
    Randint(x, y) selects a random page from the API.
    """
    page = random.randint(2500, 2976)
    req = requests.get(f'{endpoint}?json=2&page={page}')
    res = json.loads(req.text)
    pick_one = random.randint(0, len(res['Paintings']) - 1)
    return res['Paintings'][pick_one]


def parse_details(work):
    """
    Take a work of art in JSON format as a parameter and parse keys and values.
    """
    title = work['title']
    artist_name = work['artistName']
    year = work['year']
    url = work['image']

    print(title, artist_name, year, url)

    return {
        'title': title,
        'artist name': artist_name,
        'year': year,
        'url': url
    }


def visualise_colours(cluster, centroids):
    """
    Get the top six dominant colours and determine the width of each rectangle.
    Credits: colordetect.color_detect
    """
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins=labels)
    hist = hist.astype("float")
    hist /= hist.sum()
    rect = np.zeros((628, 628, 3), dtype=np.uint8)
    colors = [(percent, color) for (percent, color) in zip(hist, centroids)]
    start = 0

    hexcodes = []
    for (percent, color) in colors:
        hexcodes.append(f"{clamp(color[0]):02x}{clamp(color[1]):02x}{clamp(color[2]):02x}".upper())
        end = start + (percent * 628)
        cv2.rectangle(rect, (int(start), 0), (int(end), 628), color.astype("uint8").tolist(), -1)
        start = end
    return rect, hexcodes


def url_to_image(url):
    """
    Convert url to image and continuoisly resize it if either the width or the height are greater than 1000.
    """
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    getsize = tuple(image.shape[1::-1])
    while getsize[0] > 1000 or getsize[1] > 1000:
        image = cv2.resize(image, None, fx=0.5, fy=0.5)
        getsize = tuple(image.shape[1::-1])
        print(f"Resized to {tuple(image.shape[1::-1])}")
    return image
