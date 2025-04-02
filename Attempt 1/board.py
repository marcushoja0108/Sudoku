from PyQt5.QtWidgets import (QGridLayout, QPushButton, QFrame)
class Box:
    def __init__(self, box_id):
        self.box_id = box_id
        self.slots = {f"slot{slot}": None for slot in range(9)}

    def __repr__(self):
        return f"Box({self.box_id}): {self.slots}"

class Board:
    def __init__(self):
        self.boxes = {f"box{box}": Box(box) for box in range(9)}
    def __repr__(self):
        return "\n".join([f"{box}: {self.boxes[box]}" for box in self.boxes])

class BoardGrid(QGridLayout):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.draw_grid()
        
    def draw_grid(self):
        for box_id in range(9):
            box = self.board.boxes[f"box{box_id}"]
            row_offset = (box_id // 3) * 3
            col_offset = (box_id % 3) * 3
        
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setLineWidth(2)
            frame.setStyleSheet("border: 2px solid hsl(35, 1%, 42%);")
            
            box_layout = QGridLayout()
            frame.setLayout(box_layout)
            
            for slot_id in range(9):
                row = slot_id // 3
                col = slot_id % 3
                
                button = QPushButton(f"{box_id}-{slot_id}")
                box_layout.addWidget(button, row, col)
        
            self.addWidget(frame, row_offset, col_offset, 3, 3)
