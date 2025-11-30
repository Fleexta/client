#  Copyright (c) 2025 Timofei Kirsanov

from PyQt6.QtGui import QImage, QPixmap


def get(name: str):
    with open("res/" + name + ".png", "rb") as f:
        image = QImage()
        image.loadFromData(f.read())
        pixmap = QPixmap(image)
    return pixmap
