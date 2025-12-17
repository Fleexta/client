import json
import sys

from PyQt6.QtCore import Qt

from client.activities import LoginActivity
from PyQt6.QtNetwork import QNetworkAccessManager
from PyQt6.QtWidgets import QWidget, QApplication

from client.main import Main
from client import api, translate, forms, settings, Themes, cache
from client.registration import Registration


class Login(QWidget, LoginActivity):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)
        self.manager = QNetworkAccessManager()

    def login(self):
        if not self.loginBox.text() or not self.passwordBox.text():
            forms.warn(self, translate.get("auth.error.empty"))
        else:
            form_data = {
                "grant_type": "password",
                "username": self.loginBox.text(),
                "password": self.passwordBox.text()
            }
            result, status = api.post_token("/token", form_data)
            if status == 401:
                forms.warn(self, translate.get("auth.error.wrong"))
            self.open_main(json.loads(result)["access_token"], json.loads(result)["id"])

    def register(self):
        self.registration = Registration(self)
        self.registration.show()
        self.close()

    def open_main(self, token, id):
        self.main = Main(self.app, token, id)
        self.main.load_chats()
        self.main.refresh()
        self.main.show()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    settings.load()
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QLineEdit {
            selection-background-color: #A328B0;
        }

        QComboBox {
            selection-background-color: #A328B0;
        }

        QListWidget {
            selection-background-color: #A328B0;
        }""")

    if not (cache.check()):
        cache.init()

    if app.styleHints().colorScheme() == Qt.ColorScheme.Light:
        settings.system_theme = Themes.LIGHT
    elif app.styleHints().colorScheme() == Qt.ColorScheme.Dark:
        settings.system_theme = Themes.DARK

    if settings.get_theme() == Themes.LIGHT:
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    elif settings.get_theme() == Themes.DARK:
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark)

    ex = Login(app)
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
