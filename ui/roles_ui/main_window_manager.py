import sys

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QMessageBox

from db.database import Database
from db.dao_classes import User, Order, Book, Role
from ui.cart_state import Cart
from ui.roles_ui.main_window_interface import MainWindowInterface
from ui.tab_state import Tab
from ui.widget_classes.add_book_window import AddBookWindow
from ui.widget_classes.book_widget import BookWidget
from ui.widget_classes.order_widget import OrderWidget
from ui.widget_classes.user_widget import UserWidget


class MainWindowManager(MainWindowInterface):
    def __init__(self, config: dict, db: Database, path_to_ui: str, current_user: User):
        super(MainWindowManager, self).__init__(config, db, path_to_ui, current_user)
        self.add_new_book_window = None
        self.texts = self.texts["manager"]

        self.setup_content()

        self.tabs.blockSignals(True)

        self.tabs.currentChanged.connect(self.setup_tab_content)
        self.add_new_book.clicked.connect(self.show_add_new_book_dialog)
        self.sort_status.currentTextChanged.connect(self.fill_orders)

        self.tabs.blockSignals(False)

    def setup_tab_content(self):
        Tab.current_tab = self.tabs.currentWidget().objectName()
        if Tab.current_tab == "catalog_base":
            self.fill_catalog()
        elif Tab.current_tab == "profile_base":
            self.fill_profile()
        elif Tab.current_tab == "orders_base":
            self.fill_orders()

    def setup_content(self):
        if not self.current_user.is_active:
            popup_book_added = QMessageBox()
            popup_book_added.setWindowTitle(self.window_names["error"])
            admin_phone = self.db.get_users_selected_role(Role.ADMIN)[0].phone_number
            popup_book_added.setText(
                self.exceptions["not_verified_user"] + admin_phone)
            popup_book_added.setIcon(QMessageBox.Critical)
            popup_book_added.exec_()
            sys.exit(0)
        Tab.current_tab = self.tabs.currentWidget().objectName()
        self.fill_profile()
        self.fill_orders()
        self.fill_catalog()

    def fill_catalog(self):
        self.clear_layout(self.catalog)
        books = self.db.get_all_books()
        for book in books:
            tmp_book_widget = BookWidget(book=book, current_user=self.current_user, db=self.db, config=self.config)
            self.catalog.addWidget(tmp_book_widget)

    def fill_profile(self):
        self.clear_layout(self.profile)
        user_profile_widget = UserWidget(current_user=self.current_user, viewable_user=self.current_user, db=self.db,
                                         config=self.config)
        self.profile.addWidget(user_profile_widget)

    def fill_orders(self):
        self.clear_layout(self.orders)
        customers = self.db.get_users_selected_role(Role.CUSTOMER)
        current_index = self.sort_status.currentIndex()
        for customer in customers:
            customer_orders = self.db.get_user_orders(customer)
            if len(customer_orders) > 0:
                user_label = QLabel(self.texts["user"] + " " + customer.login + ":")
                self.orders.addWidget(user_label)
            orders_count = 0
            for order in customer_orders:
                if current_index == 0 or order.status_id == current_index:
                    order_widget = OrderWidget(order, self.current_user, self.db, self.config)
                    order_widget.save_changes_button.clicked.connect(self.fill_orders)
                    self.orders.addWidget(order_widget)
                    orders_count += 1
            if orders_count == 0 and len(customer_orders) > 0:
                label_no_orders_with_selected_status = QLabel(self.texts["no_orders_with_selected_status"])
                self.orders.addWidget(label_no_orders_with_selected_status)

    def clear_layouts(self):
        self.clear_layout(self.catalog)
        self.clear_layout(self.profile)
        self.clear_layout(self.orders)

    def show_add_new_book_dialog(self):
        empty_book = Book(book_id=None,
                          title=None,
                          description=None,
                          author=None,
                          price=None,
                          quantity=None)
        if self.add_new_book_window is None:
            self.add_new_book_window = AddBookWindow(book=empty_book, current_user=self.current_user, db=self.db,
                                                     config=self.config)
        self.add_new_book_window.show()
