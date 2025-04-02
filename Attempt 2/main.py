import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from ui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setGeometry(2400, 400, 600, 600)
        self.board = Board()
        self.initUI()

    def initUI(self):       #UI funksjon
        self.board_widget = create_board(self.board)
        solve_button = create_solve_button(self)
        
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.board_widget)
        layout.addWidget(solve_button)
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        
        def solve_board():
            self.board.solve()
            update_board(self.board, self.board_widget)
            
        solve_button.clicked.connect(solve_board)
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()