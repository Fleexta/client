#  Copyright (c) 2025 Timofei Kirsanov

import requests
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMessageBox, QWidget

from client import api, translate
from client.activities import CreateChatActivity, EditChatActivity, NewUserActivity


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

        username = requests.get(api.get_common(f"/get/user/username/{self.user_id}"))
        self.username.setText(username.json()[str(user_id)])

        name = requests.get(api.get_common(f"/get/user/name/{self.user_id}"))
        self.name.setText(name.json()[str(user_id)])

        about = requests.get(api.get_common(f"/get/user/about/{self.user_id}"))
        self.about.setText(about.json()[str(user_id)])

        self.chatCreate.clicked.connect(self.create_chat)

    def create_chat(self):
        chat_id = requests.get(api.get_common(f"/c/{self.user_id}"), headers={'Authorization': "Bearer " + self.token})
        self.parent.load_chats()
        self.parent.current_chat = chat_id.json()["id"]


class EditChat(QWidget, EditChatActivity):
    def __init__(self, chat_id, parent, token, app):
        super().__init__()
        self.token = token
        self.parent = parent
        self.chat_id = chat_id
        self.app = app
        self.setupUi(self)

        avatar = requests.get(api.get_common(f"/get/chat/avatar/{self.chat_id}"))
        image = QImage()
        image.loadFromData(avatar.content)
        pixmap = QPixmap(image)
        self.avatar.setPixmap(pixmap)

        name = requests.get(api.get_common(f"/get/chat/name/{self.chat_id}"))
        self.name.setText(name.json()[str(self.chat_id)])

        invite = requests.get(api.get_common(f"/get/chat/invite/{self.chat_id}"))
        self.invite.setText(invite.json()[str(self.chat_id)])

        members = requests.get(api.get_common(f"/get/chat/members/{self.chat_id}"))
        members_list = ""
        for member in members.json()[str(self.chat_id)]:
            members_list += str(member) + ", "
        self.members.setText(members_list)

        self.generateLink.clicked.connect(self.generate_link)
        self.copyLink.clicked.connect(self.copy_link)

    def generate_link(self):
        requests.post(api.get_common(f"/generate/invite/chat/{self.chat_id}"),
                      headers={'Authorization': "Bearer " + self.token})
        invite = requests.get(api.get_common(f"/get/chat/invite/{self.chat_id}"))
        self.invite.setText(invite.json()[str(self.chat_id)])

    def copy_link(self):
        clipboard = self.app.clipboard()
        clipboard.setText(api.get_common(f"/?invite={self.invite.text()}"))
