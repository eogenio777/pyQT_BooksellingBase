from PyQt5.QtWidgets import QVBoxLayout, QWidget

from ui.widget_classes.user_widget import UserWidget


class ShowUserWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, current_user, db, config, user):
        super().__init__()
        layout = QVBoxLayout()
        self.user = UserWidget(current_user=current_user, db=db,
                               config=config, viewable_user=user)
        layout.addWidget(self.user)
        self.setLayout(layout)
