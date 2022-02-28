from PyQt5.QtWidgets import QVBoxLayout, QWidget

from ui.widget_classes.book_widget import BookWidget


class AddBookWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, book, current_user, db, config):
        super().__init__()
        layout = QVBoxLayout()
        self.new_book = BookWidget(book=book, current_user=current_user, db=db,
                                   config=config)
        layout.addWidget(self.new_book)
        self.new_book.finish_add_new_book.show()
        self.new_book.save_changes.hide()
        if current_user.role_id == 2:
            self.new_book.delete_button.hide()
            self.new_book.sold.hide()
            self.new_book.number_sold.hide()
        self.setLayout(layout)
