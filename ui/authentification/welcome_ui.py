from PyQt5.QtWidgets import QStackedWidget

from db.database import Database
from ui.authentification.login_ui import LoginScreen
from ui.authentification.register_ui import RegisterScreen
from ui.authentification.auth_template_ui import AuthUserInterface


class WelcomeScreen(AuthUserInterface):
    def __init__(self, widget: QStackedWidget, config: dict, db: Database):
        super(WelcomeScreen, self).__init__(widget, config, db, "ui/qt/welcomescreen.ui")
        self.login_redirect_button.clicked.connect(self.login_page)
        self.register_redirect_button.clicked.connect(self.register_page)

    def login_page(self):
        login = LoginScreen(widget=self.widget, config=self.config, db=self.db)
        self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def register_page(self):
        register = RegisterScreen(widget=self.widget, config=self.config, db=self.db)
        self.widget.addWidget(register)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
