import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QAbstractScrollArea, QWidget

import dataInfo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Test application")
        self.setGeometry(300, 300, 500, 400)
        # Create database session
        self.session = dataInfo.initDataBase()
        test = dataInfo.Costs("Bike", 500, "No comments :C")
        self.session.add(test)
        self.widget = QWidget()
        self.createTable()
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.table)
        self.setCentralWidget(self.widget)

        self.show()
    
    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setRowCount(40)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Bought", "Amount", "Comment"])
        
        all_boughts = self.session.query(dataInfo.Costs).all()
        self.last_row = 0
        for bought in all_boughts:
            self.table.setItem(self.last_row, 0, QTableWidgetItem(str(bought.date)))
            self.table.setItem(self.last_row, 1, QTableWidgetItem(bought.bought_thing))
            self.table.setItem(self.last_row, 2, QTableWidgetItem(str(bought.amount)))
            self.table.setItem(self.last_row, 3, QTableWidgetItem(bought.comment))
            self.last_row += 1
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
