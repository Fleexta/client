#  Copyright (c) 2025 Timofei Kirsanov
import json
import os
import warnings

import requests
import uuid
from PyQt6.QtGui import QImage, QPixmap

from client import api


class File:
    def __init__(self, path: str, token: str = None):
        if not (get_media(path) is None):
            self.data = get_media(path)
            return
        if token is None:
            self.data = requests.get(api.get_common(path)).content
        else:
            self.data = requests.get(api.get_common(path), headers={'Authorization': "Bearer " + token}).content
        write_media(path, self.data)

    def img(self):
        return self.data

    def json(self):
        return json.loads(self.data)


def get_media(name: str):
    items = {}
    with open("cache/cache", "r") as f:
        for item in f.readlines():
            key, value = map(str, item.strip().split(" ", maxsplit=1))
            items[key] = value
    if name in items.keys():
        return load_media(items[name])
    else:
        return None


def load_media(name: str):
    with open("cache/" + name, "rb") as f:
        return f.read()


def write_media(name: str, media):
    key = str(uuid.uuid4())
    with open("cache/cache", "a") as f:
        f.write(name + " " + key + "\n")
    with open("cache/" + key, "wb") as f:
        f.write(media)


def check():
    try:
        with open("cache/cache", "r") as f:
            return True
    except FileNotFoundError:
        warnings.warn("cache registration file not found", CacheWarning)
        return False


def init():
    os.makedirs("cache", exist_ok=True)
    with open("cache/cache", "w") as f:
        pass


class CacheWarning(Warning):
    pass
