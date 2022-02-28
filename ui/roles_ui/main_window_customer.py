from PyQt5.QtWidgets import QLabel

from db.database import Database
from db.dao_classes import User, Order
from ui.cart_state import Cart
from ui.roles_ui.main_window_interface import MainWindowInterface
from ui.tab_state import Tab
from ui.widget_classes.book_widget import BookWidget
from ui.widget_classes.order_widget import OrderWidget
from ui.widget_classes.user_widget import UserWidget


class MainWindowCustomer(MainWindowInterface):
    def __init__(self, config: dict, db: Database, path_to_ui: str, current_user: User):
        super(MainWindowCustomer, self).__init__(config, db, path_to_ui, current_user)

        self.texts = self.texts["customer"]
        self.tabs.blockSignals(True)
        self.setup_content()

        self.tabs.currentChanged.connect(self.setup_tab_content)

        self.clear_cart.clicked.connect(self.delete_current_order_clear_cart)
        self.submit_order.clicked.connect(self.finalize_order)

        self.tabs.blockSignals(False)

    def setup_tab_content(self):
        Tab.current_tab = self.tabs.currentWidget().objectName()
        if Tab.current_tab == "catalog_base":
            self.fill_catalog()
        elif Tab.current_tab == "profile_base":
            self.fill_profile()
        elif Tab.current_tab == "orders_base":
            self.fill_orders()
        elif Tab.current_tab == "cart_base":
            self.fill_cart()

    def setup_content(self):
        Tab.current_tab = self.tabs.currentWidget().objectName()
        self.fill_profile()
        self.fill_orders()
        self.fill_catalog()
        self.fill_cart()

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
        user = User(self.current_user.user_id, None, None, None, None, None, None, None, None)
        user_orders = self.db.get_user_orders(user)
        for order in user_orders:
            order_widget = OrderWidget(order, self.current_user, self.db, self.config)
            self.orders.addWidget(order_widget)

    def fill_cart(self):
        self.clear_layout(self.cart)
        if Cart.cart_empty and Cart.order_id is None:
            label = QLabel(self.texts["cart_is_empty"])
            self.cart.addWidget(label)
            self.order_info_label.hide()
            self.order_info.hide()
            self.submit_order.hide()
            self.clear_cart.hide()
        else:
            order = Order(Cart.order_id, None, None, None, None, None, None)
            order_info_list = self.db.get_order_info(order)
            for info in order_info_list:
                book_widget = BookWidget(info.book, self.current_user, self.db, self.config)
                self.cart.addWidget(book_widget)
            self.order_info_label.show()
            self.order_info.show()
            self.submit_order.show()
            self.clear_cart.show()

    def delete_current_order_clear_cart(self):
        order = Order(Cart.order_id, None, None, None, None, None, None)
        self.db.delete_unfinished_order(order)
        Cart.cart_empty = True
        Cart.order_id = None
        self.fill_cart()

    def finalize_order(self):
        order = Order(Cart.order_id, None, None, None, None, None, None)
        total_price = self.calculate_order_price()
        self.update_all_order_books()
        self.db.update_order_total_price(order=order, new_price=total_price)
        self.db.update_order_info(order=order, new_info=self.order_info.toPlainText())
        Cart.cart_empty = True
        Cart.order_id = None
        self.fill_cart()

    def update_all_order_books(self):
        for i in range(self.cart.count()):
            self.cart.itemAt(i).widget().update_quantity_from_cart()

    def calculate_order_price(self) -> float:
        total_price = 0.0
        for i in range(self.cart.count()):
            total_price += float(self.cart.itemAt(i).widget().price.text()) * int(
                self.cart.itemAt(i).widget().quantity_spin.value())
        return total_price

    def clear_layouts(self):
        self.clear_layout(self.catalog)
        self.clear_layout(self.profile)
        self.clear_layout(self.orders)
        self.clear_layout(self.cart)
