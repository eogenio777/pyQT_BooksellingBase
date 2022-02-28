from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QMessageBox

from db.dao_classes import Book, User, Order, OrderBook
from db.database import Database
from ui.cart_state import Cart
from ui.tab_state import Tab
from ui.widget_classes.widget_interface import WidgetInterface


class BookWidget(WidgetInterface):
    def __init__(self, book: Book, current_user: User, db: Database, config: dict):
        super(BookWidget, self).__init__(current_user, db, config)
        loadUi("ui/qt/book_widget.ui", self)

        self.current_user = current_user
        self.book = book
        self.setup_widgets()
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        self.save_changes.clicked.connect(self.save_book_changes)
        self.finish_add_new_book.clicked.connect(self.add_new_book)
        self.delete_button.clicked.connect(self.try_delete_book)

    def add_to_cart(self):
        order = Order(
            order_id=Cart.order_id,
            user_id=self.current_user.user_id,
            info=None,
            date=None,
            total_price=0,
            operator_id=None,
            status_id=1
        )
        if Cart.cart_empty:
            Cart.order_id = self.db.add_order(order)
            self.logger.info(f"New order#{Cart.order_id} created")
            Cart.cart_empty = False
        if not Cart.cart_empty and self.quantity_spin.value() > 0:
            new_position = OrderBook(
                order_id=Cart.order_id,
                book_id=self.book.book_id,
                quantity=self.quantity_spin.value()
            )
            self.db.add_position_order_book(new_position)
            self.logger.info(
                f"New position: order#{new_position.order_id} book##{new_position.book_id} "
                f"quantity={new_position.quantity}")
            self.book.quantity -= self.quantity_spin.value()
            self.quantity.setText(str(self.book.quantity))
            self.quantity_spin.setRange(0, self.book.quantity)
            self.quantity_spin.setValue(1)
        else:
            popup_book_quantity_error = QMessageBox()
            popup_book_quantity_error.setWindowTitle(self.window_names["error"])
            popup_book_quantity_error.setText(self.exceptions["book_quantity_error"])
            popup_book_quantity_error.setIcon(QMessageBox.Critical)
            popup_book_quantity_error.exec_()
        self.clear_widgets()
        self.setup_widgets()

    def save_book_changes(self):
        updated_book = Book(book_id=self.book.book_id,
                            title=self.title.text(),
                            description=self.description.toPlainText(),
                            author=self.author.text(),
                            price=self.price.text(),
                            quantity=self.quantity.text())
        self.db.update_book(updated_book)

    def add_new_book(self):
        new_book = Book(book_id=self.book.book_id,
                        title=self.title.text(),
                        description=self.description.toPlainText(),
                        author=self.author.text(),
                        price=self.price.text(),
                        quantity=self.quantity.text())
        self.db.add_book(new_book)
        popup_book_added = QMessageBox()
        popup_book_added.setWindowTitle(self.window_names["success"])
        popup_book_added.setText(self.exceptions["add_book_success"])
        popup_book_added.setIcon(QMessageBox.Information)
        popup_book_added.exec_()

    def setup_widgets(self):
        # fill in all fields
        self.title.insert(self.book.title)
        self.description.insertPlainText(self.book.description)
        self.author.insert(self.book.author)
        only_float = QDoubleValidator()
        self.quantity.setValidator(only_float)
        self.price.insert(str(self.book.price))
        only_int = QIntValidator()
        self.quantity.setValidator(only_int)
        self.quantity.insert(str(self.book.quantity))
        if self.book.quantity is not None:
            self.quantity_spin.setRange(0, self.book.quantity)
        self.quantity_spin.setValue(1)
        self.info.hide()

        role_id = self.current_user.role_id
        # manager or admin
        if role_id == 1 or role_id == 2:
            self.add_to_cart_button.hide()
            self.quantity_spin.hide()
            self.finish_add_new_book.hide()
            if role_id == 1:
                self.delete_button.hide()
                self.sold.hide()
                self.number_sold.hide()
            if Tab.current_tab == "orders_base":
                self.title.setEnabled(False)
                self.description.setEnabled(False)
                self.author.setEnabled(False)
                self.price.setEnabled(False)
                self.quantity.setEnabled(True)
                self.quantity_spin.hide()
        # customer
        elif role_id == 3:
            self.title.setEnabled(False)
            self.description.setEnabled(False)
            self.author.setEnabled(False)
            self.price.setEnabled(False)
            self.quantity.setEnabled(False)
            self.delete_button.hide()
            self.save_changes.hide()
            self.sold.hide()
            self.number_sold.hide()
            self.finish_add_new_book.hide()
            if Tab.current_tab == "catalog_base" and self.book.quantity <= 0:
                self.add_to_cart_button.hide()
                self.info.setText(self.exceptions["book_quantity_error"])
                self.info.show()
            if Tab.current_tab == "catalog_base" and not Cart.cart_empty:
                if self.db.is_book_in_cart(book=self.book, order_id=Cart.order_id):
                    self.add_to_cart_button.hide()
            elif Tab.current_tab == "cart_base":
                self.add_to_cart_button.hide()
                quantity = self.db.get_order_book_quantity(Cart.order_id, self.book.book_id)
                if quantity is not None:
                    self.quantity_spin.setRange(1, self.book.quantity)
                    self.quantity_spin.setValue(quantity)
            elif Tab.current_tab == "orders_base":
                self.add_to_cart_button.hide()
                self.quantity_spin.hide()

    def update_quantity_from_cart(self):
        self.db.update_order_book_quantity(self.quantity_spin.value(), Cart.order_id, self.book.book_id)

    def try_delete_book(self):
        is_book_deleted = self.db.delete_book(self.book)
        popup_book_added = QMessageBox()
        if is_book_deleted:
            popup_book_added.setWindowTitle(self.window_names["success"])
            popup_book_added.setText(self.exceptions["delete_book_success"])
            popup_book_added.setIcon(QMessageBox.Information)
        else:
            popup_book_added.setWindowTitle(self.window_names["error"])
            popup_book_added.setText(self.exceptions["unable_to_delete_book"])
            popup_book_added.setIcon(QMessageBox.Critical)
        popup_book_added.exec_()

    def clear_widgets(self):
        self.title.setText("")
        self.description.clear()
        self.author.setText("")
        self.price.setText("")
        self.quantity.setText("")
