#  Copyright (c) 2025 Timofei Kirsanov
import webbrowser
from urllib.parse import urlparse

import markdown
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QFileDialog, QToolButton, QMessageBox

from client import settings, api, translate
from client.res import resource


class MediaLabel(QLabel):
    def __init__(self, filename="", media="", parent=None):
        super().__init__(parent)
        self.media = media
        self.filename = filename
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QLabel {
                background-color: """ + settings.get_theme().BACKGROUND_COLOR_BACK + """;
                border-radius: 8px;
                padding: 8px;
                border: 1px solid #363646;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        pixmap = resource.get("file")
        self.icon_label = QLabel()
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setFixedSize(48, 52)
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: """ + settings.get_theme().BACKGROUND_COLOR_FRONT + """;
                border-radius: 4px;
            }
        """)

        self.filename_label = QLabel(self.filename)
        self.filename_label.setStyleSheet("""
            QLabel {
                color: """ + settings.get_theme().TEXT + """;
                font-size: 9pt;
                padding: 0 4px;
            }
        """)
        self.filename_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.filename_label.setWordWrap(True)

        self.download_icon = QToolButton()
        self.download_icon.setFixedSize(32, 32)
        self.download_icon.setStyleSheet("""
            QToolButton {
                background-color: """ + settings.get_theme().BACKGROUND_COLOR_DOWNLOAD + """;
                border-radius: 10px;
                color: """ + settings.get_theme().TEXT_MAIN + """;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
            }
        """)
        self.download_icon.setText("↓")

        self.download_icon.clicked.connect(self.on_download_clicked)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.filename_label, 1)
        layout.addWidget(self.download_icon)

        container = QWidget()
        container.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

        self.setMinimumHeight(88)

    def set_filename(self, filename):
        self.filename_label.setText(filename)

    def on_download_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", self.filename, "Все файлы (*)")
        if file_name:
            response = requests.get(api.get_common(f"/media/{self.media}"))
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    for chunk in response.iter_content(8192):
                        f.write(chunk)


class CircularLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(26, 26)
        self._pixmap = None

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        if self._pixmap:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            path = QPainterPath()
            path.addEllipse(0, 0, self.width(), self.height())
            painter.setClipPath(path)

            painter.drawPixmap(0, 0, self.width(), self.height(),
                               self._pixmap.scaled(self.size(),
                                                   Qt.AspectRatioMode.IgnoreAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation))

            painter.setPen(QPen(QColor("#363646"), 1.3))
            painter.drawEllipse(0, 0, self.width() - 1, self.height() - 1)
        else:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.fillRect(self.rect(), QColor("#18181a"))
            painter.setPen(QPen(QColor("#363646"), 1.3))
            painter.drawEllipse(0, 0, self.width() - 1, self.height() - 1)


class ChatMessageWidget(QWidget):
    def __init__(self, id=0, author_name="", message_text="", media=b"", time_str="", parent=None):
        super().__init__(parent)
        self.id = id
        self.setup_ui(author_name, message_text, media, time_str)

    def setup_ui(self, author_name, message_text, media, time_str):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(7)

        self.avatar_label = CircularLabel()
        self.avatar_label.setText("A")
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setStyleSheet("""
            QLabel {
                border-radius: 13px;
                border: 1.3px solid #363646;
                background: #18181a;
                color: """ + settings.get_theme().TEXT + """;
                font-size: 10px;
            }
        """)

        message_container = QFrame()
        message_container.setObjectName("messageContainer")
        message_container.setStyleSheet("""
            QFrame#messageContainer {
                border-radius: 16px;
                background-color: """ + settings.get_theme().BACKGROUND_COLOR_FRAME + """;
                border: none;
            }
        """)

        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(13, 4, 13, 4)
        message_layout.setSpacing(1)

        self.name_label = QLabel(author_name)
        self.name_label.setStyleSheet("""
            QLabel {
                color: """ + settings.get_theme().TEXT_MAIN + """;
                font-size: 9.5pt;
                font-weight: 500;
                margin-bottom: 1px;
            }
        """)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.name_label.setMaximumWidth(280)
        self.name_label.setWordWrap(True)

        html_message = markdown.markdown(message_text)
        self.message_label = QLabel(html_message)
        self.message_label.setStyleSheet("""
            QLabel {
                color: """ + settings.get_theme().TEXT + """;
                font-size: 9.5pt;
                line-height: 1.25;
            }
        """)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.message_label.setMaximumWidth(280)
        self.message_label.setWordWrap(True)
        self.message_label.setOpenExternalLinks(False)
        self.message_label.linkActivated.connect(self.on_link_clicked)

        if media:
            response = requests.get(api.get_common(f"/media/{media}"))
            filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
            self.media_label = MediaLabel(filename, media)

        self.time_label = QLabel(time_str)
        self.time_label.setStyleSheet("""
            QLabel {
                color: """ + settings.get_theme().TIME_COLOR + """;
                font-size: 7pt;
                letter-spacing: 0.12px;
            }
        """)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        message_layout.addWidget(self.name_label)
        message_layout.addWidget(self.message_label)
        if media:
            message_layout.addWidget(self.media_label)
        message_layout.addWidget(self.time_label)
        message_container.setLayout(message_layout)

        main_layout.addWidget(self.avatar_label)
        main_layout.addWidget(message_container, 1)
        self.setLayout(main_layout)

    def on_link_clicked(self, link):
        link_form = urlparse(link)
        if link_form.scheme == "https" or link_form.scheme == "http":
            if link_form.netloc == api.NETLOC:
                reply = QMessageBox.question(self.parent(),
                                             translate.get("web.link.title.internal"),
                                             translate.get("web.link.text.internal", (link, )),
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    webbrowser.open(link)
            else:
                reply = QMessageBox.question(self.parent(),
                                             translate.get("web.link.title.external"),
                                             translate.get("web.link.text.external", (link, )),
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    webbrowser.open(link)
