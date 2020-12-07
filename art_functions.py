import numpy as np
import urllib
import cv2

def clamp(x):
    return max(0, min(int(x), 255))


def visualize_colors(cluster, centroids):
    # Credits: colordetect.color_detect
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
        cv2.rectangle(rect, (int(start), 0), (int(end), 628), \
                      color.astype("uint8").tolist(), -1)
        start = end
    return rect, hexcodes


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    getsize = tuple(image.shape[1::-1])
    while getsize[0] > 1000 or getsize[1] > 1000:
        image = cv2.resize(image, None, fx=0.5, fy=0.5)
        getsize = tuple(image.shape[1::-1])
        print("Resized to ", tuple(image.shape[1::-1]))
    return image