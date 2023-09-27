from datetime import datetime
from WhiteLineEdit import WhiteLineEdit
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QTableWidget, QWidget, QAbstractItemView, QHeaderView


class Cleanroom(QWidget):
    def __init__(self, sheet, parent_frame, access):
        super().__init__()
        self.access = access
        global wk, wc, wnc
        wk = sheet.worksheet('Kanban')
        wc = sheet.worksheet('Clean')
        wnc = sheet.worksheet('NoClean')
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
        # Layout per l'inserimento del part-number
        input_layout = QVBoxLayout()
        input_label = QLabel("Cleanroom")
        input_label.setAlignment(Qt.AlignCenter)
        input_font = QFont()
        input_font.setPointSize(30)
        input_label.setFont(input_font)
        input_layout.addWidget(input_label)
        input_instructions = QLabel("Inserisci il part-number e invia la richiesta al Cleaning")
        input_layout.addWidget(input_instructions)

        partnumber_layout = QHBoxLayout()
        partnumber_label = QLabel("Part-Number:")
        self.partnumber_input = WhiteLineEdit()
        partnumber_layout.addWidget(partnumber_label)
        partnumber_layout.addWidget(self.partnumber_input)
        input_layout.addLayout(partnumber_layout)

        # Pulsante per inviare la richiesta di cleaning
        self.request_button = QPushButton(QIcon('icons/send.png'), '', self)
        self.request_button.setToolTip('Invia')
        self.request_button.setIconSize(QSize(64, 64))
        partnumber_layout.addWidget(self.request_button)

        # Tabella per visualizzare le richieste in corso
        table_layout = QVBoxLayout()
        table_label = QLabel("Richieste in corso:")
        self.requests_table = QTableWidget()
        self.requests_table.setColumnCount(5)
        self.requests_table.setHorizontalHeaderLabels(["Part-Number", "Description", "Qty", "Process", "Data"])
        # Lettura e visualizzazione dati da MMI
        self.update_table()
        self.requests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.requests_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.requests_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.requests_table.setSortingEnabled(True)
        table_layout.addWidget(table_label)
        table_layout.addWidget(self.requests_table)

        # Box orizzontale per rientro kanban
        input_ins = QLabel("Check del Component dal Passbox:")
        input_ins.setAlignment(Qt.AlignCenter)
        partnumber_box = QHBoxLayout()
        partnumber_box.addWidget(input_ins)
        self.partnumber_box_input = WhiteLineEdit()
        partnumber_box.addWidget(self.partnumber_box_input)
        partnumber_box_button = QPushButton(QIcon('icons/check.png'), '', self)
        partnumber_box_button.setToolTip('Registra')
        partnumber_box_button.setIconSize(QSize(45, 45))
        partnumber_box.addWidget(partnumber_box_button)

        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(partnumber_box)

        self.setLayout(main_layout)
        self.request_button.clicked.connect(self.barcode_scanned)
        partnumber_box_button.clicked.connect(self.check)

        if self.access == "cleaning" or self.access == "guest":
            self.request_button.setEnabled(False)
            partnumber_box_button.setEnabled(False)

        self.show()

    def update_table(self):
        self.start_timer(60)
        datac = wc.get_all_values()[1:]  # esclude la prima riga (intestazioni delle colonne)
        datanc = wnc.get_all_values()[1:]
        self.data = datac + datanc

        # Memorizza l'indice della colonna di ordinamento corrente
        sort_column = self.requests_table.horizontalHeader().sortIndicatorSection()

        # Disabilita l'ordinamento della tabella
        self.requests_table.setSortingEnabled(False)

        # Cancella i dati presenti nella tabella
        self.requests_table.clearContents()

        self.requests_table.setRowCount(len(self.data))
        # Popola la tabella con i dati recuperati da clean
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table_item.setTextAlignment(Qt.AlignCenter)
                table_item.setTextAlignment(Qt.AlignCenter)
                self.requests_table.setItem(i, j, table_item)
            if row[3] != 'Passbox':
                color = QColor(255, 153, 153)  # rosso pastello con opacità del 50%
            else:
                color = QColor(0, 255, 0, 127)  # verde pastello con opacità del 50%
            for k in range(self.requests_table.columnCount()):
                self.requests_table.item(i, k).setBackground(color)
        # Ripristina l'ordinamento della tabella
        self.requests_table.setSortingEnabled(True)
        self.requests_table.horizontalHeader().setSortIndicator(sort_column, Qt.AscendingOrder)
        # Adatta la larghezza delle colonne in base al contenuto
        padding = 20
        for i in range(self.requests_table.columnCount()):
            self.requests_table.resizeColumnToContents(i)
            width = self.requests_table.columnWidth(i) + padding
            self.requests_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)
            self.requests_table.setColumnWidth(i, width)

    def update_sheet_data(self):
        # Ottiene i valori della colonna "part_number"
        part_numbers = wk.col_values(1)  # considerando che "part_number" sia la prima colonna
        # Cerca il componente nella lista di part_number
        try:
            idx = part_numbers.index(self.partnumber)
        except ValueError:
            return False
        # Ottiene i valori della riga corrispondente al part_number
        clone_row = wk.row_values(idx + 1)  # aggiungere 1 perché gli indici delle righe partono da 1 in gspread
        clone_row.insert(3, "Pending")
        clone_row.insert(4, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        if 'TENDON' in clone_row[1] or 'BEARING' in clone_row[1] or 'BRAIDED' in clone_row[1]:
            wnc.append_row(clone_row)
        else:
            wc.append_row(clone_row)
        return True

    def barcode_scanned(self):
        self.requests_table.clearSelection()
        # Ottiene il part-number dal textbox
        self.partnumber = self.partnumber_input.text()
        if self.partnumber == "":
            QMessageBox.warning(self, "Attenzione", "Inserire il part-number.")
            return
        # Aggiorna il campo "Stato" nella riga del part-number
        success = self.update_sheet_data()
        if success:
            # Aggiorna la tabella delle richieste in corso
            self.update_table()
            QMessageBox.information(self, 'Invio Richiesta', 'Richiesta inviata al Cleaning')
        else:
            # Mostra un messaggio di errore
            QMessageBox.warning(self, 'Attenzione', 'Componente non trovato. '
                                                    'Non è possibile inviare la richiesta.Riprovare')
        self.partnumber_input.clear()

    def check(self):
        partnumber = self.partnumber_box_input.text()
        self.partnumber_box_input.clear()
        if not partnumber:
            QMessageBox.warning(self, "Attenzione", "Inserire il part-number.")
            return
        part_numbers1 = wc.col_values(1)
        # Cerca il componente nella lista di part_number
        indices1 = [i+1 for i, x in enumerate(part_numbers1) if x == partnumber]
        if not indices1:
            part_numbers2 = wnc.col_values(1)
            indices2 = [i + 1 for i, x in enumerate(part_numbers2) if x == partnumber]
            if not indices2:
                QMessageBox.critical(self, 'Errore', 'Componente non richiesto!')
                return
            else:
                indices = indices2
                ws = wnc
        else:
            indices = indices1
            ws = wc
        # Cerca il primo componente con stato Passbox a partire dall'indice trovato
        found = False
        for idx in indices:
            if ws.cell(row=idx, col=4).value == 'Passbox':
                ws.delete_rows(idx)
                found = True
                break
        if not found:
            QMessageBox.critical(self, 'Attenzione', 'Contattare il Cleaning per verifica stato componente')
        else:
            self.update_table()
