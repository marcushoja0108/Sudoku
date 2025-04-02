import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from board import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(2400, 500, 500, 500)
        self.setWindowTitle("Sudoku")
        self.initUI()

    def initUI(self):       
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        self.board = Board()
        self.grid = BoardGrid(self.board)
        layout.addLayout(self.grid)
        
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-color: hsl(30, 100%, 98%);")
        self.setStyleSheet("""
            QPushButton{
                max-width: 40px;
                max-height: 40px;
            }
            font-family: Arial;
        """)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()