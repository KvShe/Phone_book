import sys
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView, QVBoxLayout, QWidget, QLineEdit,\
                            QFileDialog
from PyQt6.QtCore import Qt
from file_management import write_in_txt, write_in_csv, file_read_txt, file_read_csv
from database import contact_list


def error():
    err = QMessageBox()
    err.setWindowTitle('Error')
    err.setText('Выбран не верный формат файла')
    err.exec()


def create_view(title, model):
    view = QTableView()
    view.verticalHeader().hide()
    view.setModel(model)
    view.setWindowTitle(title)
    return view


class Contacts(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Контакты')

        font = QtGui.QFont('Monotype Corsiva')
        font.setPointSize(16)

        self.search = QLineEdit(self)
        self.search.setFont(font)
        self.search.setGeometry(5, 25, 390, 30)
        self.search.setPlaceholderText('Поиск')  # Добавляет placeholder
        self.search.returnPressed.connect(self.find_item)

        font.setPointSize(13)

        self.model = QSqlTableModel(self)
        self.model.setTable("phonebook")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.select()

        self.view_table = QTableView()
        self.view_table.setModel(self.model)
        [self.view_table.setColumnWidth(i, 128) for i in range(3)]
        self.view_table.setFont(font)

        self.button = [QtWidgets.QPushButton(self) for _ in range(4)]
        self.button_setting(0, 'Новый контакт', font)
        self.button_setting(1, 'Удалить контакт', font)
        self.button_setting(2, 'Импортировать контакты', font)
        self.button_setting(3, 'Экспортировать контакты', font)

        self.button[0].clicked.connect(self.add_row)
        self.button[1].clicked.connect(self.delete_contact)
        self.button[2].clicked.connect(self.import_contacts)
        self.button[3].clicked.connect(self.export_contacts)

        layout = QVBoxLayout()
        layout.addWidget(self.search)
        layout.addWidget(self.view_table)
        [layout.addWidget(self.button[i]) for i in range(4)]

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def find_item(self):
        item = self.search.text()
        for el in range(self.view_table.model().columnCount()):
            indexes = self.view_table.model().match(self.view_table.model().index(0, el), Qt.ItemDataRole.DisplayRole,
                                                    item, -1, Qt.MatchFlag.MatchContains)
            for ix in indexes:
                self.view_table.selectRow(ix.row())

    def button_setting(self, index, name, font):
        self.button[index].setText(name)
        self.button[index].setFont(font)

    def add_row(self):
        self.model.insertRows(self.model.rowCount(), 1)

    def delete_contact(self):
        self.model.removeRow(self.view_table.currentIndex().row())

    def import_contacts(self):
        file_name = QFileDialog.getOpenFileName(self, 'Импорт контактов', 'Name.csv')[0]
        match file_name[-3:]:
            case 'txt':
                file_read_txt(file_name)
            case 'csv':
                file_read_csv(file_name)
            case '':
                return
            case _:
                error()

    def export_contacts(self):
        file_name = QFileDialog.getOpenFileName(self, 'Экспорт контактов', 'Name.csv')[0]
        match file_name[-3:]:
            case 'txt':
                write_in_txt(file_name, contact_list())
            case 'csv':
                write_in_csv(file_name, contact_list())
            case '':
                return
            case _:
                error()


def create_connection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("phonebook.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


app = QApplication(sys.argv)
if not create_connection():
    sys.exit()

win = Contacts()
win.show()
win.setMinimumSize(450, 600)
win.setMaximumSize(450, 600)


sys.exit(app.exec())
