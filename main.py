import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QHeaderView, QAction, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractScrollArea, QWidget, QPushButton, QLineEdit, QLabel
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
        # Create database session
        self.session = dataInfo.initDataBase()
        if not self.session:
            sys.exit()
        
        # Toolbar
        add = QAction(QIcon('static/add.png'), "Add new bought", self)
        add.triggered.connect(self.output)
        self.toolbar = self.addToolBar("Add")
        self.toolbar.addAction(add)
        
        # Table
        self.widget = QWidget()
        self.createTable()
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.table)
        self.setCentralWidget(self.widget)

        self.show()

    def output(self):
        self.add_window = DialogWindow()
    
    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Bought", "Amount", "Comment"])
        self.table.itemClicked.connect(self.cell_item_one_click_event)
        all_boughts = self.session.query(dataInfo.Costs).all()
        self.table.setRowCount(len(all_boughts))
        self.last_row = 0
        for bought in all_boughts:
            self.table.setItem(self.last_row, 0, QTableWidgetItem(str(bought.date)))
            self.table.setItem(self.last_row, 1, QTableWidgetItem(bought.bought_thing))
            self.table.setItem(self.last_row, 2, QTableWidgetItem(str(bought.amount)))
            self.table.setItem(self.last_row, 3, QTableWidgetItem(bought.comment))
            self.last_row += 1
        
        self.table_header = self.table.horizontalHeader()
        self.table_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table_header.setSectionResizeMode(3, QHeaderView.Stretch)

    def cell_item_one_click_event(self):
        row = self.table.currentRow()
        col = self.table.currentColumn()
        print("Content: {}\n".format(self.table.item(row, col).text()))
    
    def keyPressEvent(self, event):
        # To delete info from current cell
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_Backspace:
                row = self.table.currentRow()
                col = self.table.currentColumn()
                self.table.item(row, col).setText(None)

class DialogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new bought")
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)
        
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
        self.vbox = QVBoxLayout()
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

        self.widget.setLayout(self.vbox)
        self.setCentralWidget(self.widget)

        self.show()

    def on_click(self):
        print("Here")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
