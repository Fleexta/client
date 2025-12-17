#  Copyright (c) 2025 Timofei Kirsanov

import requests
from PyQt6.QtWidgets import QWidget

from client import forms, translate, api
from client.activities import RegistrationActivity


class Registration(QWidget, RegistrationActivity):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.registerButton.clicked.connect(self.register)

    def register(self):
        if (self.loginBox.text() == "" or self.passwordBox.text() == "" or
                self.retryBox.text() == "" or self.nameBox.text() == ""):
            forms.warn(self, translate.get("auth.error.empty"))
        if self.passwordBox.text() != self.retryBox.text():
            forms.warn(self, translate.get("auth.error.password"))
        else:
            form_data = {
                "username": self.loginBox.text(),
                "password": self.passwordBox.text(),
                "name": self.nameBox.text()
            }
            response = requests.post(api.get_common("/reg"), json=form_data)
            if response.status_code == 200:
                self.parent.show()
                self.close()
