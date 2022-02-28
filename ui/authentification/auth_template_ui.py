import hashlib
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget

from db.database import Database
from db.dao_classes import User


class AuthUserInterface(QDialog):
    def __init__(self, widget: QStackedWidget, config: dict, db: Database, path_to_ui: str):
        super(AuthUserInterface, self).__init__()
        loadUi(path_to_ui, self)
        self.adjustSize()
        self.widget = widget
        self.config = config
        self.exceptions = self.config["gui"]["exceptions"]
        self.worker_passes = self.config["gui"]["worker_passes"]
        self.window_names = self.config["gui"]["window_names"]
        self.texts = self.config["gui"]["texts"]["authentication"]
        self.db = db

    def check_input_correct_user_data(self, current_user: User):
        check_user = self.db.get_user_by_nickname(current_user)
        if check_user is not None:
            return self.exceptions["user_login_exists"]
        check_user = self.db.get_user_by_phone(current_user)
        if check_user is not None:
            return self.exceptions["user_phone_exists"]
        # TODO: check phone, login, names with regex
        # if current_user.phone_number
        # if current_user.login

    def check_input_correct_log_in(self, current_user: User):
        check_user = self.db.get_user_by_nickname(current_user)
        hashed_password = hashlib.md5(current_user.password.encode()).hexdigest()
        if check_user is None:
            return self.exceptions["user_login_does_not_exist"]
        if hashed_password != check_user.password:
            return self.exceptions["user_password_incorrect"]
        return check_user

    def go_back(self):
        current_page = self.widget.currentWidget()
        self.widget.removeWidget(current_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)
