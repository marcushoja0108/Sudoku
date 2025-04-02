from random import randint

class Box():
    def __init__(self, box_id):
        self.box_id = box_id
        self.slots = [['', '', ''], 
                 ['', '', ''], 
                 ['', '', '']]
        # for row in range(3):
        #     for column in range(3):
        #         number = randint(1, 9)
        #         self.slots[row][column] = randint(1,9)

        
class Board():
    def __init__(self):
        self.boxes = [['', '', ''],
                 ['', '', ''],
                 ['', '', '']]
        box_id = 1
        for row in range(3):
            for column in range(3):
                self.boxes[row][column] = Box(box_id)    #må lage korrekt id
                box_id += 1
    
    def solve(self):
        for box_row in range(3):
            for box_col in range(3):
                box = self.boxes[box_row][box_col]
    
                for slot_row in range(3):
                    for slot_col in range(3):
                        if box.slots[slot_row][slot_col] == '':                             #sjekk tom slot
                            for num in range(1, 10):                                        #prøv tall fra 1-9
                                if self.valid(num, box_row, box_col, slot_row, slot_col):   #sjekk om det er lov
                                   box.slots[slot_row][slot_col] = num                      
                                   
                                   if self.solve():                                         #sjekker om brettet fortsatt er korrekt
                                       return True                                          #gå til neste slot
                                    
                                   box.slots[slot_row][slot_col] = ''                       #backtrack: hvis det blir feil på neste fjernes forrige
                            return False                                                    #sender til backtrack hvis alle tall er prøvd
        return True                                                                         #hvis alle slots er fulle er brettet løst

    def fill_board(self):
        self.solve()


    def valid(self, number, box_row, box_col, slot_row, slot_col):
        # check for box
        if number in [num for row in self.boxes[box_row][box_col].slots for num in row]:
            return False
        #check for row

        for col in range(3):
            if number in [self.boxes[box_row][col].slots[slot_row][c] for c in range(3)]:
                return False

        #check for column
        for row in range(3):
            if number in [self.boxes[row][box_col].slots[r][slot_col] for r in range(3)]:
                return False
        return True
                                