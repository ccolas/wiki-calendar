import json
import itertools
from urllib.request import urlopen, Request
import random
from bs4 import BeautifulSoup
from PIL import Image

# from https://gist.github.com/genekogan/ebd77196e4bf0705db51f86431099e57

REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def get_soup(url, header):
    response = urlopen(Request(url, headers=header))
    return BeautifulSoup(response, 'html.parser')

def get_query_url(query):
    url = "https://www.google.com/search?q=%s&hl=en&source=lnms&tbm=isch&tbs=isz:l" % query
    return url
     # return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch&tbs=sur:fc,isz:l" % query # use this line to have images free of rights


def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})
    metadata_dicts = (json.loads(e.text) for e in image_elements)
    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
    return link_type_records

def new_extract_images_from_soup(soup):
    image_elements = soup.find_all("img")
    urls = [im['src'] for im in image_elements if 'encrypted-tbn0' in im['src']]
    urls = [bytes(url, 'ascii').decode('unicode-escape') for url in urls]
    urls = [bytes(url, 'ascii').decode('unicode-escape') for url in urls]  # need two decodings

def extract_images(query, num_images):
    url = get_query_url(query).encode('utf-8').decode('ascii', 'ignore')
    print(url)
    soup = get_soup(url, REQUEST_HEADER)
    link_type_records = extract_images_from_soup(soup)
    return itertools.islice(link_type_records, num_images)

def get_raw_image(url):
    req = Request(url, headers=REQUEST_HEADER)
    resp = urlopen(req)
    return resp.read()

def save_image(raw_image, image_type, save_directory, filename):
    extension = image_type if image_type else 'jpg'
    # file_name = uuid.uuid4().hex
    save_path = save_directory + filename
    with open(save_path, 'wb') as image_file:
        image_file.write(raw_image)

def download_images_to_dir(image, save_directory, filename):

        raw_image = get_raw_image(image[0])
        save_image(raw_image, image[1], save_directory, filename)


def get_google_image(query, save_directory, filename, shuffle_all=False, num_images=40):
    query = '+'.join(query.split())

    # randomise order of first 15, respecting the first 10
    try:
        images = extract_images(query, num_images)
        imgs = []
        # remove all images that are not jpeg
        n_imgs = 0
        for ind, item in enumerate(images):
            n_imgs += 1
            if item[1] in ['jpg','JPG','jpeg','JPEG']:
                imgs.append(item)
        n_images = len(imgs)
        if n_images == 0:
            print('Invalid image format in the first', n_imgs, 'images')
            raise IOError
        if shuffle_all:
            inds = list(range(n_images))
            random.shuffle(inds)
        else:
            if n_images > 10:
                first_10 = list(range(10))
                random.shuffle(first_10)
                inds_sup_10 = list(range(10,n_images))
                random.shuffle(inds_sup_10)
                inds = first_10 + inds_sup_10
            else:
                inds = list(range(n_images))
                random.shuffle(inds)
        imgs = [imgs[i] for i in inds]

    except:
        print('Error in image extraction')
        return True

    # try to download images until one successful download
    for i in range(n_images):
        try:
            download_images_to_dir(imgs[i], save_directory, filename)
            # try opening it again..
            save_path = save_directory + filename
            image = Image.open(save_path)
            print('Image downloaded successfully')
            return False
        except:
            print('Image downloading failed, try to download image '+str(i+1),'out of', str(n_images), 'possibilities.')
    print('Failed to download an image, changing keyword')
    return True




