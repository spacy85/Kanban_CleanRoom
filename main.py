import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, \
    QVBoxLayout, QSplitter, QFrame, QStackedWidget, QMessageBox, QDialog, QLineEdit, QApplication, QComboBox, \
    QSizePolicy
from PyQt5.QtGui import QIcon, QColor, QPixmap, QFont
from PyQt5.QtCore import QSize, Qt
from WhiteLineEdit import WhiteLineEdit
from GoogleSheet import connect_to_googlesheet
from Cleanroom import Cleanroom
from Kanban import Kanban
from Cleaning import Cleaning
from Clean import Clean

def set_default_font():
    font = QFont('Arial', 20)
    font.setBold(True)
    QApplication.setFont(font)

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint)

        # Ottenere le dimensioni dello schermo
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry(desktop.primaryScreen())
        width, height = 300, 300  # Dimensioni della finestra
        self.resize(width, height)
        self.move(screen_rect.center() - self.rect().center())

        # Oggetto colore grigio medio
        graymed = QColor(112, 112, 112)
        # Imposta il colore di sfondo dell'interfaccia grafica al grigio medio
        self.setStyleSheet("background-color: {}".format(graymed.name()))

        self.user_role_label = QLabel("Select User Role:")
        self.user_role_combo = QComboBox()
        self.user_role_combo.addItem("Cleaning")
        self.user_role_combo.addItem("Cleanroom")

        self.password_label = QLabel("Password:")
        self.password_edit = WhiteLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.guest_button = QPushButton("Guest")

        vbox = QVBoxLayout()
        vbox.addWidget(self.user_role_label)
        vbox.addWidget(self.user_role_combo)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_edit)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.guest_button)


        self.setLayout(vbox)

        self.login_button.clicked.connect(self.login)
        self.guest_button.clicked.connect(self.guest)

    def login(self):
        password = self.password_edit.text()
        user_role = self.user_role_combo.currentText()
        if user_role == "Cleaning" and password == "***":
            self.accept()
            self.access = "cleaning"
        elif user_role == "Cleanroom" and password == "###":
            self.accept()
            self.access = "cleanroom"
        else:
            QMessageBox.warning(self, "Warning", "Invalid username or password")

    def guest(self):
        self.accept()
        self.access = "guest"


