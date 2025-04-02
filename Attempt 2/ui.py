from board import *
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QFrame


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
                    btn = QPushButton(str(number))
                    btn.setStyleSheet("max-height: 50px;"
                                      "max-width: 50px;")
                    frame_layout.addWidget(btn, slot_row, slot_col)
            layout.addWidget(frame, box_row, box_col)
    
    widget.setLayout(layout)
    return widget

def create_solve_button(window):
    solve_button = QPushButton("Click to solve board")
    solve_button.setStyleSheet("font-size: 50px;"
                               "font-family: Arial;"
                               "background-color: green;")
    return solve_button

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