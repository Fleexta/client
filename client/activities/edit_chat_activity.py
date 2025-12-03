#  Copyright (c) 2025 Timofei Kirsanov

from PyQt6 import QtCore, QtWidgets

from client import translate


class EditChatActivity(object):
    def setupUi(self, centralwidget):
        centralwidget.setObjectName("centralwidget")
        centralwidget.resize(300, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grid = QtWidgets.QGridLayout()
        self.grid.setObjectName("grid")
        self.generateLink = QtWidgets.QPushButton(parent=centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generateLink.sizePolicy().hasHeightForWidth())
        self.generateLink.setSizePolicy(sizePolicy)
        self.generateLink.setObjectName("generateLink")
        self.grid.addWidget(self.generateLink, 2, 3, 1, 1)
        self.membersLabel = QtWidgets.QLabel(parent=centralwidget)
        self.membersLabel.setObjectName("membersLabel")
        self.grid.addWidget(self.membersLabel, 3, 0, 1, 2)
        self.name = QtWidgets.QLabel(parent=centralwidget)
        self.name.setObjectName("name")
        self.grid.addWidget(self.name, 1, 0, 1, 4)
        self.invite = QtWidgets.QLabel(parent=centralwidget)
        self.invite.setObjectName("invite")
        self.grid.addWidget(self.invite, 2, 0, 1, 2)
        self.avatar = QtWidgets.QLabel(parent=centralwidget)
        self.avatar.setObjectName("avatar")
        self.grid.addWidget(self.avatar, 0, 0, 1, 4)
        self.copyLink = QtWidgets.QToolButton(parent=centralwidget)
        self.copyLink.setObjectName("copyLink")
        self.grid.addWidget(self.copyLink, 2, 2, 1, 1)
        self.members = QtWidgets.QLabel(parent=centralwidget)
        self.members.setObjectName("members")
        self.grid.addWidget(self.members, 3, 2, 1, 2)
        self.verticalLayout.addLayout(self.grid)

        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)

    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", translate.get("app.name")))
        self.generateLink.setText(_translate("centralwidget", "Новая"))
        self.membersLabel.setText(_translate("centralwidget", "Участники"))
        self.name.setText(_translate("centralwidget", "name"))
        self.invite.setText(_translate("centralwidget", "invite_link"))
        self.avatar.setText(_translate("centralwidget", "avatar"))
        self.copyLink.setText(_translate("centralwidget", "📃"))
        self.members.setText(_translate("centralwidget", "members"))
