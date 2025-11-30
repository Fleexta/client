#  Copyright (c) 2025 Timofei Kirsanov
from client import translate

from PyQt6 import QtCore, QtWidgets


class CreateChatActivity(object):
    def setupUi(self, centralwidget):
        centralwidget.setObjectName("centralwidget")
        centralwidget.resize(205, 299)
        self.verticalLayout = QtWidgets.QVBoxLayout(centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grid = QtWidgets.QGridLayout()
        self.grid.setObjectName("grid")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.grid.addItem(spacerItem, 10, 1, 1, 1)
        self.chatCreate = QtWidgets.QPushButton(parent=centralwidget)
        self.chatCreate.setObjectName("chatCreate")
        self.grid.addWidget(self.chatCreate, 6, 1, 1, 1)
        self.createChatName = QtWidgets.QLineEdit(parent=centralwidget)
        self.createChatName.setInputMask("")
        self.createChatName.setObjectName("createChatName")
        self.grid.addWidget(self.createChatName, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.grid.addItem(spacerItem1, 5, 1, 1, 1)
        self.chatType = QtWidgets.QComboBox(parent=centralwidget)
        self.chatType.setObjectName("chatType")
        self.chatType.addItem("")
        self.chatType.addItem("")
        self.grid.addWidget(self.chatType, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.grid.addItem(spacerItem2, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.grid.addItem(spacerItem3, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.grid.addItem(spacerItem4, 7, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.grid.addItem(spacerItem5, 3, 2, 1, 2)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.grid.addItem(spacerItem6, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(parent=centralwidget)
        self.label.setObjectName("label")
        self.grid.addWidget(self.label, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.grid)

        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)

    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", translate.get("chat.new")))
        self.chatCreate.setText(_translate("centralwidget", translate.get("chat.create")))
        self.chatType.setItemText(0, _translate("centralwidget", translate.get("chat.chat")))
        self.chatType.setItemText(1, _translate("centralwidget", translate.get("chat.channel")))
        self.label.setText(_translate("centralwidget", translate.get("chat.create")))
