from random import randint, shuffle

from PIL.ImageFont import Layout
from PyQt5.QtWidgets import QLineEdit


class Box():
    def __init__(self, box_id):
        self.box_id = box_id
        self.slots = [['', '', ''], 
                 ['', '', ''], 
                 ['', '', '']]
        self.given = [[False, False, False],        #map over hint
                      [False, False, False],
                      [False, False, False]]

        
class Board():
    def __init__(self, hints):
        board_it = 1
        self.hints = hints
        print("Creating board")
        while True:
            self.boxes = [['', '', ''],
                     ['', '', ''],
                     ['', '', '']]
            box_id = 1
            for row in range(3):
                for column in range(3):
                    self.boxes[row][column] = Box(box_id)    #må lage korrekt id
                    box_id += 1
                    
            self.fill_board()
            if self.solvable():
                break
            print(f"🧠 Board {board_it} unsolvable, retrying...\n")
            board_it += 1
        print(f"Solvable board created in {board_it} attempts 🧠")
    
    @classmethod
    def from_ocr(cls, nested_board):
        board = cls(hints=0)
        for box_row in range(3):
            for box_col in range(3):
                for slot_row in range(3):
                    for slot_col in range(3):
                        value = nested_board[box_row][box_col][slot_row][slot_col]
                        if value != '':
                            board.boxes[box_row][box_col].slots[slot_row][slot_col] = value
        return board
    def solvable(self):
        import copy
        board_copy = copy.deepcopy(self)
        return board_copy.solve()
    
    def find_empty_cell(self):
        best_cell = None
        min_options = 10
        
        for box_row in range(3):
            for box_col in range(3):
                box = self.boxes[box_row][box_col]
                for slot_row in range(3):
                    for slot_col in range(3):
                        if box.slots[slot_row][slot_col] == '':                          #sjekk tom slot
                            possible_values = [num for num in range(1, 10) if self.valid(num, box_row, box_col, slot_row, slot_col)]
                            if len(possible_values) < min_options:
                                min_options = len(possible_values)
                                best_cell = (box_row, box_col, slot_row, slot_col, possible_values)
        return best_cell
    
    def solve(self):
        empty = self.find_empty_cell()
        if not empty:
            return True                                                         #hvis alle slots er fulle er brettet løst

        box_row, box_col, slot_row, slot_col, possible_values = empty
        shuffle(possible_values)
        
        for num in sorted(possible_values):
            if self.valid(num, box_row, box_col, slot_row, slot_col):           #sjekk om det er lov
                self.boxes[box_row][box_col].slots[slot_row][slot_col] = str(num)
                
                if self.solve():                                                #sjekker om brettet fortsatt er korrekt
                    return True                                                 #gå til neste slot

                self.boxes[box_row][box_col].slots[slot_row][slot_col] = ''     #backtrack: hvis det blir feil på neste fjernes forrige
                
        return False                                                            #sender til backtrack hvis alle tall er prøvd                                                                  

    def fill_board(self):
        board_hints = self.hints

        while board_hints > 0:
            box_row = randint(0,2)
            box_col = randint(0,2)
            slot_row = randint(0,2)
            slot_col = randint(0,2)

            box = self.boxes[box_row][box_col]

            if box.slots[slot_row][slot_col] == '':
                numbers = list(range(1, 10))
                shuffle(numbers)

                for num in numbers:
                    if self.valid(num, box_row, box_col, slot_row, slot_col):
                        box.slots[slot_row][slot_col] = num
                        box.given[slot_row][slot_col] = True                        #plasserer hint i map
                        board_hints -= 1
                        break
        
 
                            
    def valid(self, number, box_row, box_col, slot_row, slot_col):
        full_row = box_row * 3 + slot_row
        full_col = box_col * 3 + slot_col
        
        #Check all rows
        for col in range(9):
            b_col, s_col = divmod(col, 3)
            if self.boxes[box_row][b_col].slots[slot_row][s_col] == str(number):
                return False
        
        #Check all columns
        for row in range(9):
            b_row, s_row = divmod(row, 3)
            if self.boxes[b_row][box_col].slots[s_row][slot_col] == str(number):
                return False
        
        #Check box
        for r in range(3):
            for c in range(3):
                if self.boxes[box_row][box_col].slots[r][c] == str(number):
                    return False
        
        #Is valid
        return True
        
        # # check for box
        # if number in [num for row in self.boxes[box_row][box_col].slots for num in row]:
        #     # print(f"❌ {number} already in box ({box_row}, {box_col})")                  #debug
        #     return False
        # #check for row
        # for col in range(3):
        #     if number in [self.boxes[box_row][col].slots[slot_row][c] for c in range(3)]:
        #         # print(f"❌ {number} already in row {slot_row}")                          #debug
        #         return False
        # 
        # #check for column
        # for row in range(3):
        #     if number in [self.boxes[row][box_col].slots[r][slot_col] for r in range(3)]:
        #         # print(f"❌ {number} already in column {slot_col}")                       #debug
        #         return False
        # return True

def check_answer(board, board_widget):
    layout = board_widget.layout()
    board.solve()
    for box_row in range(3):
        for box_col in range(3):
            box = board.boxes[box_row][box_col]
            frame = layout.itemAtPosition(box_row, box_col).widget()
            frame_layout = frame.layout()
            
            for slot_row in range(3):
                for slot_col in range(3):
                    widget = frame_layout.itemAtPosition(slot_row, slot_col). widget()
                    correct_value = box.slots[slot_row][slot_col]
                    
                    if isinstance(widget, QLineEdit):
                        user_input = widget.text()
                        if user_input == str(correct_value):
                            widget.setStyleSheet("font-size: 25px;"
                                                 "font-family: Arial;"
                                                 "background-color: #c0ff8b;"
                                                 "max-height: 50px;"
                                                 "max-width: 50px;")
                        else:
                            widget.setStyleSheet("font-size: 25px;"
                                                 "font-family: Arial;"
                                                 "background-color: #ff737b;"
                                                 "max-height: 50px;"
                                                 "max-width: 50px;")