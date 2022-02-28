import logging

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from db.dao_classes import User
from db.database import Database
from logs.setup_logger import setup_logger


class WidgetInterface(QWidget):
    def __init__(self, current_user: User, db: Database, config: dict):
        super(WidgetInterface, self).__init__()
        self.config = config
        self.exceptions = self.config["gui"]["exceptions"]
        self.window_names = self.config["gui"]["window_names"]
        self.texts = self.config["gui"]["texts"]
        self.current_user = current_user
        self.db = db
        self.logger = setup_logger(file_path=f"logs\\main_window.log",
                                   name=__name__,
                                   level=logging.INFO)

    def setup_widgets(self):
        pass
