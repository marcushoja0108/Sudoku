from board import *
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QFrame, QVBoxLayout, QSlider, QLabel, QLineEdit
from PyQt5.QtCore import Qt

def create_board(board):
    widget = QWidget()
    layout = QGridLayout()
    
    for box_row in range(3):
        for box_col in range(3):
            box = board.boxes[box_row][box_col]
            
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setStyleSheet("border: 2px solid hsl(35, 1%, 42%);")
            frame_layout = QGridLayout()
            frame.setLayout(frame_layout)
            
            for slot_row in range(3):
                for slot_col in range(3):
                    number = box.slots[slot_row][slot_col]
                    if box.given[slot_row][slot_col]:
                        btn = QLabel(str(number))
                        btn.setStyleSheet("background-color: lightgray;"
                                          "font-weight: bold;"
                                          "font-size: 25px;"
                                          "qproperty-alignment: AlignCenter;"
                                          "font-family: Arial;")
                        
                    else:
                        btn = QLineEdit()
                        btn.setMaxLength(1)
                        btn.setStyleSheet("background-color: white;")
                        if number != '':
                            btn.setText(str(number))
                        btn.setStyleSheet("font-size: 25px;"
                                          "qproperty-alignment: AlignCenter;")
                    btn.setFixedSize(50,50)
                    frame_layout.addWidget(btn, slot_row, slot_col)
            layout.addWidget(frame, box_row, box_col)
    
    widget.setLayout(layout)
    return widget

def create_solve_button():
    solve_button = QPushButton("Click to solve board")
    solve_button.setStyleSheet("font-size: 25px;"
                               "font-family: Arial;"
                               "background-color: lightgreen;")
    solve_button.setFixedWidth(225)
    return solve_button

def create_new_board_button():
    new_board_button = QPushButton("New game")
    new_board_button.setStyleSheet("font-size: 25px;"
                                   "font-family: Arial;"
                                   "background-color: lightblue;")
    new_board_button.setFixedWidth(225)
    return new_board_button

def create_check_button():
    check_button = QPushButton("Check answer")
    check_button.setStyleSheet("font-size: 25px;"
                               "font-family: Arial;"
                               "background-color: lightyellow;")
    return check_button
    
def create_hint_slider(window):
    hint_slider = QSlider(Qt.Horizontal)
    hint_slider.setMinimum(17)
    hint_slider.setMaximum(35)
    hint_slider.setTickInterval(1)
    hint_slider.setTickPosition(QSlider.TicksBelow)
    hint_slider.setValue(window.hints)
    return hint_slider
    
def create_buttons(window):
    buttons = QWidget()
    layout = QVBoxLayout()
    new_board = create_new_board_button()
    check = create_check_button()
    solve = create_solve_button()
    hint_slider = create_hint_slider(window)
    hint_label = QLabel(f"Hints: {hint_slider.value()}")
    hint_label.setStyleSheet("font-size: 25px;"
                          "font-family: Arial;")
    
    
    hint_slider.valueChanged.connect(lambda value: hint_label.setText(f"Hints: {value}"))
    solve.clicked.connect(lambda: solve_board(window.board, window.board_widget))
    check.clicked.connect(lambda: check_answer(window.board, window.board_widget))
    new_board.clicked.connect(window.new_game)
    hint_slider.valueChanged.connect(window.update_hints)
    
    layout.addWidget(hint_label, alignment=(Qt.AlignCenter))
    layout.addWidget(hint_slider)
    layout.addWidget(new_board, alignment=(Qt.AlignCenter))
    layout.addWidget(check, alignment=(Qt.AlignCenter))
    layout.addWidget(solve, alignment=(Qt.AlignCenter))
    buttons.setLayout(layout)
    
    return buttons

def print_board(self):
    """ Print board in a readable format """
    for box_row in range(3):
        for slot_row in range(3):
            row = []
            for box_col in range(3):
                row.extend(self.boxes[box_row][box_col].slots[slot_row])
            print(" ".join(str(x) if x != '' else '.' for x in row))
        if box_row < 2:
            print("-" * 21)  # Separate 3x3 sections
            
def solve_board(board, board_widget):
    if board.solve():
        update_board(board, board_widget)
        check_answer(board, board_widget)
    else:
        print("Brain damage")

def update_board(board, board_widget):
    layout = board_widget.layout()
    
    for box_row in range(3):
        for box_col in range(3):
            box = board.boxes[box_row][box_col]
            frame = layout.itemAtPosition(box_row, box_col).widget()
            frame_layout = frame.layout()
            
            for slot_row in range(3):
                for slot_col in range(3):
                    number = box.slots[slot_row][slot_col]
                    btn = frame_layout.itemAtPosition(slot_row, slot_col).widget()
                    btn.setText(str(number))
