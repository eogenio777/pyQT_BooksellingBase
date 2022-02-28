from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from db.dao_classes import Book, User, Order, OrderStatus
from db.database import Database
from ui.widget_classes.book_widget import BookWidget
from ui.widget_classes.show_user_window import ShowUserWindow
from ui.widget_classes.widget_interface import WidgetInterface


class OrderWidget(WidgetInterface):
    def __init__(self, order: Order, current_user: User, db: Database, config: dict):
        super(OrderWidget, self).__init__(current_user, db, config)
        loadUi("ui/qt/order_widget.ui", self)
        self.order = order
        self.viewable_user = self.db.get_user(User(order.user_id, None, None, None, None, None, None, None, None))
        self.operator = self.db.get_user(User(order.operator_id, None, None, None, None, None, None, None, None))
        self.operator_found = self.operator is not None
        self.setup_widgets()
        self.show_user_window = None
        self.show_operator_window = None
        self.user_login_button.clicked.connect(self.show_user)
        self.operator_login_button.clicked.connect(self.show_operator)
        self.save_changes_button.clicked.connect(self.save_changes)

    def setup_widgets(self):
        self.order_id.setText(str(self.order.order_id))
        self.date.setText(str(self.order.date))
        self.user_login_button.setText(self.viewable_user.login)
        if self.operator_found:
            self.operator_login_button.setText(self.operator.login)
        else:
            self.operator_login_button.setText(self.texts["customer"]["operator_pending"])
            self.operator_login_button.setEnabled(False)
        self.info.insertPlainText(self.order.info)
        self.total_price.setText(str(self.order.total_price))
        self.order_status.setCurrentIndex(self.order.status_id - 1)

        order = Order(self.order.order_id, None, None, None, None, None, None)
        order_info_list = self.db.get_order_info(order)

        role_id = self.current_user.role_id
        # manager
        if role_id == 1 or role_id == 2:
            for info in order_info_list:
                book_widget = BookWidget(info.book, self.viewable_user, self.db, self.config)
                book_widget.quantity.setText(str(info.quantity))
                self.order_books.addWidget(book_widget)
        # customer
        elif role_id == 3:
            self.save_changes_button.hide()
            self.info.setEnabled(False)
            for info in order_info_list:
                book_widget = BookWidget(info.book, self.current_user, self.db, self.config)
                book_widget.quantity.setText(str(info.quantity))
                self.order_books.addWidget(book_widget)
                self.total_price.setEnabled(False)
                self.order_status.setEnabled(False)

    def show_user(self):
        if self.show_user_window is None:
            self.show_user_window = ShowUserWindow(self.current_user, self.db, self.config, self.viewable_user)
        self.show_user_window.show()

    def show_operator(self):
        if self.show_operator_window is None:
            self.show_operator_window = ShowUserWindow(self.current_user, self.db, self.config, self.operator)
        self.show_operator_window.show()


    def save_changes(self):
        self.order.info = self.info.toPlainText()
        self.order.total_price = self.total_price.text()
        self.db.update_order_info(self.order, self.order.info)
        self.db.update_order_total_price(self.order, self.order.total_price)
        new_order_status = OrderStatus(self.order_status.currentText())
        self.db.update_order_status(self.order, new_order_status)
        self.db.update_order_operator_id(self.order, self.current_user.user_id)
