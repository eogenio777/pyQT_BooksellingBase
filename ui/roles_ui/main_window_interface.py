import hashlib
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout

from db.database import Database
from db.dao_classes import User


class MainWindowInterface(QMainWindow):
    def __init__(self, config: dict, db: Database, path_to_ui: str, current_user: User):
        QMainWindow.__init__(self)
        # super(MainWindowInterface, self).__init__()
        self.adjustSize()
        self.config = config
        self.exceptions = self.config["gui"]["exceptions"]
        self.window_names = self.config["gui"]["window_names"]
        self.texts = self.config["gui"]["texts"]
        self.db = db
        self.current_user = current_user
        uic.loadUi(path_to_ui, self)

    def setup_content(self):
        pass

    def clear_layout(self, layout: QVBoxLayout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def clear_layouts(self):
        pass
