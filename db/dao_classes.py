import datetime
from dataclasses import dataclass
from enum import Enum


# DB TABLES:
@dataclass
class Book:
    book_id: int
    title: str
    description: str
    author: str
    price: float
    quantity: int


@dataclass
class Order:
    order_id: int
    user_id: int
    info: str
    date: datetime
    total_price: float
    operator_id: int
    status_id: int


@dataclass
class OrderBook:
    order_id: int
    book_id: int
    quantity: int


class OrderStatus(Enum):
    ACCEPTED = "Принято"
    IN_PROGRESS = "В обработке"
    CANCELLED = "Отменено"
    FINISHED = "Успешно завершено"


class Role(Enum):
    MANAGER = "Менеджер"
    ADMIN = "Администратор"
    CUSTOMER = "Покупатель"


@dataclass
class User:
    user_id: int
    first_name: str
    second_name: str
    middle_name: str
    phone_number: str
    login: str
    password: str
    role_id: int
    is_active: bool


# VIEWS:
@dataclass
class BookPopularity:
    book: Book
    number_sold: int


@dataclass
class ManagerTotalProfit:
    manager: User
    total_profit: float


@dataclass
class ManagerOrderCount:
    manager: User
    orders_done: int


@dataclass
class OrderInfo:
    order: Order
    book: Book
    quantity: int


# SYSTEM FUNCTIONS
def parse_tuple_book(source: tuple) -> Book:
    return Book(*source[:6])


def parse_tuple_order(source: tuple) -> Order:
    return Order(*source[:7])


def parse_tuple_user(source: tuple) -> User:
    return User(*source[:9])


def parse_role_str(role_id: int) -> str:
    if role_id == 1:
        return "Менеджер"
    elif role_id == 2:
        return "Администратор"
    elif role_id == 3:
        return "Покупатель"


def parse_tuple_manager_order_count(source: tuple) -> ManagerOrderCount:
    return ManagerOrderCount(manager=parse_tuple_user(source[:9]), orders_done=int(source[9]))


def parse_tuple_manager_total_profit(source: tuple) -> ManagerTotalProfit:
    return ManagerTotalProfit(manager=parse_tuple_user(source[:9]), total_profit=float(source[9]))


def parse_tuple_book_popularity(source: tuple) -> BookPopularity:
    return BookPopularity(book=parse_tuple_book(source[:6]), number_sold=source[6])


def parse_tuple_order_info(source: tuple) -> OrderInfo:
    order = source[:7]
    book = source[7:13]
    quantity = source[13]
    return OrderInfo(order=parse_tuple_order(order), book=parse_tuple_book(book), quantity=quantity)
