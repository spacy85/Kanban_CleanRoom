from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QPoint, QTimer
from datetime import datetime


class Cleaning(QWidget):
    def __init__(self, sheet, parent_frame, access):
        super().__init__()
        global wc
        global axess
        axess = access
        self.last_operation = None
        wc = sheet.worksheet('Clean')
        self.data = []
        self.parent_frame = parent_frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.Gui()

    def start_timer(self, interval_seconds):
        # Avvia il timer per aggiornare la tabella ogni tot secondi
        self.timer.start(interval_seconds * 1000)

    def stop_timer(self):
        # Ferma il timer
        self.timer.stop()



    def Gui(self):
        # Layout Titolo
        input_layout = QVBoxLayout()
        input_label = QLabel("Cleaning")
        input_label.setAlignment(Qt.AlignCenter)
        input_font = QFont()
        input_font.setPointSize(30)
        input_label.setFont(input_font)
        input_layout.addWidget(input_label)

        # Oggetto QPixmap con l'immagine da visualizzare
        pixmap = QPixmap('icons/right.png')
        # Crea un QLabel e imposta l'immagine come pixmap
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        # Aggiungi una nuova sezione di layout contenente i pulsanti
        button_layout = QHBoxLayout()
        self.edit_button = QPushButton(QIcon('icons/edit.png'), '', self)
        self.edit_button.setToolTip('Modifica')
        self.edit_button.setIconSize(QSize(64, 64))
        self.edit_button.setEnabled(True)
        self.wash_button = QPushButton(QIcon('icons/washing.png'), '', self)
        self.wash_button.setToolTip('Lavaggio')
        self.wash_button.setIconSize(QSize(64, 64))
        self.wash_button.setEnabled(False)
        self.dry_button = QPushButton(QIcon('icons/dry.png'), '', self)
        self.dry_button.setToolTip('Asciugatura')
        self.dry_button.setIconSize(QSize(64, 64))
        self.dry_button.setEnabled(False)
        self.passbox_button = QPushButton(QIcon('icons/passbox.png'), '', self)
        self.passbox_button.setToolTip('Passbox')
        self.passbox_button.setIconSize(QSize(64, 64))
        self.passbox_button.setEnabled(False)

        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.image_label)
        button_layout.addWidget(self.wash_button)
        button_layout.addWidget(self.dry_button)
        button_layout.addWidget(self.passbox_button)

        self.edit_button.clicked.connect(self.edit_mode)
        self.wash_button.clicked.connect(self.wash_mode)
        self.dry_button.clicked.connect(self.dry_mode)
        self.passbox_button.clicked.connect(self.passbox_mode)


        # Oggetto QPixmap con l'immagine da visualizzare
        pixmap = QPixmap('icons/left.png')
        # Crea un QLabel e imposta l'immagine come pixmap
        self.image1_label = QLabel()
        self.image1_label.setPixmap(pixmap)
        # Aggiungi una nuova sezione di layout contenente i pulsanti
        button_layout1= QHBoxLayout()
        self.undo_button = QPushButton(QIcon('icons/undo.png'), '', self)
        self.undo_button.setToolTip('Anulla')
        self.undo_button.setIconSize(QSize(64, 64))
        self.undo_button.setEnabled(True)
        self.wash1_button = QPushButton(QIcon('icons/pending.png'), '', self)
        self.wash1_button.setToolTip('Lavaggio')
        self.wash1_button.setIconSize(QSize(64, 64))
        self.wash1_button.setEnabled(False)
        self.dry1_button = QPushButton(QIcon('icons/washing.png'), '', self)
        self.dry1_button.setToolTip('Asciugatura')
        self.dry1_button.setIconSize(QSize(64, 64))
        self.dry1_button.setEnabled(False)
        self.passbox1_button = QPushButton(QIcon('icons/dry.png'), '', self)
        self.passbox1_button.setToolTip('Passbox')
        self.passbox1_button.setIconSize(QSize(64, 64))
        self.passbox1_button.setEnabled(False)

        button_layout1.addWidget(self.wash1_button)
        button_layout1.addWidget(self.dry1_button)
        button_layout1.addWidget(self.passbox1_button)
        button_layout1.addWidget(self.image1_label)
        button_layout1.addWidget(self.undo_button)

        self.undo_button.clicked.connect(self.undo_mode)
        self.wash1_button.clicked.connect(self.wash1_mode)
        self.dry1_button.clicked.connect(self.dry1_mode)
        self.passbox1_button.clicked.connect(self.passbox1_mode)

        # Tabella per visualizzare le richieste in corso
        table_layout = QVBoxLayout()
        table_label = QLabel("Richieste in corso:")
        table_layout.addWidget(table_label)
        self.requests_table = QTableWidget()
        self.requests_table.setColumnCount(6)
        self.requests_table.setHorizontalHeaderLabels(["", "Part-Number", "Description", "Qty", "Stato", "Data"])
        self.requests_table.setColumnHidden(0, True)

        # Lettura e visualizzazione dati da MMI
        self.update_table()
        self.requests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.requests_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.requests_table.setSelectionMode(QTableWidget.NoSelection)

        self.requests_table.setSortingEnabled(True)

        input_layout.addLayout(button_layout)
        input_layout.addLayout(button_layout1)
        input_layout.addLayout(table_layout)
        table_layout.addWidget(self.requests_table)

        if axess == "cleanroom" or axess == "guest":
            self.edit_button.setEnabled(False)
            self.undo_button.setEnabled(False)

        self.setLayout(input_layout)
    def update_table(self):
        self.start_timer(60)
        # Recupera i dati dalla tabella del foglio di lavoro Clean
        self.data = wc.get_all_values()[1:]  # esclude la prima riga (intestazioni delle colonne)

        # Memorizza l'indice della colonna di ordinamento corrente
        sort_column = self.requests_table.horizontalHeader().sortIndicatorSection()

        # Disabilita l'ordinamento della tabella
        self.requests_table.setSortingEnabled(False)

        # Cancella i dati presenti nella tabella
        self.requests_table.clearContents()

        self.requests_table.setRowCount(len(self.data))
        header = self.requests_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # adatta la larghezza della colonna del checkbox

        # Popola la tabella con i dati recuperati
        for i, row in enumerate(self.data):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.requests_table.setItem(i, 0, checkbox_item)
            checkbox_item.setText("")
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table_item.setTextAlignment(Qt.AlignCenter)
                self.requests_table.setItem(i, j + 1, table_item)
            if row[3] == 'Washing':
                color = QColor(255, 255, 0, 127)  # giallo pastello con opacità del 50%
            elif row[3] == 'Drying':
                color = QColor(135, 206, 250, 127)  # blu pastello con opacità del 50%
            elif row[3] == 'Passbox':
                color = QColor(0, 255, 0, 127)  # verde pastello con opacità del 50%
            else:
                color = QColor(190, 190, 190)
            for k in range(self.requests_table.columnCount()):
                self.requests_table.item(i, k).setBackground(color)
        # Ripristina l'ordinamento della tabella
        self.requests_table.setSortingEnabled(True)
        self.requests_table.horizontalHeader().setSortIndicator(sort_column, Qt.AscendingOrder)
        padding = 20
        for i in range(self.requests_table.columnCount()):
            self.requests_table.resizeColumnToContents(i)
            width = self.requests_table.columnWidth(i) + padding
            self.requests_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)
            self.requests_table.setColumnWidth(i, width)
    def edit_mode(self):
        self.wash1_button.setEnabled(False)
        self.dry1_button.setEnabled(False)
        self.passbox1_button.setEnabled(False)

        if self.requests_table.isColumnHidden(0):
            self.requests_table.setColumnHidden(0, False)
            # Trasla i dati nelle rispettive colonne
            for i in range(self.requests_table.rowCount()):
                for j in range(1, self.requests_table.columnCount() - 1):
                    item = self.requests_table.item(i, j)
                    self.requests_table.setItem(i, j + 1, item)

            self.wash_button.setEnabled(True)
            self.dry_button.setEnabled(True)
            self.passbox_button.setEnabled(True)
        else:

            self.wash_button.setEnabled(False)
            self.dry_button.setEnabled(False)
            self.passbox_button.setEnabled(False)
            self.requests_table.setColumnHidden(0, True)
            # Trasla i dati nelle rispettive colonne
            for i in range(self.requests_table.rowCount()):
                for j in range(self.requests_table.columnCount()):
                    item = self.requests_table.item(i, j)
                    self.requests_table.setItem(i, j-1, item)
        # Aggiorna la tabella
        self.update_table()

    def undo_mode(self):
        self.wash_button.setEnabled(False)
        self.dry_button.setEnabled(False)
        self.passbox_button.setEnabled(False)
        if self.requests_table.isColumnHidden(0):
            self.requests_table.setColumnHidden(0, False)
            # Trasla i dati nelle rispettive colonne
            for i in range(self.requests_table.rowCount()):
                for j in range(1, self.requests_table.columnCount() - 1):
                    item = self.requests_table.item(i, j)
                    self.requests_table.setItem(i, j + 1, item)
            self.wash1_button.setEnabled(True)
            self.dry1_button.setEnabled(True)
            self.passbox1_button.setEnabled(True)
        else:
            self.wash1_button.setEnabled(False)
            self.dry1_button.setEnabled(False)
            self.passbox1_button.setEnabled(False)
            self.requests_table.setColumnHidden(0, True)
            # Trasla i dati nelle rispettive colonne
            for i in range(self.requests_table.rowCount()):
                for j in range(self.requests_table.columnCount()):
                    item = self.requests_table.item(i, j)
                    self.requests_table.setItem(i, j - 1, item)
        # Aggiorna la tabella
        self.update_table()

    def type_mode(self, process, process1):
        selected_rows = [self.requests_table.indexAt(QPoint(0, self.requests_table.rowViewportPosition(i))).row()
                         for i in range(self.requests_table.rowCount())
                         if self.requests_table.item(i, 0).checkState() == Qt.Checked]

        if not selected_rows:
            # Nessuna riga selezionata
            QMessageBox.warning(self, 'Attenzione', 'Seleziona almeno una richiesta da elaborare')
            return

        # Controlla che tutte le righe selezionate siano nello stato "pending"
        for row in selected_rows:
            if self.requests_table.item(row, 4).text() != process:
                QMessageBox.warning(self, 'Attenzione',
                                    'Non è possibile elaborare richieste diverse da ' + process)
                return
        for i in range(self.requests_table.rowCount()):
            if self.requests_table.item(i, 0).checkState() == Qt.Checked:
                partnumber = self.requests_table.item(i, 1).text()
                part_number = wc.col_values(1)
                # Cerca il componente nella lista di part_number
                indices = [i + 1 for i, x in enumerate(part_number) if x == partnumber]
                # Cerca il primo componente con stato process a partire dall'indice trovato
                for idx in indices:
                    if wc.cell(row=idx, col=4).value == process:
                        wc.update_cell(row=idx, col=4, value=process1)
                        wc.update_cell(row=idx, col=5, value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        break
        self.update_table()
        QMessageBox.information(self, 'Aggiornamento', 'Componenti selezionati aggiornati allo stato ' + process1)
        self.edit_mode()

    def wash_mode(self):
        self.type_mode("Pending", "Washing")
    def dry_mode(self):
        self.type_mode("Washing", "Drying")
    def passbox_mode(self):
        self.type_mode("Drying", "Passbox")

    def wash1_mode(self):
        self.type_mode( "Washing", "Pending")
    def dry1_mode(self):
        self.type_mode("Drying", "Washing")
    def passbox1_mode(self):
        self.type_mode("Passbox", "Drying")