class HomePage(QMainWindow):
    def __init__(self, access_type):
        super().__init__()

        self.access = access_type
        self.initUI()

    def initUI(self):
        global sheet
        sheet = connect_to_googlesheet()
        self.setWindowTitle("CleanTrack")
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # Ottenere le dimensioni dello schermo
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry(desktop.primaryScreen())

        # Imposta le dimensioni e la posizione della finestra
        width, height =800, 600  # Dimensioni della finestra
        self.resize(width, height)
        self.move(screen_rect.center() - self.rect().center())

        # Oggetto colore grigio medio
        graymed = QColor(140, 140, 140)
        # Imposta il colore di sfondo dell'interfaccia grafica al grigio medio
        self.setStyleSheet("background-color: {}".format(graymed.name()))

        # Layout principale verticale
        main_layout = QHBoxLayout()

        # Crea un QStackedWidget come widget principale
        self.stacked_widget = QStackedWidget()

        # Imposta l'immagine iniziale come logo
        self.set_initial_image()

        # Crea tutte le istanze delle tue GUI come QWidget e aggiungile al QStackedWidget
        self.cleanroom_widget = QWidget(parent=self.stacked_widget)
        self.cleanroom = Cleanroom(sheet, self.cleanroom_widget.layout(), self.access)
        self.stacked_widget.addWidget(self.cleanroom)

        self.kanban_widget = QWidget(parent=self.stacked_widget)
        self.kanban = Kanban(sheet, self.kanban_widget.layout(), self.access)
        self.stacked_widget.addWidget(self.kanban)

        self.cleaning_widget = QWidget(parent=self.stacked_widget)
        self.cleaning = Cleaning(sheet, self.cleaning_widget.layout(), self.access)
        self.stacked_widget.addWidget(self.cleaning)

        self.clean_widget = QWidget(parent=self.stacked_widget)
        self.clean = Clean(sheet, self.clean_widget.layout(), self.access)
        self.clean_widget.setLayout(QVBoxLayout())
        self.stacked_widget.addWidget(self.clean)

        # Crea un widget per l'icona/logo
        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)
        logo_label = QLabel()
        logo_pixmap = QPixmap('icons/logo.png')
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        logo_layout.setAlignment(Qt.AlignCenter)
        # Pulsanti e le relative icone
        self.cleanroom_button = QPushButton(QIcon('icons/cleanroom.png'), '', self)
        self.cleanroom_button.setToolTip('CleanRoom')
        self.cleanroom_button.setIconSize(QSize(0.1 * self.width(), 0.1 * self.height()))
        self.cleanroom_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cleaning_button = QPushButton(QIcon('icons/cleaning.png'), '', self)
        self.cleaning_button.setToolTip('Cleaning')
        self.cleaning_button.setIconSize(QSize(0.1 * self.width(), 0.1 * self.height()))
        self.cleaning_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clean_button = QPushButton(QIcon('icons/clean.png'), '', self)
        self.clean_button.setToolTip('Clean')
        self.clean_button.setIconSize(QSize(0.1 * self.width(), 0.1 * self.height()))
        self.clean_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.kanban_button = QPushButton(QIcon('icons/kanban.png'), '', self)
        self.kanban_button.setToolTip('Kanban')
        self.kanban_button.setIconSize(QSize(0.1 * self.width(), 0.1 * self.height()))
        self.kanban_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exit_button = QPushButton(QIcon('icons/exit.png'), '', self)
        self.exit_button.setToolTip('Chiudi')
        self.exit_button.setIconSize(QSize(0.1*self.width(), 0.1*self.height()))
        self.exit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exit_button.clicked.connect(QApplication.quit)

        # Aggiungi i pulsanti al layout verticale
        vbox = QVBoxLayout()
        # Aggiungi il widget dell'icona sopra il layout verticale dei pulsanti
        vbox.insertWidget(0, logo_widget)
        vbox.addWidget(self.cleanroom_button)
        vbox.addWidget(self.cleaning_button)
        vbox.addWidget(self.clean_button)
        vbox.addWidget(self.kanban_button)
        vbox.addWidget(self.exit_button)

        # Crea un widget vuoto con un layout grid e aggiungi il layout verticale al centro del grid
        center_widget = QWidget()
        grid_layout = QGridLayout(center_widget)
        grid_layout.addLayout(vbox, 0, 0, Qt.AlignCenter)

        # Crea un widget splitter con un frame verticale e il widget vuoto creato sopra come primi due widget
        splitter = QSplitter(Qt.Vertical)
        frame = QFrame(splitter)
        frame.setFrameShape(QFrame.HLine)
        splitter.addWidget(frame)
        splitter.addWidget(center_widget)

        # Aggiungi il widget splitter come secondo widget del layout principale
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.stacked_widget)

        # Crea un widget centrale e aggiungi il layout principale ad esso
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect pulsanti ai metodi show_widget
        self.cleanroom_button.clicked.connect(lambda: self.show_widget(0))
        self.kanban_button.clicked.connect(lambda: self.show_widget(1))
        self.cleaning_button.clicked.connect(lambda: self.show_widget(2))
        self.clean_button.clicked.connect(lambda: self.show_widget(3))

    def show_widget(self, index):
        """
        Mostra il widget corrispondente all'indice specificato nel QStackedWidget
        """
        # Rimuovi il widget del QLabel se presente
        if isinstance(self.stacked_widget.currentWidget(), QLabel):
            self.remove_initial_image()
        self.stacked_widget.setCurrentIndex(index)

    def set_initial_image(self):
        # Crea un QLabel con un'immagine di sfondo
        label = QLabel(self)
        pixmap = QPixmap('icons/CleanTrack.png')
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        # Aggiungi il QLabel come widget principale del QStackedWidget
        self.stacked_widget.addWidget(label)
        self.stacked_widget.setCurrentWidget(label)

    def remove_initial_image(self):
        # Rimuovi il widget del QLabel dal QStackedWidget
        self.stacked_widget.removeWidget(self.stacked_widget.widget(0))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_default_font()
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        access_type = login.access
        window = HomePage(access_type)
        window.show()
    sys.exit(app.exec_())