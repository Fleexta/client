#  Copyright (c) 2025 Timofei Kirsanov

import json

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication

from client import Themes, translate
from client.activities import SettingsActivity

format = "%H:%M"
theme = Themes.DARK
system_theme = Themes.DARK
language = "ru_RU"


def write():
    global format, theme, language
    with open("settings.json", "w", encoding="utf-8") as f:
        settings = {"format": format, "language": language}
        if theme == Themes.DARK:
            settings["theme"] = "Themes.DARK"
        elif theme == Themes.LIGHT:
            settings["theme"] = "Themes.LIGHT"
        elif theme == Themes.SYSTEM:
            settings["theme"] = "Themes.SYSTEM"
        f.write(json.dumps(settings))


def load():
    global format, theme, language
    with open("settings.json", "r", encoding="utf-8") as f:
        settings = json.loads(f.read())
        format = settings["format"]
        if settings["theme"] == "Themes.DARK":
            theme = Themes.DARK
        elif settings["theme"] == "Themes.LIGHT":
            theme = Themes.LIGHT
        elif settings["theme"] == "Themes.SYSTEM":
            theme = Themes.SYSTEM
        language = settings["language"]


def get_theme():
    if theme == Themes.SYSTEM:
        return system_theme
    else:
        return theme


class SettingsWindow(QWidget, SettingsActivity):
    def __init__(self, app: QApplication, refresh):
        super().__init__()
        self.app = app
        self.refresh = refresh
        self.setupUi(self)
        if format == "%H:%M":
            self.format1.setChecked(True)
        elif format == "%H:%M:%S":
            self.format2.setChecked(True)
        self.lang.setCurrentText(language)
        if theme == Themes.LIGHT:
            self.theme.setCurrentText(translate.get("settings.theme.light"))
        elif theme == Themes.DARK:
            self.theme.setCurrentText(translate.get("settings.theme.dark"))
        elif theme == Themes.SYSTEM:
            self.theme.setCurrentText(translate.get("settings.theme.system"))
        self.saveButton.clicked.connect(self.save)

    def save(self):
        global format, language, theme
        for button in self.formatGroup.buttons():
            if button.isChecked():
                selected_text = button.text()
                format = selected_text
        language = self.lang.currentText()
        if self.theme.currentText() == translate.get("settings.theme.system"):
            if system_theme == Themes.DARK:
                self.app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
            elif system_theme == Themes.LIGHT:
                self.app.styleHints().setColorScheme(Qt.ColorScheme.Light)
            theme = Themes.SYSTEM
        elif self.theme.currentText() == translate.get("settings.theme.light"):
            self.app.styleHints().setColorScheme(Qt.ColorScheme.Light)
            theme = Themes.LIGHT
        elif self.theme.currentText() == translate.get("settings.theme.dark"):
            self.app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
            theme = Themes.DARK
        self.app.setStyleSheet("""
            QLineEdit {
                selection-background-color: #A328B0;
            }
    
            QComboBox {
                selection-background-color: #A328B0;
            }
    
            QListWidget {
                selection-background-color: #A328B0;
            }""")
        self.refresh()
        write()
