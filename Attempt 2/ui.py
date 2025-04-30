from board import *
from OCR import *
from utility import *
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QFrame,
                             QVBoxLayout, QSlider, QLabel, QLineEdit, QFileDialog, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread


def finish_ocr(window, ocr_slots):
    if ocr_slots:
        board = Board.from_ocr(ocr_slots)
        window.board = board
        window.layout.removeWidget(window.board_widget)
        window.board_widget.setParent(None)
    
        window.board_widget = create_board(board)
        window.layout.insertWidget(1, window.board_widget)
        window.confirm_button.show()
    window.overlay.hide_overlay()
    
def create_board(board):
    widget = QWidget()
    layout = QGridLayout()
    
    for box_row in range(3):
        for box_col in range(3):
            box = board.boxes[box_row][box_col]
            
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setStyleSheet("border: 2px solid hsl(35, 1%, 42%);"
                                "background-color: #f7f2e6;")
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
                        if number != '':
                            btn.setText(str(number))
                        btn.setStyleSheet("font-size: 25px;"
                                          "qproperty-alignment: AlignCenter;"
                                          "background-color: white;")
                    btn.setFixedSize(50,50)
                    frame_layout.addWidget(btn, slot_row, slot_col)
            layout.addWidget(frame, box_row, box_col)
    
    widget.setLayout(layout)
    return widget

def create_solve_button():
    solve_button = QPushButton("Solve board")
    solve_button.setStyleSheet("""
       QPushButton {
           font-size: 22px;
           font-family: Arial;
           padding: 10px 20px;
           border-radius: 8px;
           color: white;
           background-color: #0071bd;
       }
       QPushButton:hover {
            background-color: #0099ff;
       }
    """)
    solve_button.setFixedWidth(225)
    return solve_button

def create_new_board_button():
    new_board_button = QPushButton("New game")
    new_board_button.setStyleSheet("""
       QPushButton {
           font-size: 22px;
           font-family: Arial;
           padding: 10px 20px;
           border-radius: 8px;
           color: white;
           background-color: #05bf02;
       }
       QPushButton:hover {
            background-color: #07fa02;
       }
    """)
    new_board_button.setFixedWidth(225)
    return new_board_button

def create_check_button():
    check_button = QPushButton("Check answer")
    check_button.setStyleSheet("""
       QPushButton {
           font-size: 22px;
           font-family: Arial;
           padding: 10px 20px;
           border-radius: 8px;
           color: white;
           background-color: #6f00c4;
       }
       QPushButton:hover {
            background-color: #9000ff;
       }
    """)
    check_button.setFixedWidth(225)
    return check_button
    
def create_hint_slider(window):
    hint_slider = QSlider(Qt.Horizontal)
    hint_slider.setMinimum(17)
    hint_slider.setMaximum(40)
    hint_slider.setTickInterval(1)
    hint_slider.setTickPosition(QSlider.TicksBelow)
    hint_slider.setValue(window.hints)
    return hint_slider

def create_load_board_button():
    load_board = QPushButton("Load board")
    load_board.setStyleSheet("""
       QPushButton {
           font-size: 22px;
           font-family: Arial;
           padding: 10px 20px;
           border-radius: 8px;
           color: white;
           background-color: #c9a500;
       }
       QPushButton:hover {
            background-color: #ffd000;
       }
    """)
    load_board.setFixedWidth(225)
    return load_board
    
def create_confirm_board_button():
    confirm_button = QPushButton("Confirm Board")
    confirm_button.setStyleSheet("""
       QPushButton {
           font-size: 22px;
           font-family: Arial;
           padding: 10px 20px;
           border-radius: 8px;
           color: white;
           background-color: #d10000;
       }
       QPushButton:hover {
            background-color: #ff0000;
       }
    """)
    confirm_button.setFixedWidth(225)
    return confirm_button

def create_buttons(window):
    buttons = QWidget()
    main_layout = QVBoxLayout()
    
    #Game controls
    controls_layout = QHBoxLayout()
    new_board = create_new_board_button()
    load_board = create_load_board_button()
    confirm_loaded = create_confirm_board_button()
    confirm_loaded.hide()
    window.confirm_button = confirm_loaded
    
    controls_layout.addWidget(new_board)
    controls_layout.addWidget(load_board)
    controls_layout.addWidget(confirm_loaded)
    
    #hint slider
    hint_slider = create_hint_slider(window)
    hint_label = QLabel()
    def update_hint_label(value):
        if value >= 35:
            hint_label.setText(f"Hints: {hint_slider.value()} - May take som time")
        else:
            hint_label.setText(f"Hints: {hint_slider.value()}")
    
    update_hint_label(hint_slider.value())
    hint_label.setStyleSheet("font-size: 22px;"
                          "font-family: Arial;")
    
    hint_slider.valueChanged.connect(update_hint_label)
    hint_slider.valueChanged.connect(window.update_hints)
    
    hint_layout = QVBoxLayout()
    hint_layout.addWidget(hint_label, alignment=(Qt.AlignCenter))
    hint_layout.addWidget(hint_slider)
    
    #Action buttons
    actions_layout = QHBoxLayout()
    solve = create_solve_button()
    check = create_check_button()
    actions_layout.addWidget(check)
    actions_layout.addWidget(solve)
    
    #Connect
    solve.clicked.connect(lambda: solve_board(window.board, window.board_widget))
    check.clicked.connect(lambda: check_answer(window.board, window.board_widget))
    new_board.clicked.connect(window.new_game)
    load_board.clicked.connect(lambda: upload_and_process_image(window))
    confirm_loaded.clicked.connect(lambda: confirm_loaded_board(window))
    
    #Full layout
    main_layout.addLayout(controls_layout)
    main_layout.addLayout(hint_layout)
    main_layout.addLayout(actions_layout)
    buttons.setLayout(main_layout)
    
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

def upload_and_process_image(window):
    file_path, _ = QFileDialog.getOpenFileName(None, "Select Sudoku Image", "", "Images (*.png *.jpg * .jpeg)")
    if file_path:
        window.overlay.show_overlay()
        window.ocr_thread = OCRThread(file_path)
        window.ocr_thread.ocr_done.connect(lambda ocr_slots: finish_ocr(window, ocr_slots))
        window.ocr_thread.start()

def confirm_loaded_board(window):
    layout = window.board_widget.layout()
    for box_row in range(3):
        for box_col in range(3):
            box = window.board.boxes[box_row][box_col]
            frame = layout.itemAtPosition(box_row, box_col).widget()
            frame_layout = frame.layout()
            
            for slot_row in range(3):
                for slot_col in range(3):
                    widget = frame_layout.itemAtPosition(slot_row, slot_col).widget()
                    
                    val = ''
                    if isinstance(widget, QLineEdit):
                        text = widget.text().strip()
                        if text.isdigit():
                            val = text
                    elif isinstance(widget, QLabel):
                        text = widget.text().strip()
                        if text.isdigit():
                            val = text
                    
                    box.slots[slot_row][slot_col] = val
                    box.given[slot_row][slot_col] = bool(val)
    print("\n🧾 Confirmed Custom Board (9x9):")
    for box_row in range(3):
        for slot_row in range(3):
            row = []
            for box_col in range(3):
                row.extend(window.board.boxes[box_row][box_col].slots[slot_row])
            print(" ".join(cell if cell != '' else '.' for cell in row))                
            
    window.layout.removeWidget(window.board_widget)
    window.board_widget.setParent(None)
    
    window.board_widget = create_board(window.board)
    window.layout.insertWidget(1, window.board_widget)
    window.confirm_button.hide()
                    
