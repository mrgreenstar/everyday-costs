import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QAbstractScrollArea, QWidget
from PyQt5.Qt import Qt
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
        #test = dataInfo.Costs("Bike", 500, "No comments :C")
        #self.session.add(test)
        #self.session.commit()
        self.widget = QWidget()
        self.createTable()
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.table)
        self.setCentralWidget(self.widget)

        self.show()
    
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
                self.table.item(row, col).setText('')
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
