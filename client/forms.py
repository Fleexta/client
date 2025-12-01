#  Copyright (c) 2025 Timofei Kirsanov

import requests
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMessageBox, QWidget

from client import api, translate
from client.activities import CreateChatActivity
from client.activities import NewUserActivity


def warn(parent, text):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    return_button = msg.exec()
    if return_button == QMessageBox.StandardButton.Ok:
        return


class CreateChat(QWidget, CreateChatActivity):
    def __init__(self, parent, token):
        super().__init__()
        self.setupUi(self)
        self.token = token
        self.parent = parent
        self.createChatName.setText("")
        self.chatCreate.clicked.connect(self.create_chat)

    def create_chat(self):
        chat_name = self.createChatName.text()
        chat_type = "chat"
        if self.chatType.currentText() == translate.get("chat.chat"):
            chat_type = "chat"
        elif self.chatType.currentText() == translate.get("chat.channel"):
            chat_type = "channel"
        data = {
            "name": chat_name,
            "types": chat_type
        }
        requests.post(api.get_common("/create"), json=data, headers={'Authorization': "Bearer " + self.token})
        self.parent.load_chats()


class NewUser(QWidget, NewUserActivity):
    def __init__(self, user_id, parent, token):
        super().__init__()
        self.token = token
        self.parent = parent
        self.user_id = user_id
        self.setupUi(self)

        avatar = requests.get(api.get_common(f"/get/user/avatar/{self.user_id}"))
        image = QImage()
        image.loadFromData(avatar.content)
        pixmap = QPixmap(image)
        self.avatar.setPixmap(pixmap)

        name = requests.get(api.get_common(f"/get/user/name/{self.user_id}"))
        self.username.setText(name.json()[str(user_id)])

        about = requests.get(api.get_common(f"/get/user/about/{self.user_id}"))
        self.about.setText(about.json()[str(user_id)])

        self.chatCreate.clicked.connect(self.create_chat)

    def create_chat(self):
        chat_id = requests.get(api.get_common(f"/c/{self.user_id}"), headers={'Authorization': "Bearer " + self.token})
        self.parent.load_chats()
        self.parent.current_chat = chat_id.json()["id"]
