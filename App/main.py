import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFontDatabase, QFont, QIcon

from ui import *
from utility import *
from board import *

class BoardGeneratorThread(QThread):
    board_ready = pyqtSignal(object)
    def __init__(self, hints):
        super().__init__()
        self.hints = hints
    def run(self):
        board = Board(self.hints)
        self.board_ready.emit(board)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Time")
        self.setWindowIcon(QIcon('App/assets/logo.png'))
        self.setGeometry(2300, 200, 700, 900)

        self.overlay = LoadingOverlay(self)

        font_id = QFontDatabase.addApplicationFont("App/fonts/Slabo13px-Regular.ttf")
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.logo_font = QFont(family, 50)
        else:
            print("Failed to load font")
            self.logo_font = QFont("Arial", 32)

        self.hints = 24
        self.board = Board(self.hints)
        self.initUI()

    def initUI(self):       
        self.setStyleSheet("QMainWindow {background-color: #ebf0ff;}")
        self.logo = QLabel("Sudoku Time")
        self.board_widget = create_board(self.board)
        self.error_label = QLabel("")
        self.buttons = create_buttons(self)

        container = QWidget()
        self.layout = QVBoxLayout()

        self.logo.setStyleSheet("qproperty-alignment: AlignCenter;")
        self.logo.setFixedHeight(100)
        self.logo.setFont(self.logo_font)
        
        self.error_label.setStyleSheet("color: red; font-weight: bold; font-size: 20px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        self.buttons.setFixedHeight(200)

        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.board_widget)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.buttons)
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def new_game(self):
        self.error_label.hide()
        self.confirm_button.hide()
        self.solve_button.show()
        self.check_button.show()
        self.overlay.show_overlay()
        self.thread = BoardGeneratorThread(self.hints)
        self.thread.board_ready.connect(self.finish_new_game)
        self.thread.start()

    def finish_new_game(self, board):
        self.board = board
        self.layout.removeWidget(self.board_widget)
        self.board_widget.setParent(None)

        self.board_widget = create_board(self.board)
        self.layout.insertWidget(1, self.board_widget)
        self.overlay.hide_overlay()

    def update_hints(self, value):
        self.hints = value

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()