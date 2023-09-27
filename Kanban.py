from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QImage, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from WhiteLineEdit import WhiteLineEdit
import barcode
from barcode.writer import ImageWriter



class Kanban(QWidget):
    def __init__(self,  sheet, parent_frame, access):
        super().__init__()
        global wk
        wk = sheet.worksheet('Kanban')
        self.access = access
        self.parent_frame = parent_frame
        self.Gui()

    def Gui(self):
        # Layout Titolo
        title_label = QLabel("Kanban")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(30)
        title_label.setFont(title_font)

        main_layout = QVBoxLayout()

        # Crea il widget stack e aggiungi i widget da visualizzare
        self.stack = QStackedWidget()

        #crea istanze gui
        self.listkan_widget = QWidget(self)
        self.listkan_layout = QVBoxLayout()
        self.listkan_widget.setLayout(self.listkan_layout)

        self.print_widget = QWidget(self)
        self.print_layout = QVBoxLayout()
        self.listkan_widget.setLayout(self.print_layout)

        self.add_widget = QWidget(self)
        self.add_layout = QVBoxLayout()
        self.add_widget.setLayout(self.add_layout)

        self.modify_widget = QWidget(self)
        self.modify_layout = QVBoxLayout()
        self.modify_widget.setLayout(self.modify_layout)

        self.remove_widget = QWidget(self)
        self.remove_layout = QVBoxLayout()
        self.remove_widget.setLayout(self.remove_layout)

        self.search_widget = QWidget(self)
        self.search_layout = QVBoxLayout()
        self.search_widget.setLayout(self.search_layout)

        self.stack.addWidget(self.listkan_widget)
        self.stack.addWidget(self.print_widget)
        self.stack.addWidget(self.add_widget)
        self.stack.addWidget(self.modify_widget)
        self.stack.addWidget(self.remove_widget)
        self.stack.addWidget(self.search_widget)

        # Aggiungi una nuova sezione di layout contenente i pulsanti
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_widget.setLayout(button_layout)
        self.add_button = QPushButton(QIcon('icons/add.png'), '', self)
        self.add_button.setToolTip('Aggiungi')
        self.add_button.setIconSize(QSize(64, 64))
        self.modify_button = QPushButton(QIcon('icons/modify.png'), '', self)
        self.modify_button.setToolTip('Modifica')
        self.modify_button.setIconSize(QSize(64, 64))
        self.remove_button = QPushButton(QIcon('icons/remove.png'), '', self)
        self.remove_button.setToolTip('Elimina')
        self.remove_button.setIconSize(QSize(64, 64))
        self.search_button= QPushButton(QIcon('icons/search.png'), '', self)
        self.search_button.setToolTip('Cerca')
        self.search_button.setIconSize(QSize(64, 64))
        self.listkan_button= QPushButton(QIcon('icons/list.png'), '', self)
        self.listkan_button.setToolTip('Lista')
        self.listkan_button.setIconSize(QSize(64, 64))
        self.print_button = QPushButton(QIcon('icons/label.png'), '', self)
        self.print_button.setToolTip('Stampa')
        self.print_button.setIconSize(QSize(64, 64))
        button_layout.addWidget(self.listkan_button)
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.search_button)

        main_layout.addWidget(title_label)
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        if self.access == "guest":
            self.add_button.setEnabled(False)
            self.modify_button.setEnabled(False)
            self.remove_button.setEnabled(False)

        # Connetti i pulsanti del layout principale ai widget da visualizzare
        self.listkan_button.clicked.connect(self.show_list)
        self.print_button.clicked.connect(self.print_mode)
        self.add_button.clicked.connect(self.add_mode)
        self.modify_button.clicked.connect(self.modify_mode)
        self.remove_button.clicked.connect(self.remove_mode)
        self.search_button.clicked.connect(self.search)

    def update_table(self):
        # Recupera i dati dalla tabella del foglio di lavoro Kanban
        data = wk.get_all_values()[1:]  # esclude la prima riga (intestazioni delle colonne)
        self.table.setRowCount(len(data))
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # adatta la larghezza della colonna del checkbox

        # Popola la tabella con i dati recuperati
        for i, row in enumerate(data):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(i, 0, checkbox_item)
            checkbox_item.setText("")
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(i, j + 1, table_item)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.show()

    def show_list(self):
        self.show_table()
        self.update_table()

    def show_table(self):
        # tabella component
        self.table_widget = QWidget(self)
        self.table_layout = QVBoxLayout(self.table_widget)
        self.table = QTableWidget(self.table_widget)
        table_label = QLabel("Lista Kanban:")
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["", "Part-Number", "Description", "Qty"])
        self.table.setColumnHidden(0, True)
        # Lettura e visualizzazione dati da MMI
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(True)
        self.table_layout.addWidget(table_label)
        self.table_layout.addWidget(self.table)
        self.table_widget.setLayout(self.table_layout)
        self.stack.addWidget(self.table_widget)
        self.stack.setCurrentWidget(self.table_widget)
    def search(self):
        title_layout = QHBoxLayout()
        title_label = QLabel('Ricerca KANBAN')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(15)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        input_layout = QVBoxLayout()
        input_layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        form_layout.addLayout(title_layout)
        input_instructions = QLabel("Visualizzazione dati del componente:")
        form_layout.addWidget(input_instructions)

        part_number_label = QLabel("Part-Number:")
        form_layout.addWidget(part_number_label)
        self.part_number_delete = WhiteLineEdit()
        form_layout.addWidget(self.part_number_delete)

        self.cercaremove_button = QPushButton('Cerca')
        form_layout.addWidget(self.cercaremove_button)

        descrizione_label = QLabel('Descrizione:')
        self.descrizione_remove = WhiteLineEdit()
        self.descrizione_remove.setReadOnly(True)
        qty_label = QLabel('Qty:')
        self.qty_remove = WhiteLineEdit()
        self.qty_remove.setReadOnly(True)
        form_layout.addWidget(descrizione_label)
        form_layout.addWidget(self.descrizione_remove)
        form_layout.addWidget(qty_label)
        form_layout.addWidget(self.qty_remove)

        self.cercaremove_button.clicked.connect(self.search_component)

        self.search_widget = QWidget(self)
        self.search_widget.setLayout(form_layout)
        self.stack.addWidget(self.search_widget)
        self.stack.setCurrentWidget(self.search_widget)

    def add_mode(self):
        title_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        input_label = QLabel('DATI KANBAN')
        input_label.setAlignment(Qt.AlignCenter)
        input_font = QFont()
        input_font.setPointSize(15)
        input_label.setFont(input_font)
        input_layout.addWidget(input_label)
        title_layout.addLayout(input_layout)

        form_layout = QVBoxLayout()
        input_instructions = QLabel("Inserire i dati del kanban relativi al componente:")
        form_layout.addWidget(input_instructions)

        part_number_label = QLabel("Part-Number:")
        form_layout.addWidget(part_number_label)
        self.part_number_input = WhiteLineEdit()
        form_layout.addWidget(self.part_number_input)

        description_label = QLabel("Description:")
        form_layout.addWidget(description_label)
        self.description_input = WhiteLineEdit()
        form_layout.addWidget(self.description_input)

        qty_label = QLabel("Qty:")
        form_layout.addWidget(qty_label)
        self.qty_input = WhiteLineEdit()
        form_layout.addWidget(self.qty_input)

        # Creazione del pulsante per confermare l'aggiunta
        aggiungi_button = QPushButton('Aggiungi')
        aggiungi_button.clicked.connect(self.add_component)

        # Creazione del pulsante per annullare l'aggiunta
        annulla_button = QPushButton('Annulla')
        annulla_button.clicked.connect(self.cancel_add_component)
        form_layout.addWidget(aggiungi_button)
        form_layout.addWidget(annulla_button)

        self.add_widget = QWidget(self)
        self.add_widget.setLayout(form_layout)
        self.stack.addWidget(self.add_widget)
        self.stack.setCurrentWidget(self.add_widget)

    def add_component(self):
        partnumber = self.part_number_input.text()
        description = self.description_input.text()
        qty = self.qty_input.text()
        """
        # Genera il barcode
        self.generate_barcode(partnumber)
        """
        # Verifica che i campi siano stati compilati correttamente
        if partnumber and description and qty:
            try:
                if self.check_partnumber(partnumber):
                    QMessageBox.warning(self, 'Attenzione', 'Il part-number inserito esiste già nel foglio di lavoro.')
                    return
                value_list = [partnumber, description, qty]
                wk.append_row(value_list)

                # Mostra un messaggio di conferma all'utente
                QMessageBox.information(self, 'Aggiunta dati', 'I dati sono stati aggiunti correttamente.')

            except Exception as e:
                # Mostra un messaggio di errore all'utente
                QMessageBox.critical(self, 'Errore', 'Impossibile aggiungere i dati. Errore: {}'.format(str(e)))
        else:
            # Mostra un messaggio di errore all'utente se non sono stati compilati tutti i campi
            QMessageBox.warning(self, 'Attenzione', 'Compila tutti i campi per aggiungere i dati.')
        self.cancel_add_component()
        self.update_table()

        # Verifica se il part-number esiste già nel foglio di lavoro

    def check_partnumber(self, partnumber):
        range_name = 'A2:A' + str(wk.row_count)
        values = wk.get_values(range_name)
        for i, row in enumerate(values):
            if row and row[0] == partnumber:
                return i + 2
        return None

    def cancel_add_component(self):
        self.part_number_input.clear()
        self.description_input.clear()
        self.qty_input.clear()
        return

    def modify_mode(self):
        title_layout = QHBoxLayout()
        title_label = QLabel('Modifica Dati KANBAN')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(15)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        input_layout = QVBoxLayout()
        input_layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        form_layout.addLayout(title_layout)
        input_instructions = QLabel("Modifica i dati del kanban relativi al componente:")
        form_layout.addWidget(input_instructions)

        part_number_label = QLabel("Part-Number:")
        form_layout.addWidget(part_number_label)
        self.part_number_modify = WhiteLineEdit()
        form_layout.addWidget(self.part_number_modify)

        self.cerca_button = QPushButton('Cerca')
        form_layout.addWidget(self.cerca_button)

        descrizione_label = QLabel('Descrizione:')
        self.descrizione_edit = WhiteLineEdit()
        self.descrizione_edit.setReadOnly(True)
        qty_label = QLabel('Qty:')
        self.qty_edit = WhiteLineEdit()
        self.qty_edit.setReadOnly(True)
        self.salva_button = QPushButton('Salva')
        form_layout.addWidget(descrizione_label)
        form_layout.addWidget(self.descrizione_edit)
        form_layout.addWidget(qty_label)
        form_layout.addWidget(self.qty_edit)
        form_layout.addWidget(self.salva_button)

        self.cerca_button.clicked.connect(self.cerca_componente)
        self.salva_button.clicked.connect(self.salva_componente)
        self.salva_button.setEnabled(False)

        self.modify_widget = QWidget(self)
        self.modify_widget.setLayout(form_layout)
        self.stack.addWidget(self.modify_widget)
        self.stack.setCurrentWidget(self.modify_widget)

    def cerca_componente(self):
        # Recupera il part number inserito dall'utente
        part_number = self.part_number_modify.text()

        # Cerca il componente nel foglio Google Sheet
        cell = wk.find(part_number)
        if cell is None:
            QMessageBox.critical(self, 'Errore', 'Part Number non trovato!')
            self.part_number_modify.clear()
            return

        self.row = cell.row
        self.col = cell.col
        # Recupero i dati del componente e li mostro nell'interfaccia grafica
        self.descrizione_edit.setText(wk.cell(self.row, self.col+1).value)
        self.qty_edit.setText(wk.cell(self.row, self.col+2).value)
        self.descrizione_edit.setReadOnly(False)
        self.qty_edit.setReadOnly(False)
        self.salva_button.setEnabled(True)
        self.cerca_button.setEnabled(False)

    def salva_componente(self):
        # Recupero i dati modificati dall'utente
        descrizione = self.descrizione_edit.text()
        qty = self.qty_edit.text()
        wk.update_cell(row=self.row, col=self.col+1, value=descrizione)
        wk.update_cell(row=self.row, col=self.col+2, value=int(qty))
        self.close()

    #Metodi per Eliminazione Componente
    def remove_mode(self):
        title_layout = QHBoxLayout()
        title_label = QLabel('Elimina KANBAN')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(15)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        input_layout = QVBoxLayout()
        input_layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        form_layout.addLayout(title_layout)
        input_instructions = QLabel("Elimina kanban relativo al componente:")
        form_layout.addWidget(input_instructions)

        part_number_label = QLabel("Part-Number:")
        form_layout.addWidget(part_number_label)
        self.part_number_delete = WhiteLineEdit()
        form_layout.addWidget(self.part_number_delete)

        self.cercaremove_button = QPushButton('Cerca')
        form_layout.addWidget(self.cercaremove_button)

        descrizione_label = QLabel('Descrizione:')
        self.descrizione_remove = WhiteLineEdit()
        self.descrizione_remove.setReadOnly(True)
        qty_label = QLabel('Qty:')
        self.qty_remove = WhiteLineEdit()
        self.qty_remove.setReadOnly(True)
        self.remove_button = QPushButton('Elimina')
        form_layout.addWidget(descrizione_label)
        form_layout.addWidget(self.descrizione_remove)
        form_layout.addWidget(qty_label)
        form_layout.addWidget(self.qty_remove)
        form_layout.addWidget(self.remove_button)

        self.cercaremove_button.clicked.connect(self.search_component)
        self.remove_button.clicked.connect(self.confirm_delete)
        self.remove_button.setEnabled(False)

        self.remove_widget = QWidget(self)
        self.remove_widget.setLayout(form_layout)
        self.stack.addWidget(self.remove_widget)
        self.stack.setCurrentWidget(self.remove_widget)

    def search_component(self):
        self.pnumber = self.part_number_delete.text()
        if self.pnumber:
            # Cerca il componente nel foglio Google Sheet
            cell = wk.find(self.pnumber)
            if cell is None:
                QMessageBox.critical(self, 'Errore', 'Part Number non trovato!')
                self.part_number_delete.clear()
                return

            self.row = cell.row
            self.col = cell.col
            # Recupero i dati del componente e li mostro nell'interfaccia grafica
            self.descrizione_remove.setText(wk.cell(self.row, self.col + 1).value)
            self.qty_remove.setText(wk.cell(self.row, self.col + 2).value)
            self.descrizione_remove.setReadOnly(False)
            self.qty_remove.setReadOnly(False)
            self.remove_button.setEnabled(True)
            self.cercaremove_button.setEnabled(False)
        else:
            # Mostra un messaggio di errore all'utente se non è stato compilato il campo
            QMessageBox.warning(self, 'Attenzione', 'Inserisci il Part-Number del componente')

    def confirm_delete(self):
        confirm_dialog = QMessageBox()
        confirm_dialog.setWindowTitle("Conferma eliminazione")
        confirm_dialog.setText(f"Sei sicuro di voler eliminare il componente?")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        confirm_dialog.setDefaultButton(QMessageBox.Cancel)
        if confirm_dialog.exec_() == QMessageBox.Yes:
            cell = wk.find(self.pnumber)
            wk.delete_row(cell.row)
            QMessageBox.information(self, 'Eliminazione',
                                        'Componente {} eliminato con successo'.format(self.pnumber))
        else:
            self.cancel_delete_component()
            self.confirmation_edit.hide()

        self.remove_button.clicked.connect(self.confirm_delete)


    # Funzione per generare Barcode Code39

    def print_mode(self):
        self.show_table()
        button_layout = QHBoxLayout()
        button = QPushButton(self)
        self.print_button = QPushButton(QIcon('icons/print.png'), '', self)
        self.print_button.setToolTip('Print')
        self.print_button.setIconSize(QSize(64, 64))
        button_layout.addWidget(self.print_button)
        self.table_layout.addLayout(button_layout)
        self.edit_barcode()
        self.print_button.clicked.connect(self.print_barcode)

        self.update_table()

    def generate_barcode(self, code):
        # Genera il codice a barre
        Code39 = barcode.get_barcode_class('code39')
        code39 = Code39(code, writer=ImageWriter(), add_checksum=False)
        # Salva l'immagine come PNG
        code_bar = code39.save('code/'+ code)
        return code_bar

    def edit_barcode(self):
        if self.table.isColumnHidden(0):
            self.table.setColumnHidden(0, False)
            # Trasla i dati nelle rispettive colonne
            for i in range(self.table.rowCount()):
                for j in range(1, self.table.columnCount() - 1):
                    item = self.table.item(i, j)
                    self.table.setItem(i, j + 1, item)
        else:
            self.table.setColumnHidden(0, True)
            # Trasla i dati nelle rispettive colonne
            for i in range(self.table.rowCount()):
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    self.table.setItem(i, j-1, item)
        self.show()

    def print_barcode(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer)
        if dialog.exec_() == QDialog.Accepted:
            selected_rows = [i for i in range(self.table.rowCount()) if
                             self.table.item(i, 0).checkState() == Qt.Checked]
            if not selected_rows:
            # Nessuna riga selezionata
                QMessageBox.warning(self, 'Attenzione', 'Seleziona almeno un componente per il Barcode')
                return
            for i in selected_rows:
                partnumber = self.table.item(i, 1).text()
                barcode = self.generate_barcode(partnumber)
                painter = QPainter()
                painter.begin(printer)
                barcode = QImage(self.generate_barcode(partnumber))
                painter.drawImage(0,0, barcode)
                painter.end()