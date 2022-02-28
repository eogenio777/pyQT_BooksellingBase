from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from db.database import Database
from db.dao_classes import User, Order, Book, Role, ManagerOrderCount, ManagerTotalProfit
from ui.cart_state import Cart
from ui.roles_ui.main_window_interface import MainWindowInterface
from ui.tab_state import Tab
from ui.widget_classes.add_book_window import AddBookWindow
from ui.widget_classes.book_widget import BookWidget
from ui.widget_classes.order_widget import OrderWidget
from ui.widget_classes.user_widget import UserWidget


class MainWindowAdmin(MainWindowInterface):
    def __init__(self, config: dict, db: Database, path_to_ui: str, current_user: User):
        super(MainWindowAdmin, self).__init__(config, db, path_to_ui, current_user)
        self.add_new_book_window = None
        self.texts = self.texts["admin"]

        self.setup_content()

        self.tabs.blockSignals(True)

        self.tabs.currentChanged.connect(self.setup_tab_content)
        self.add_new_book.clicked.connect(self.show_add_new_book_dialog)
        self.sort.currentTextChanged.connect(self.fill_employees_stat)
        self.order_stat.currentTextChanged.connect(self.fill_employees_stat)
        self.sort_books.currentTextChanged.connect(self.fill_catalog)
        self.calculate.clicked.connect(self.fill_income)

        self.tabs.blockSignals(False)

    def setup_tab_content(self):
        Tab.current_tab = self.tabs.currentWidget().objectName()
        if Tab.current_tab == "catalog_base":
            self.fill_catalog()
        elif Tab.current_tab == "profile_base":
            self.fill_profile()
        elif Tab.current_tab == "employees_stat_base":
            self.fill_employees_stat()
        elif Tab.current_tab == "employees_base":
            self.fill_employees()
        elif Tab.current_tab == "orders_base":
            self.fill_orders()
        elif Tab.current_tab == "statistics_base":
            pass

    def setup_content(self):
        Tab.current_tab = self.tabs.currentWidget().objectName()
        self.fill_catalog()
        self.fill_profile()
        self.fill_orders()
        self.fill_employees_stat()
        self.fill_employees()

    def fill_catalog(self):
        self.clear_layout(self.catalog)
        direction = self.rus_to_sql(self.sort_books.currentText())
        if direction is None:
            books = self.db.get_all_books()
            for book in books:
                tmp_book_widget = BookWidget(book=book, current_user=self.current_user, db=self.db, config=self.config)
                tmp_book_widget.sold.hide()
                tmp_book_widget.number_sold.hide()
                self.catalog.addWidget(tmp_book_widget)
        else:
            books = self.db.get_books_number_sold_ordered(direction)
            for book_popularity in books:
                tmp_book_widget = BookWidget(book=book_popularity.book, current_user=self.current_user, db=self.db,
                                             config=self.config)
                tmp_book_widget.number_sold.setText(str(book_popularity.number_sold))
                self.catalog.addWidget(tmp_book_widget)

    def fill_profile(self):
        self.clear_layout(self.profile)
        user_profile_widget = UserWidget(current_user=self.current_user, viewable_user=self.current_user, db=self.db,
                                         config=self.config)
        self.profile.addWidget(user_profile_widget)

    def fill_employees_stat(self):
        self.clear_layout(self.employees_stat)
        direction = self.rus_to_sql(self.sort.currentText())
        if self.order_stat.currentText() == "Количество заказов":
            managers_info = self.db.get_managers_order_count_ordered(direction)
            for manager_info in managers_info:
                manager = manager_info.manager
                orders_done = manager_info.orders_done
                manager_widget = UserWidget(current_user=self.current_user, viewable_user=manager, db=self.db,
                                            config=self.config)
                manager_widget.orders_number.setText(str(orders_done))
                self.employees_stat.addWidget(manager_widget)
        elif self.order_stat.currentText() == "Принесенная прибыль":
            managers_info = self.db.get_managers_total_count_ordered(direction)
            for manager_info in managers_info:
                manager = manager_info.manager
                orders_done = manager_info.total_profit
                manager_widget = UserWidget(current_user=self.current_user, viewable_user=manager, db=self.db,
                                            config=self.config)
                manager_widget.orders.setText(self.texts["total_profit"])
                manager_widget.orders_number.setText(str(orders_done))
                self.employees_stat.addWidget(manager_widget)

    def fill_employees(self):
        self.clear_layout(self.employees)
        employees = self.db.get_users_selected_role(Role.MANAGER)
        for manager in employees:
            manager_widget = UserWidget(current_user=self.current_user, viewable_user=manager, db=self.db,
                                        config=self.config)
            manager_widget.orders.hide()
            manager_widget.orders_number.hide()
            self.employees.addWidget(manager_widget)

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

    def fill_income(self):
        self.income.setText(str(self.db.get_base_income_between(self.start_date.dateTime(), self.end_date.dateTime())))

    def clear_layouts(self):
        self.clear_layout(self.catalog)
        self.clear_layout(self.profile)
        self.clear_layout(self.orders)
        self.clear_layout(self.employees)
        self.clear_layout(self.employees_stat)

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

    def rus_to_sql(self, direction: str) -> str:
        if direction == "По возрастанию":
            return "ASC"
        elif direction == "По убыванию":
            return "DESC"
        else:
            return None
