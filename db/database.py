import datetime
import hashlib
import pyodbc
from logs.setup_logger import setup_logger
import logging
from db.dao_classes import (Book, User, OrderBook,
                            Order, OrderStatus, Role, ManagerOrderCount,
                            parse_tuple_book, parse_tuple_order,
                            parse_tuple_user, parse_role_str, parse_tuple_manager_order_count,
                            parse_tuple_book_popularity, BookPopularity,
                            parse_tuple_manager_total_profit, ManagerTotalProfit,
                            parse_tuple_order_info, OrderInfo)


class Database:
    def __init__(self, driver, dbname, server):
        self.connection = pyodbc.connect(
            Trusted_Connection='Yes',
            Driver=driver,
            Server=server,
            Database=dbname)
        self.logger = setup_logger(file_path=f"logs\\db.log",
                                   name=__name__,
                                   level=logging.INFO)

    # SYSTEM
    def __log_rows(self, rows: list):
        for row in rows:
            self.logger.debug(row)

    def __log_query_rows_updated(self, logger_str: str, rows_len: int):
        if rows_len == 0:
            self.logger.info(f"{logger_str}: no rows updated")
        else:
            self.logger.info(f"{logger_str}: {rows_len} rows updated")

    # CREATE_______________________________________
    # Books:
    def add_book(self, new_book: Book) -> int:
        cursor = self.connection.cursor()
        logger_str = f"EXEC ADD_BOOK " \
                     f"'{new_book.title}'," \
                     f"'{new_book.description}'," \
                     f"'{new_book.author}'," \
                     f"'{new_book.price}'," \
                     f"'{new_book.quantity}',"

        cursor.execute(
            "EXEC ADD_BOOK "
            "?,"
            "?,"
            "?,"
            "?,"
            "?",
            new_book.title,
            new_book.description,
            new_book.author,
            new_book.price,
            new_book.quantity)
        rows = cursor.fetchall()
        book_id = int(rows[0][0])
        rows_len = len(rows)
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()
        return book_id

    # Orders:
    def add_order(self, new_order: Order) -> int:
        """Returns new_order.order_id"""
        new_order.status_id = 1
        cursor = self.connection.cursor()
        logger_str = f"EXEC ADD_ORDER " \
                     f"{new_order.user_id}," \
                     f"'{new_order.info}'," \
                     f"'{new_order.total_price}'," \
                     f"'{new_order.status_id}',"

        cursor.execute(
            "EXEC ADD_ORDER "
            "?,"
            "?,"
            "?,"
            "?",
            new_order.user_id,
            new_order.info,
            new_order.total_price,
            new_order.status_id)
        rows = cursor.fetchall()
        order_id = int(rows[0][0])
        rows_len = len(rows)
        if rows_len > 1:
            raise Exception("Несколько заказов создано, должен был один.")
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()
        return order_id

    # OrdersBooks:
    def add_position_order_book(self, order_book: OrderBook):
        cursor = self.connection.cursor()
        logger_str = f"INSERT INTO [OrdersBooks] " \
                     f"VALUES ({order_book.order_id}, {order_book.book_id}, {order_book.quantity})"

        cursor.execute("INSERT INTO [OrdersBooks] "
                       "VALUES (?,?,?)",
                       order_book.order_id,
                       order_book.book_id,
                       order_book.quantity)

        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    # Users:
    def add_user(self, new_user: User) -> int:
        cursor = self.connection.cursor()
        logger_str = f"EXEC ADD_NEW_USER " \
                     f"'{new_user.first_name}'," \
                     f"'{new_user.second_name}'," \
                     f"'{new_user.middle_name}'," \
                     f"'{new_user.phone_number}'," \
                     f"'{new_user.login}'," \
                     f"'***'," \
                     f"'{new_user.role_id}'," \
                     f"'{new_user.is_active}'"

        hashed_password = hashlib.md5(new_user.password.encode())

        cursor.execute(
            "EXEC ADD_NEW_USER ?,?,?,?,?,?,?,?",
            new_user.first_name,
            new_user.second_name,
            new_user.middle_name,
            new_user.phone_number,
            new_user.login,
            hashed_password.hexdigest(),
            new_user.role_id,
            new_user.is_active)

        rows = cursor.fetchall()
        user_id = int(rows[0][0])

        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()
        return user_id

    # UPDATE________________________________________
    # Books:
    def update_book(self, book: Book):
        cursor = self.connection.cursor()
        logger_str = f"UPDATE BOOK {book.book_id}"
        cursor.execute("""
        UPDATE [Books]
        SET [title] = ?,
            [description] = ?,
            [author] = ?,
            [price] = ?,
            [quantity] = ?
        WHERE Books.book_id = ?
                        """,
                       book.title,
                       book.description,
                       book.author,
                       book.price,
                       book.quantity,
                       book.book_id)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    # Orders:
    def update_order_status(self, order: Order, status: OrderStatus):
        cursor = self.connection.cursor()
        logger_str = f"EXEC SET_ORDER_STATUS {order.order_id}, '{status.value}'"
        cursor.execute("EXEC SET_ORDER_STATUS ?, ?",
                       order.order_id,
                       status.value)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    def update_order_total_price(self, order: Order, new_price: float):
        cursor = self.connection.cursor()
        logger_str = f"UPDATE [Orders] " \
                     f"SET [total_price] = {new_price} " \
                     f"WHERE OrderBooks.order_id = {order.order_id}"
        cursor.execute("""
                        UPDATE [Orders]
                        SET [total_price] = ?
                        WHERE Orders.order_id = ?
                        """,
                       new_price,
                       order.order_id)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    def update_order_info(self, order: Order, new_info: str):
        cursor = self.connection.cursor()
        logger_str = f"UPDATE [Orders] " \
                     f"SET [info] = {new_info} " \
                     f"WHERE Orders.order_id = {order.order_id}"
        cursor.execute("""
                        UPDATE [Orders]
                        SET [info] = ?
                        WHERE Orders.order_id = ?
                        """,
                       new_info,
                       order.order_id)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    def update_order_operator_id(self, order: Order, operator_id: int):
        cursor = self.connection.cursor()
        logger_str = f"UPDATE [Orders] " \
                     f"SET [operator_id] = {operator_id} " \
                     f"WHERE Orders.order_id = {order.order_id}"
        cursor.execute("""
                        UPDATE [Orders]
                        SET [operator_id] = ?
                        WHERE Orders.order_id = ?
                        """,
                       operator_id,
                       order.order_id)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    # OrdersBooks:
    def update_order_book_quantity(self, quantity: int, order_id: int, book_id: int):
        cursor = self.connection.cursor()
        logger_str = f"UPDATE [OrdersBooks] " \
                     f"SET [quantity] = {quantity} " \
                     f" WHERE OrdersBooks.order_id = {order_id} AND OrdersBooks.book_id = {book_id}"

        cursor.execute(
            """UPDATE [OrdersBooks] SET [quantity] = ? 
            WHERE OrdersBooks.order_id = ? AND OrdersBooks.book_id = ?""",
            quantity,
            order_id,
            book_id)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    # Users:
    def update_user(self, updated_user: User):
        cursor = self.connection.cursor()
        logger_str = f"UPDATE [Users] " \
                     f"SET [first_name] = {updated_user.first_name}," \
                     f"[second_name] = {updated_user.second_name}," \
                     f"[middle_name] = {updated_user.middle_name}," \
                     f"[role_id] = {updated_user.role_id}," \
                     f"[phone_number] = {updated_user.phone_number}," \
                     f"[is_active] = {updated_user.is_active}" \
                     f" WHERE Users.user_id = {updated_user.user_id}"

        cursor.execute("UPDATE [Users] "
                       "SET [first_name] = ?,"
                       "[second_name] = ?,"
                       "[middle_name] = ?,"
                       "[role_id] = ?,"
                       "[phone_number] = ?,"
                       "[is_active] = ? "
                       " WHERE Users.user_id = ?",
                       updated_user.first_name,
                       updated_user.second_name,
                       updated_user.middle_name,
                       updated_user.role_id,
                       updated_user.phone_number,
                       updated_user.is_active,
                       updated_user.user_id)

        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    # DELETE________________________________________
    # Books:
    def delete_book(self, book: Book):
        cursor = self.connection.cursor()
        logger_str = f"DELETE FROM [Books]" \
                     f" WHERE Books.book_id = {book.book_id}"

        cursor.execute(f"EXEC GET_UNFINISHED_ORDERS_WITH_BOOK ?",
                       book.book_id)

        if len(cursor.fetchall()) > 0:
            self.logger.exception("Attempt to delete book, which remains in orders.")
            return False
        cursor.execute(f"DELETE FROM [Books]"
                       f" WHERE Books.book_id = ?",
                       book.book_id)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()
        return True

    # Orders:
    def delete_unfinished_order(self, order: Order):
        cursor = self.connection.cursor()
        logger_str = f"EXEC DELETE_ORDER_FROM_CART {order.order_id}"
        cursor.execute("EXEC DELETE_ORDER_FROM_CART  ?", order.order_id)
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    def delete_all_null_orders(self):
        cursor = self.connection.cursor()
        logger_str = f"DELETE ALL NULLPRICE Orders and OrdersBooks"
        cursor.execute(
            """
            DELETE FROM OrdersBooks
            WHERE OrdersBooks.order_id IN (
            	SELECT Orders.order_id FROM Orders
            	WHERE Orders.total_price = 0
            )
            DELETE FROM Orders
            WHERE Orders.total_price = 0"""
        )
        rows_len = cursor.rowcount
        self.__log_query_rows_updated(logger_str, rows_len)
        cursor.commit()

    # GET___________________________________________
    # Books:
    def get_all_books(self) -> list[Book]:
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM Books ORDER BY book_id DESC"
        cursor.execute(logger_str)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        books = []
        for book in result:
            books.append(parse_tuple_book(book))
        return books

    def get_books_bought_by_user(self, user: User) -> list[Book]:
        # NOTICE: query returns as it seems usual Book instance,
        # but it ain't:
        # quantity field is from order within which book is
        cursor = self.connection.cursor()
        logger_str = f"SELECT Books.book_id, title, description, author, price, OrdersBooks.quantity " \
                     f"FROM Books " \
                     f"LEFT JOIN OrdersBooks ON OrdersBooks.book_id = Books.book_id " \
                     f"LEFT JOIN Orders ON Orders.order_id = OrdersBooks.order_id " \
                     f"LEFT JOIN Users ON Users.user_id = Orders.user_id " \
                     f"LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id " \
                     f" WHERE Users.user_id = {user.user_id} AND OrderStatuses.name = " \
                     f"'{OrderStatus.FINISHED.value}'"

        cursor.execute("SELECT Books.book_id, title, description, author, price, OrdersBooks.quantity "
                       "FROM Books ""LEFT JOIN OrdersBooks ON OrdersBooks.book_id = Books.book_id "
                       "LEFT JOIN Orders ON Orders.order_id = OrdersBooks.order_id "
                       "LEFT JOIN Users ON Users.user_id = Orders.user_id "
                       "LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id "
                       " WHERE Users.user_id = ? AND OrderStatuses.name = ?",
                       user.user_id,
                       OrderStatus.FINISHED.value)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        books = []
        for book in result:
            books.append(parse_tuple_book(book))
        return books

    def is_book_in_cart(self, book: Book, order_id: int):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT Books.book_id FROM Books
        JOIN OrdersBooks ON OrdersBooks.book_id = Books.book_id
        WHERE Books.book_id = ? AND OrdersBooks.order_id = ?""",
                       book.book_id,
                       order_id)
        result = cursor.fetchall()
        return True if len(result) != 0 else False

    # Orders:
    def get_all_orders(self) -> list[Order]:
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM ORDER BY order_id DESC"
        cursor.execute(logger_str)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        orders = []
        for order in result:
            orders.append(parse_tuple_order(order))
        return orders

    def get_orders_of_manager(self, manager: User):
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM Orders WHERE Orders.operator_id = {manager.user_id}"
        cursor.execute("SELECT * FROM Orders WHERE Orders.operator_id = ?",
                       manager.user_id)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        orders = []
        for order in result:
            orders.append(parse_tuple_order(order))
        return orders

    # Users:
    def get_all_users(self) -> list[User]:
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM Users"
        cursor.execute(logger_str)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        users = []
        for user in result:
            users.append(parse_tuple_user(user))
        return users

    def get_user(self, user_: User) -> User:
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM Users WHERE Users.user_id = {user_.user_id}"
        cursor.execute("SELECT * FROM Users WHERE Users.user_id = ?",
                       user_.user_id)
        user = cursor.fetchall()
        if len(user) == 0:
            return None
        self.logger.info(logger_str)
        return parse_tuple_user(user[0])

    def get_user_by_nickname(self, user: User) -> User:
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM Users WHERE Users.login = {user.login}"
        cursor.execute("SELECT * FROM Users WHERE Users.login = ?",
                       user.login)
        found_user = cursor.fetchall()
        if len(found_user) == 0:
            return None
        self.logger.info(logger_str)
        return parse_tuple_user(found_user[0])

    def get_user_by_phone(self, user: User) -> User:
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM Users WHERE Users.login = {user.phone_number}"
        cursor.execute("SELECT * FROM Users WHERE Users.login = ?",
                       user.phone_number)
        found_user = cursor.fetchall()
        if len(found_user) == 0:
            return None
        self.logger.info(logger_str)
        return parse_tuple_user(user[0])

    def get_users_selected_role(self, role: Role) -> list[User]:
        cursor = self.connection.cursor()
        logger_str = f"SELECT " \
                     f"Users.user_id," \
                     f"first_name," \
                     f"second_name," \
                     f"middle_name," \
                     f"phone_number," \
                     f"login," \
                     f"password," \
                     f"Users.role_id," \
                     f"is_active" \
                     f" FROM Users " \
                     f"LEFT JOIN Roles ON Roles.role_id = Users.role_id " \
                     f" WHERE Roles.name = '{role.value}'"
        cursor.execute("SELECT "
                       "Users.user_id,"
                       "first_name,"
                       "second_name,"
                       "middle_name,"
                       "phone_number,"
                       "login,"
                       "password,"
                       "Users.role_id,"
                       "is_active "
                       "FROM Users "
                       "LEFT JOIN Roles ON Roles.role_id = Users.role_id "
                       " WHERE Roles.name = ?",
                       role.value)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        users = []
        for user in result:
            users.append(parse_tuple_user(user))
        return users

    def get_users_bought_selected_book(self, book: Book, book_id: int) -> list[User]:
        cursor = self.connection.cursor()
        logger_str = f"SELECT " \
                     f"Users.user_id," \
                     f"first_name," \
                     f"second_name," \
                     f"middle_name," \
                     f"phone_number," \
                     f"login," \
                     f"password," \
                     f"Users.role_id," \
                     f"is_active" \
                     f" FROM Users " \
                     f"LEFT JOIN Roles ON Roles.role_id = Users.role_id " \
                     f"LEFT JOIN Orders ON Orders.user_id = Users.user_id " \
                     f"LEFT JOIN OrdersBooks ON OrdersBooks.order_id = Orders.order_id " \
                     f"LEFT JOIN Books ON Books.book_id = OrdersBooks.book_id " \
                     f"LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id " \
                     f" WHERE Books.book_id = {book.book_id} AND OrderStatuses.name = " \
                     f"'{OrderStatus.FINISHED.value}'"

        cursor.execute("SELECT "
                       "Users.user_id,"
                       "first_name,"
                       "second_name,"
                       "middle_name,"
                       "phone_number,"
                       "login,"
                       "Users.role_id,"
                       "is_active "
                       "FROM Users "
                       f"LEFT JOIN Roles ON Roles.role_id = Users.role_id "
                       f"LEFT JOIN Orders ON Orders.user_id = Users.user_id "
                       f"LEFT JOIN OrdersBooks ON OrdersBooks.order_id = Orders.order_id "
                       f"LEFT JOIN Books ON Books.book_id = OrdersBooks.book_id "
                       f"LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id "
                       f" WHERE Books.book_id = ? AND OrderStatuses.name = ?",
                       book.book_id,
                       OrderStatus.FINISHED.value)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        users = []
        for user in result:
            users.append(parse_tuple_user(user))
        return users

    # Modified:
    def get_base_income_between(self, start_date, end_date) -> float:
        cursor = self.connection.cursor()
        logger_str = f"SELECT SUM(total_price) FROM Orders" \
                     f"LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id" \
                     f" WHERE Orders.date >= {start_date.toPyDateTime()} AND Orders.date <= {end_date.toPyDateTime()} " \
                     f"AND OrderStatuses.name = 'Успешно завершено'"
        cursor.execute(
            "SELECT SUM(total_price) FROM Orders "
            "LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id "
            "WHERE Orders.date >= ? AND Orders.date <= ? "
            "AND OrderStatuses.name = 'Успешно завершено'",
            start_date.toPyDateTime(),
            end_date.toPyDateTime())
        income = cursor.fetchall()
        self.logger.info(logger_str)
        result = income[0][0]
        return float(result) if result is not None else 0

    def get_managers_orders_count_between(self, start_date: datetime, end_date: datetime) -> list[ManagerOrderCount]:
        cursor = self.connection.cursor()
        logger_str = f"SELECT " \
                     f"Users.user_id," \
                     f"first_name," \
                     f"second_name," \
                     f"middle_name," \
                     f"phone_number," \
                     f"login," \
                     f"password," \
                     f"Users.role_id," \
                     f"is_active," \
                     f"COUNT(*) as orders_done " \
                     f"FROM Orders " \
                     f"LEFT JOIN Users ON Users.user_id = Orders.operator_id " \
                     f"LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id " \
                     f" WHERE Orders.date >= '{start_date}' AND Orders.date <= '{end_date}' " \
                     f"AND OrderStatuses.name = '{OrderStatus.FINISHED.value}' " \
                     f"GROUP BY " \
                     f"Users.user_id," \
                     f"first_name," \
                     f"second_name," \
                     f"middle_name," \
                     f"phone_number," \
                     f"login," \
                     f"password," \
                     f"Users.role_id," \
                     f"is_active"
        cursor.execute(
            "SELECT "
            "Users.user_id,"
            "first_name,"
            "second_name,"
            "middle_name,"
            "phone_number,"
            "login,"
            "password,"
            "Users.role_id,"
            "is_active,"
            "COUNT(*) as orders_done "
            "FROM Orders "
            "LEFT JOIN Users ON Users.user_id = Orders.operator_id "
            "LEFT JOIN OrderStatuses ON OrderStatuses.status_id = Orders.status_id "
            " WHERE Orders.date >= ? AND Orders.date <= ? "
            "AND OrderStatuses.name = ? "
            "GROUP BY "
            "Users.user_id,"
            "first_name,"
            "second_name,"
            "middle_name,"
            "phone_number,"
            "login,"
            "password,"
            "Users.role_id,"
            "is_active",
            start_date,
            end_date,
            OrderStatus.FINISHED.value)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        managers_order_count = []
        for m_o_c in result:
            managers_order_count.append(parse_tuple_manager_order_count(m_o_c))
        return managers_order_count

    def get_books_number_sold_ordered(self, direction: str) -> list[BookPopularity]:
        # direction: DESC/ASC
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM BooksPopularity ORDER BY number_sold {direction}"
        cursor.execute(logger_str)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        books_num_sold = []
        for book in result:
            books_num_sold.append(parse_tuple_book_popularity(book))
        return books_num_sold

    def get_managers_order_count_ordered(self, direction: str) -> list[ManagerOrderCount]:
        # direction: DESC/ASC
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM ManagersOrdersNumber ORDER BY number_orders {direction}"
        cursor.execute(logger_str)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        managers_order_count = []
        for m_o_c in result:
            managers_order_count.append(parse_tuple_manager_order_count(m_o_c))
        return managers_order_count

    def get_managers_total_count_ordered(self, direction: str) -> list[ManagerTotalProfit]:
        # direction: DESC/ASC
        cursor = self.connection.cursor()
        logger_str = f"SELECT * FROM ManagersTotalProfit ORDER BY total_profit {direction}"
        cursor.execute(logger_str)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        managers_total_profit = []
        for m_t_p in result:
            managers_total_profit.append(parse_tuple_manager_total_profit(m_t_p))
        return managers_total_profit

    def get_order_info(self, order: Order) -> list[OrderInfo]:
        cursor = self.connection.cursor()
        logger_str = f"EXEC GET_ORDER_INFO {order.order_id}"
        cursor.execute("EXEC GET_ORDER_INFO  ?", order.order_id)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        orders_info = []
        for o_i in result:
            orders_info.append(parse_tuple_order_info(o_i))
        return orders_info

    def get_user_orders(self, user: User) -> list[Order]:
        cursor = self.connection.cursor()
        logger_str = f"EXEC GET_USER_ORDERS {user.user_id}"
        cursor.execute("EXEC GET_USER_ORDERS  ?", user.user_id)
        result = cursor.fetchall()
        self.logger.info(logger_str)
        orders = []
        for order in result:
            orders.append(parse_tuple_order(order))
        return orders

    def get_order_book_quantity(self, order_id: int, book_id: int):
        cursor = self.connection.cursor()
        logger_str = "SELECT quantity FROM OrdersBooks WHERE OrdersBooks.order_id = ? AND OrdersBooks.book_id = ?"
        cursor.execute("""SELECT quantity FROM OrdersBooks
                            WHERE OrdersBooks.order_id = ? AND OrdersBooks.book_id = ?""",
                       order_id,
                       book_id)
        quantity = cursor.fetchall()
        if len(quantity) != 1:
            return None
        self.logger.info(logger_str)
        return int(quantity[0][0])
