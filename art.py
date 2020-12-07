import os
import json
import random
import urllib.request
import requests
from art_functions import *
from consts import *
from sklearn.cluster import KMeans
from twython import *

if __name__ == "__main__":
    # Pick a random work of art from Wikiart
    page = random.randint(2500, 2976)
    req = requests.get(f'{endpoint}?json=2&page={page}')
    res = json.loads(req.text)
    pick_one = random.randint(0, len(res['Paintings']) - 1)
    work = res['Paintings'][pick_one]

    # Parse details
    title = work['title']
    year = work['year']
    artist_name = work['artistName']
    image = image2 = work['image']
    print(title, year, artist_name, image)

    # Load image and convert to a list of pixels
    url = url_to_image(image)
    image = cv2.cvtColor(url, cv2.COLOR_BGR2RGB)
    reshape = image.reshape((image.shape[0] * image.shape[1], 3))

    # Find and display most dominant colors
    cluster = KMeans(n_clusters=6).fit(reshape)
    visualize, codes = visualize_colors(cluster, cluster.cluster_centers_)[0], \
                       visualize_colors(cluster, cluster.cluster_centers_)[1]
    visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
    cv2.imwrite("tweet_palette.jpg", visualize)

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    photo = open('tweet_palette.jpg', 'rb')
    response = twitter.upload_media(media=photo)
    get_id = twitter.update_status(status=f'"{title}", {artist_name} ({year})\n\n'
                                          f'Hexadecimal values:\n{", ".join(codes)}.',
                                   media_ids=[response['media_id']])['id']

    twitter = Twython(APP_KEY2, APP_SECRET2, OAUTH_TOKEN2, OAUTH_TOKEN_SECRET2)

    original = urllib.request.urlretrieve(image2, "tweet_original.jpg")

    with open('tweet_original.jpg', 'rb') as photo:
        response = twitter.upload_media(media=photo)

        print(twitter.update_status(status=f'@ArtPalettesBot Original artwork',
                                    in_reply_to_status_id=get_id,
                                    media_ids=[response['media_id']]))
