import json
import logging
from logging import handlers
import qdarkstyle
import os

from db.dao_classes import User, Book
from db.database import Database

from PyQt5.QtWidgets import QApplication, QStackedWidget
import sys
from ui.authentification.welcome_ui import WelcomeScreen
from ui.roles_ui.main_window_admin import MainWindowAdmin
from ui.roles_ui.main_window_customer import MainWindowCustomer
from ui.roles_ui.main_window_manager import MainWindowManager

os.environ['QT_API'] = 'pyqt5'

database = "Bookselling_Base"
server = "WIN-5BELFCTA2DT"

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s, %(name)s, line %(lineno)s, %(message)s',
    level=logging.INFO,
    handlers=[
        logging.handlers.TimedRotatingFileHandler(filename="logs\\main.log",
                                                  backupCount=1,
                                                  when="W0"),
    ])


def main():
    config_file_name = "config.json"
    try:
        with open(config_file_name, "r", encoding="utf-8") as read_file:
            config = json.load(read_file)
    except EnvironmentError as err:
        logging.error(f"File {config_file_name} not found.")
        raise SystemExit(err)

    db = Database(dbname=config["db"]["dbname"], driver=config["db"]["driver"], server=config["db"]["server"])
    # # user
    # debug_user = User(
    #     user_id=28,
    #     first_name="Test",
    #     second_name="User",
    #     middle_name="",
    #     phone_number="88005553535         ",
    #     login="a",
    #     password="c4ca4238a0b923820dcc509a6f75849b",
    #     role_id=3,
    #     is_active=True
    # )

    # # manager
    # debug_user = User(
    #     user_id=29,
    #     first_name="Manager1",
    #     second_name="Manag",
    #     middle_name="Ma",
    #     phone_number="88888888888         ",
    #     login="m",
    #     password="c4ca4238a0b923820dcc509a6f75849b",
    #     role_id=1,
    #     is_active=True
    # )

    # admin
    debug_user = User(
        user_id=30,
        first_name="Евгений",
        second_name="Подружинский",
        middle_name="Дмитриевич",
        phone_number="+79213172188        ",
        login="admin",
        password="81dc9bdb52d04dc20036dbd8313ed055",
        role_id=2,
        is_active=True
    )

    # db.update_user(updated_user)

    # for j in range(5):
    #     book = db.add_book(
    #         Book(0, f"book#{j}", f"author#{j}", f"descr#{j}", 5*j, int(150/(j+1))))
    db.delete_all_null_orders()
    app = QApplication(sys.argv)
    app.setStyleSheet((qdarkstyle.load_stylesheet()))
    widget = QStackedWidget()

    # # debug customer
    # debug_ui = MainWindowCustomer(config=config, db=db, path_to_ui="ui/qt/customer.ui", current_user=debug_user)

    # # debug manager
    # debug_ui = MainWindowManager(config=config, db=db, path_to_ui="ui/qt/manager.ui", current_user=debug_user)

    # # debug admin
    # debug_ui = MainWindowAdmin(config=config, db=db, path_to_ui="ui/qt/admin.ui", current_user=debug_user)
    #
    # debug_ui.setFixedWidth(1000)
    # debug_ui.setFixedHeight(900)
    #
    # widget.addWidget(debug_ui)

    # # actual logic
    welcome = WelcomeScreen(widget=widget, config=config, db=db)
    widget.addWidget(welcome)

    widget.show()
    try:
        sys.exit(app.exec_())
    except RuntimeError as err:
        logging.error(err)


if __name__ == '__main__':
    main()
