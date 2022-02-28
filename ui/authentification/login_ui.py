from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStackedWidget

from db.dao_classes import User
from db.database import Database
from ui.authentification.auth_template_ui import AuthUserInterface
from ui.roles_ui.main_window_admin import MainWindowAdmin
from ui.roles_ui.main_window_customer import MainWindowCustomer
from ui.roles_ui.main_window_interface import MainWindowInterface
from ui.roles_ui.main_window_manager import MainWindowManager


class LoginScreen(AuthUserInterface):
    def __init__(self, widget: QStackedWidget, config: dict, db: Database):
        super(LoginScreen, self).__init__(widget, config, db, "ui/qt/login.ui")
        self.exceptions = self.config["gui"]["exceptions"]
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button.clicked.connect(self.validate_login)
        self.back_button.clicked.connect(self.go_back)

    def validate_login(self):
        login = self.login_field.text()
        password_unhashed = self.password_field.text()
        if len(login) == 0 or len(password_unhashed) == 0:
            self.error.setText(self.exceptions["empty_fields"])
        else:
            user = User(
                user_id=0,
                first_name="",
                second_name="",
                middle_name="",
                phone_number="",
                login=login,
                password=password_unhashed,
                role_id=3,
                is_active=True
            )
            # result may be either error string in case of failed login
            # or user instance in case when login and password are correct
            result = self.check_input_correct_log_in(user)
            if type(result) is User:
                print("Correct login")
                self.open_main_window(result)
            else:
                self.error.setText(result)

    def open_main_window(self, current_user: User):
        if current_user.role_id == 1:
            main_window = MainWindowManager(config=self.config, db=self.db, current_user=current_user,
                                             path_to_ui="ui/qt/manager.ui")

            self.widget.addWidget(main_window)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        if current_user.role_id == 2:
            main_window = MainWindowAdmin(config=self.config, db=self.db, current_user=current_user,
                                             path_to_ui="ui/qt/admin.ui")

            self.widget.addWidget(main_window)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        if current_user.role_id == 3:
            main_window = MainWindowCustomer(config=self.config, db=self.db, current_user=current_user,
                                             path_to_ui="ui/qt/customer.ui")

            self.widget.addWidget(main_window)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
