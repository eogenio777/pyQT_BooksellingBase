from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from db.dao_classes import User
from db.database import Database
from ui.widget_classes.widget_interface import WidgetInterface


class UserWidget(WidgetInterface):
    def __init__(self, current_user: User, viewable_user: User, db: Database, config: dict):
        super(UserWidget, self).__init__(current_user, db, config)
        loadUi("ui/qt/user_widget.ui", self)
        self.viewable_user = viewable_user
        self.setup_widgets()
        self.adjustSize()
        self.is_active.stateChanged.connect(self.change_active_flag)

    def setup_widgets(self):
        # fill in all fields
        self.first_name.setText(self.viewable_user.first_name)
        self.second_name.setText(self.viewable_user.second_name)
        self.middle_name.setText(self.viewable_user.middle_name)
        self.phone_number.setText(self.viewable_user.phone_number)
        self.login.setText(self.viewable_user.login)
        self.role.setText(self.role_id_to_text(self.viewable_user.role_id))
        self.first_name.setText(self.viewable_user.first_name)
        self.is_active.setChecked(self.viewable_user.is_active)

        role_id = self.current_user.role_id
        # manager or customer
        if role_id == 1 or role_id == 3:
            self.orders.hide()
            self.orders_number.hide()
            self.is_active.hide()
        # admin - fill in orders_number
        elif role_id == 2:
            if self.viewable_user.role_id == 1:
                # запрос гавно, переписать
                pass
            elif self.viewable_user.role_id == 3 or self.viewable_user.role_id == 2:
                self.orders.hide()
                self.orders_number.hide()
                self.is_active.setEnabled(False)

    def change_active_flag(self):
        self.viewable_user.is_active = self.is_active.isChecked()
        self.db.update_user(self.viewable_user)

    def role_id_to_text(self, role_id: int):
        if role_id == 1:
            return "Менеджер"
        elif role_id == 2:
            return "Администратор"
        elif role_id == 3:
            return "Покупатель"
