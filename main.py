import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QHeaderView, QAction, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractScrollArea, QWidget, QPushButton, QLineEdit, QLabel, QDialog
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon

import dataInfo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Test application")
        self.setGeometry(10, 300, 500, 400)
        # Check database session
        self.session = dataInfo.SingleSession.getInstance()
        if not self.session:
            print("not session")
            sys.exit()
        
        # Toolbar
        add = QAction(QIcon('static/add.png'), "Add new bought", self)
        add.triggered.connect(self.open_add_window)
        self.toolbar = self.addToolBar("Add")
        self.toolbar.addAction(add)
        
        # Table
        self.widget = QWidget()
        self.create_table()
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.table)
        self.setCentralWidget(self.widget)

        self.show()

    def open_add_window(self):
        self.add_window = SecondWindow()
        self.add_window.exec_()
        self.refill_table()
    
    def create_table(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Bought", "Amount", "Comment", "Id"])
        self.table.itemClicked.connect(self.cell_item_one_click_event)
        self.table.setColumnHidden(4, True)
        self.refill_table()
        
        self.table_header = self.table.horizontalHeader()
        self.table_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table_header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def refill_table(self):
        # Clear table
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

        # Refill it
        all_boughts = self.session.query(dataInfo.Costs).all()
        self.table.setRowCount(len(all_boughts))
        last_row = 0
        for bought in all_boughts:
            self.table.setItem(last_row, 0, QTableWidgetItem(str(bought.date)))
            self.table.setItem(last_row, 1, QTableWidgetItem(bought.bought_thing))
            self.table.setItem(last_row, 2, QTableWidgetItem(str(bought.amount)))
            self.table.setItem(last_row, 3, QTableWidgetItem(bought.comment))
            self.table.setItem(last_row, 4, QTableWidgetItem(str(bought.id)))
            last_row += 1

    def cell_item_one_click_event(self):
        row = self.table.currentRow()
        col = self.table.currentColumn()
    
    def keyPressEvent(self, event):
        # To delete info from current cell
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_Backspace:
                delete_id = self.table.item(
                    self.table.currentRow(), self.table.columnCount() - 1).text()
                self.table.removeRow(self.table.currentRow())
                obj = self.session.query(dataInfo.Costs).filter(dataInfo.Costs.id==int(delete_id))
                obj.delete()
                self.session.commit()

class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new bought")
        self.setFixedSize(500, 250)
        
        self.widget = QWidget()
        # Add button
        self.btn = QPushButton("Add", self)
        self.btn.clicked.connect(self.on_click)
        self.date_label = QLabel("Date:")
        self.date_line = QLineEdit(str(date.today()), self)
        self.bought_thing_label = QLabel("What you bought:")
        self.bought_thing_line = QLineEdit(self)
        self.amount_label = QLabel("Amount:")
        self.amount_line = QLineEdit(self)
        self.comment_label = QLabel("Comment about bought:")
        self.comment_line = QLineEdit(self)
        # Layout
        self.vbox = QVBoxLayout(self)
        self.vbox.addStretch(1)
        # Add all lines and labels
        self.vbox.addWidget(self.date_label)
        self.vbox.addWidget(self.date_line)
        self.vbox.addWidget(self.bought_thing_label)
        self.vbox.addWidget(self.bought_thing_line)
        self.vbox.addWidget(self.amount_label)
        self.vbox.addWidget(self.amount_line)
        self.vbox.addWidget(self.comment_label)
        self.vbox.addWidget(self.comment_line)
        self.vbox.addWidget(self.btn)

        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def on_click(self):
        new_bought = dataInfo.Costs(self.bought_thing_line.text(),
            self.amount_line.text(), self.comment_line.text())
        session = dataInfo.SingleSession.getInstance()
        session.add(new_bought)
        session.commit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
