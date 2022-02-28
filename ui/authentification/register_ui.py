import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStackedWidget, QMessageBox

from db.dao_classes import User
from db.database import Database
from ui.authentification.auth_template_ui import AuthUserInterface


class RegisterScreen(AuthUserInterface):
    def __init__(self, widget: QStackedWidget, config: dict, db: Database):
        super(RegisterScreen, self).__init__(widget, config, db, "ui/qt/register.ui")

        self.worker_pass_label.hide()
        self.worker_pass_line_edit.hide()

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_repeat.setEchoMode(QtWidgets.QLineEdit.Password)

        self.register_button.clicked.connect(self.validate_register)
        self.back_button.clicked.connect(self.go_back)
        self.worker_flag.clicked.connect(self.manage_worker_info)

    def validate_register(self):
        first_name = self.first_name.text()
        second_name = self.second_name.text()
        middle_name = self.middle_name.text()
        phone_number = self.phone_number.text()
        login = self.login.text()
        password = self.password.text()
        password_repeat = self.password_repeat.text()
        worker_flag = self.worker_flag.isChecked()
        worker_pass = self.worker_pass_line_edit.text()

        user_role = 1 if worker_flag and worker_pass == self.worker_passes["manager"] else 3

        phone_matches = re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone_number)
        login_matches = re.match(r'^[a-zA-Z0-9_.-]+$', login)
        rus_initials_r = r'^([А-Я][а-я]+)'
        first_name_matches = re.match(rus_initials_r, first_name)
        second_name_matches = re.match(rus_initials_r, second_name)
        middle_name_matches = re.match(rus_initials_r, middle_name)

        if len(first_name) == 0 \
                or len(second_name) == 0 \
                or len(phone_number) == 0 \
                or len(login) == 0 \
                or len(password) == 0 \
                or len(password_repeat) == 0 \
                or (worker_flag and len(worker_pass) == 0):
            self.error.setText(self.exceptions["empty_fields"])
        elif first_name_matches is None or second_name_matches is None:
            self.error.setText(self.exceptions["incorrect_initials"])
        elif middle_name_matches is None and middle_name != "":
            self.error.setText(self.exceptions["incorrect_initials"])
        elif password != password_repeat:
            self.error.setText(self.exceptions["passwords_unmatched"])
        elif phone_matches is None:
            self.error.setText(self.exceptions["incorrect_phone_signature"])
        elif login_matches is None:
            self.error.setText(self.exceptions["incorrect_login"])

        else:
            new_user = User(
                user_id=0,
                first_name=first_name,
                second_name=second_name,
                middle_name=middle_name,
                phone_number=phone_number,
                login=login,
                password=password,
                role_id=user_role,
                # если менеджер зарегался - его должен подтвердить админ,
                # если юзер - он активен и его не нужно подтверждать
                is_active=True if user_role == 3 else False
            )
            error_message = self.check_input_correct_user_data(new_user)
            if error_message is None:
                self.db.add_user(new_user=new_user)
                popup_registration_complete = QMessageBox()
                popup_registration_complete.setWindowTitle(self.window_names["registration_complete"])
                popup_registration_complete.setText(self.texts["go_to_login"])
                popup_registration_complete.setIcon(QMessageBox.Information)
                popup_registration_complete.exec_()

            else:
                self.error.setText(error_message)

    def manage_worker_info(self):
        worker_flag = self.worker_flag.isChecked()
        if worker_flag:
            self.worker_pass_label.show()
            self.worker_pass_line_edit.show()
        else:
            self.worker_pass_label.hide()
            self.worker_pass_line_edit.hide()
