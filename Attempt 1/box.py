from PyQt5.QtWidgets import QPushButton

class Box:
    def __init__(self, box_id):
        self.box_id = box_id
        self.slots = {f"slot{slot}": None for slot in range(9)}

    def __repr__(self):
        return f"Box({self.box_id}): {self.slots}"