import datetime
import json

import requests
from PyQt6.QtCore import Qt, QTimer, QPoint, QThread
from PyQt6.QtGui import QPixmap, QImage, QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QLabel, QWidget, QVBoxLayout, \
    QSizePolicy, QMenu, QFileDialog

from client import api, settings, translate, Action, forms
from client.activities import MainActivity
from client.api import SseWorker
from client.chat import ChatMessageWidget
from client.style import Themes


class Main(QMainWindow, MainActivity):
    def __init__(self, app, token, id):
        super().__init__()
        self.setupUi(self)
        self.token = token
        self.id = id
        self.app = app
        self.chatInfo.setVisible(False)
        self.chat.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.current_chat = 0
        self.chats_dict = {}
        self.current_file = b""
        self.sendButton.clicked.connect(self.send_msg)
        self.settings.clicked.connect(self.open_settings)
        self.createChatButton.clicked.connect(self.open_create_widget)
        self.uploadButton.clicked.connect(self.upload_file)
        self.searchButton.clicked.connect(self.search_user)
        self.editButton.clicked.connect(self.edit_chat)
        self.callButton.clicked.connect(self.call)

        self.chats.clicked.connect(self.refresh)

        self.thread = None
        self.worker = None

        self.settings_window = None

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.refresh)
        # self.timer.setInterval(1000)
        # self.timer.start()

    def show_context_menu(self, pos: QPoint):
        global_pos = self.sender().mapToGlobal(pos)
        menu = QMenu(self)

        action1 = QAction(translate.get("chat.context.reply"), self)
        action1.setWhatsThis(Action.REPLY)
        menu.addAction(action1)

        if self.find_msg(self.sender().id)["author"] == id:
            action0 = QAction(translate.get("chat.context.edit"), self)
            action0.setWhatsThis(Action.EDIT)
            menu.addAction(action0)

        action2 = QAction(translate.get("chat.context.copy"), self)
        action2.setWhatsThis(Action.COPY)
        menu.addAction(action2)

        action3 = QAction(translate.get("chat.context.pin"), self)
        action3.setWhatsThis(Action.PIN)
        menu.addAction(action3)

        action4 = QAction(translate.get("chat.context.forward"), self)
        action4.setWhatsThis(Action.FORWARD)
        menu.addAction(action4)

        action5 = QAction(translate.get("chat.context.copy_link"), self)
        action5.setWhatsThis(Action.COPY_LINK)
        menu.addAction(action5)

        menu.addSeparator()

        action6 = QAction(translate.get("chat.context.delete"), self)
        action6.setWhatsThis(Action.DELETE)
        menu.addAction(action6)

        action = menu.exec(global_pos)
        if action is None:
            return
        match action.whatsThis():
            case Action.REPLY:
                print(action.whatsThis(), self.sender().id)
                return
            case Action.COPY:
                clipboard = self.app.clipboard()
                clipboard.setText(self.find_msg(self.sender().id)["message"])
                return
            case Action.PIN:
                print(action.whatsThis(), self.sender().id)
                return
            case Action.FORWARD:
                print(action.whatsThis(), self.sender().id)
                return
            case Action.COPY_LINK:
                clipboard = self.app.clipboard()
                clipboard.setText(api.get_common(f"/c/{self.current_chat}/{self.sender().id}"))
                return
            case Action.EDIT:
                data = {"message": self.message.text()}
                x = requests.post(api.get_common(f"/c/{self.current_chat}/{self.sender().id}/edit"),
                                  json=data, headers={'Authorization': "Bearer " + self.token})
                if x:
                    self.message.setText("")
                return
            case Action.DELETE:
                requests.post(api.get_common(f"/c/{self.current_chat}/{self.sender().id}/delete"),
                              headers={'Authorization': "Bearer " + self.token})
                return

    def find_msg(self, id):
        for msg in self.messages:
            if msg["id"] == id:
                return msg

    def load_chats(self):
        self.chats.clear()
        self.chats_dict = api.get_my_chats(self.token)
        self.chats_dict = json.loads(self.chats_dict)
        for chat_name in self.chats_dict.keys():
            response = requests.get(api.get_common(f"/get/chat/avatar/{self.chats_dict[chat_name]}"))
            image = QImage()
            image.loadFromData(response.content)
            pixmap = QPixmap(image)
            icon = QIcon(pixmap)
            item = QListWidgetItem(icon, chat_name)
            self.chats.addItem(item)

    def clear_chat_layout(self):
        while self.messages_layout.count():
            item = self.messages_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def refresh(self):
        if not self.token:
            return
        if self.chats.currentItem() is None:
            self.clear_chat_layout()
            message_widget = QLabel(translate.get("chat.text.choice"))
            message_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            message_widget.setStyleSheet("""
                QLabel {
                    color: """ + settings.get_theme().TEXT_MAIN + """;
                    font-size: 12pt;
                }
            """)
            self.messages_layout.addWidget(message_widget)
            return

        self.current_chat = self.chats_dict.get(self.chats.currentItem().text(), 0)

        self.thread = QThread()
        self.worker = SseWorker(f"/c/{self.current_chat}", self.token)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.data_received.connect(self.parse_sse_data)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def parse_sse_data(self, in_data):
        line_data, status = in_data
        if line_data.startswith('data:'):
            data_str = line_data[len('data:'):].strip()
            try:
                event_data = json.loads(data_str)
                data = {"type": 'json', "data": event_data, "raw_line": line_data}
            except json.JSONDecodeError:
                data = {"type": "text", "data": data_str, "raw_line": line_data}
        else:
            data = {"type": "other", "data": line_data, "raw_line": line_data}
        if data["type"] == "json":
            self.render_messages(data["data"], status)

    def render_messages(self, x, status):
        if status == 403:
            self.clear_chat_layout()

            error_container = QWidget()
            error_layout = QVBoxLayout()

            error_title = QLabel(translate.get("chat.error.forbidden"))
            error_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_title.setStyleSheet("""
                            QLabel {
                                color: """ + settings.get_theme().TEXT_MAIN + """;
                                font-size: 12pt;
                            }
                        """)

            error_layout.addWidget(error_title)
            error_container.setLayout(error_layout)

            self.messages_layout.addWidget(error_container)
            return
        elif status == 404:
            self.clear_chat_layout()

            error_container = QWidget()
            error_layout = QVBoxLayout()

            error_title = QLabel(translate.get("chat.error.not_found"))
            error_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_title.setStyleSheet("""
                            QLabel {
                                color: """ + settings.get_theme().TEXT_MAIN + """;
                                font-size: 12pt;
                            }
                        """)

            error_layout.addWidget(error_title)
            error_container.setLayout(error_layout)

            self.messages_layout.addWidget(error_container)
            return
        elif status != 200:
            self.clear_chat_layout()

            error_container = QWidget()
            error_layout = QVBoxLayout()

            error_title = QLabel(translate.get("chat.error.troubles"))
            error_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_title.setStyleSheet("""
                QLabel {
                    color: """ + settings.get_theme().TEXT_MAIN + """;
                    font-size: 12pt;
                }
            """)

            error_status = QLabel(f"HTTPException({status})")
            error_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_status.setStyleSheet("""
                QLabel {
                    color: """ + Themes.COMMON.ERROR_COLOR + """;
                    font-size: 10pt;
                }
            """)

            error_text = QLabel(translate.get("chat.error.unexpected", (api.SUPPORT_URL,)))
            error_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            error_text.setOpenExternalLinks(True)
            error_text.setStyleSheet("""
                QLabel {
                    color: """ + settings.get_theme().TEXT_SUPPORT + """;
                    font-size: 9pt;
                }
            """)

            error_layout.addWidget(error_title)
            error_layout.addWidget(error_status)
            error_layout.addWidget(error_text)
            error_container.setLayout(error_layout)

            self.messages_layout.addWidget(error_container)
            return

        self.chatInfo.setVisible(True)
        self.chatName.setText(self.chats.currentItem().text())

        self.clear_chat_layout()

        QWidget().setLayout(self.messages_layout)
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_layout.setSpacing(10)

        try:
            self.messages = x
            if len(self.messages) == 0:
                self.clear_chat_layout()

                empty_container = QWidget()
                empty_layout = QVBoxLayout()

                empty_title = QLabel(translate.get("chat.text.empty"))
                empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                empty_title.setStyleSheet("""
                    QLabel {
                        color: """ + settings.get_theme().TEXT_MAIN + """;
                        font-size: 12pt;
                    }
                """)

                empty_text = QLabel(translate.get("chat.text.empty.force"))
                empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
                empty_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                empty_text.setOpenExternalLinks(True)
                empty_text.setStyleSheet("""
                    QLabel {
                        color: """ + settings.get_theme().TEXT_SUPPORT + """;
                        font-size: 9pt;
                    }
                """)

                empty_layout.addWidget(empty_title)
                empty_layout.addWidget(empty_text)
                empty_container.setLayout(empty_layout)

                self.messages_layout.addWidget(empty_container)
                return
            for msg in self.messages:
                iso_string = msg["time"]
                dt_object = datetime.datetime.fromisoformat(iso_string)
                author = requests.get(api.get_common(f"/get/user/name/{msg['author']}"))

                message_widget = ChatMessageWidget(
                    id=msg["id"],
                    author_name=author.json()[str(msg["author"])],
                    message_text=msg["message"],
                    media=msg["media"],
                    time_str=dt_object.strftime(settings.format)
                )

                response = requests.get(api.get_common(f"/get/user/avatar/{msg['author']}"))
                image = QImage()
                image.loadFromData(response.content)
                pixmap = QPixmap(image)
                message_widget.avatar_label.setPixmap(pixmap)

                message_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
                message_widget.setMaximumWidth(int(self.width() * 0.5))

                message_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                message_widget.customContextMenuRequested.connect(self.show_context_menu)

                self.messages_layout.addWidget(message_widget)
            self.messages_container.setMinimumWidth(self.chat.viewport().width())
        except Exception as e:
            self.clear_chat_layout()
            error_widget = QLabel(translate.get("chat.error.presentation", (str(e),)))
            error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_widget.setStyleSheet("""
                QLabel {
                    color: """ + Themes.COMMON.ERROR_COLOR + """;
                    font-size: 10pt;
                }
            """)
            self.messages_layout.addWidget(error_widget)

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(2000)
        event.accept()

    def send_msg(self):
        if self.current_file == b"":
            data = {"message": self.message.text()}
            x = api.send_msg(data, self.current_chat, self.token)
            if x:
                self.message.setText("")
        else:
            response = requests.post(api.get_common("/upload/media"), files=self.current_file,
                                     headers={'Authorization': "Bearer " + self.token})
            if response.status_code == 200:
                data = {"message": self.message.text(), "media": response.json()["upload"]}
                x = api.send_msg(data, self.current_chat, self.token)
                if x:
                    self.message.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.refresh()
        if event.key() == Qt.Key.Key_W:
            self.load_chats()

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = settings.SettingsWindow(self.app, self.refresh)
        self.settings_window.show()

    def open_create_widget(self):
        self.create_chat = forms.CreateChat(self, self.token)
        self.create_chat.show()

    def upload_file(self):
        file_name = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '',
            'Изображение (*.jpg);;Изображение (*.png);;Все файлы (*)')[0]
        with open(file_name, 'rb') as f:
            self.current_file = {'file': f.read()}

    def search_user(self):
        response = requests.get(api.get_common(f"/search/{self.search.text()}"),
                                headers={'Authorization': "Bearer " + self.token})
        self.new_user = forms.NewUser(response.json()["id"], self, self.token)
        self.new_user.show()

    def edit_chat(self):
        self.edit_chat = forms.EditChat(self.current_chat, self, self.token, self.app)
        self.edit_chat.show()

    def call(self):
        pass
