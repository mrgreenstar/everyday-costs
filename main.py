import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QAbstractScrollArea, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Test application")
        self.setGeometry(300, 300, 500, 400)
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.createTable()
        self.layout.addWidget(self.table)
        self.setCentralWidget(self.widget)

        self.show()
    
    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3"])
        self.table.setRowCount(40)
        self.table.setColumnCount(3)
        self.table.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        self.table.move(0, 0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
