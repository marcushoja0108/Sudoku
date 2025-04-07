import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFontDatabase, QFont

from ui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Time")
        self.setGeometry(2400, 400, 700, 1000)
        
        font_id = QFontDatabase.addApplicationFont("Attempt 2/fonts/curlzmt.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.logo_font = QFont(family, 50)
        else:
            print("❌ Failed to load Curlz font")
            self.logo_font = QFont("Arial", 32)
        
        self.hints = 24
        self.board = Board(self.hints)
        self.initUI()

    def initUI(self):       #UI funksjon
        self.setStyleSheet("QMainWindow {background-color: hotpink;}")
        self.logo = QLabel("Sudoku Time")
        self.logo.setFont(self.logo_font)
        self.logo.setStyleSheet("qproperty-alignment: AlignCenter;")
        self.board_widget = create_board(self.board)
        self.buttons = create_buttons(self)

        container = QWidget()
        self.layout = QVBoxLayout()

        self.buttons.setFixedHeight(200)

        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.board_widget)
        self.layout.addWidget(self.buttons)
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def new_game(self):
        self.board = Board(self.hints)

        self.layout.removeWidget(self.board_widget)
        self.board_widget.setParent(None)

        self.board_widget = create_board(self.board)
        self.layout.insertWidget(1, self.board_widget)

    def update_hints(self, value):
        self.hints = value

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()