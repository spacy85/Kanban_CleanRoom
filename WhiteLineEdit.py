from PyQt5.QtWidgets import QLineEdit

class WhiteLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(WhiteLineEdit, self).__init__(parent)
        self.setStyleSheet("background-color: white;")
