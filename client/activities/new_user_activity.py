#  Copyright (c) 2025 Timofei Kirsanov

from PyQt6 import QtCore, QtWidgets

from client import translate


class NewUserActivity(object):
    def setupUi(self, centralwidget):
        centralwidget.setObjectName("centralwidget")
        centralwidget.resize(205, 299)
        self.verticalLayout = QtWidgets.QVBoxLayout(centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grid = QtWidgets.QGridLayout()
        self.grid.setObjectName("grid")
        self.chatCreate = QtWidgets.QPushButton(parent=centralwidget)
        self.chatCreate.setObjectName("chatCreate")
        self.grid.addWidget(self.chatCreate, 4, 0, 1, 2)
        self.aboutLabel = QtWidgets.QLabel(parent=centralwidget)
        self.aboutLabel.setObjectName("aboutLabel")
        self.grid.addWidget(self.aboutLabel, 2, 0, 1, 1)
        self.about = QtWidgets.QLabel(parent=centralwidget)
        self.about.setObjectName("about")
        self.grid.addWidget(self.about, 2, 1, 1, 1)
        self.username = QtWidgets.QLabel(parent=centralwidget)
        self.username.setObjectName("username")
        self.grid.addWidget(self.username, 1, 0, 1, 2)
        self.avatar = QtWidgets.QLabel(parent=centralwidget)
        self.avatar.setObjectName("avatar")
        self.grid.addWidget(self.avatar, 0, 0, 1, 2)
        self.verticalLayout.addLayout(self.grid)

        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)

    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", translate.get("user")))
        self.chatCreate.setText(_translate("centralwidget", translate.get("user.write")))
        self.aboutLabel.setText(_translate("centralwidget", translate.get("user.about")))
        self.about.setText(_translate("centralwidget", "about"))
        self.username.setText(_translate("centralwidget", "username"))
        self.avatar.setText(_translate("centralwidget", "avatar"))
