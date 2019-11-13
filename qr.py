#!/usr/bin/env python3
import re
import pyzbar.pyzbar as zbar
import requests
from PIL import Image, ImageGrab
import argparse
from io import BytesIO


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url')

    args = parser.parse_args()
    return args


def is_url(url):
    return re.match(r'https?://', url) is not None


def get_image(url):
    if is_url(url):
        r = requests.get(url)
        r.raise_for_status()
        return Image.open(BytesIO(r.content))
    else:
        return Image.open(url)


def scan_qr(image):
    if isinstance(image, str):
        image = get_image(image)

    assert isinstance(image, Image.Image)

    gray = image.convert('L')

    return zbar.decode(gray)


def main():
    args = arg_parse()
    im = args.url
    if not im:
        im = ImageGrab.grabclipboard()

    print(scan_qr(im))


if __name__ == '__main__':
    main()