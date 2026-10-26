class keyboard:
    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0
    def move(self, x, y):
        self.x_offset += x
        self.y_offset += y
    def move_left(self):
        self.move(0, -10)
    def move_right(self):
        self.move(0, 10)
    def move_roll(self):
        self.move(0, 20)
    def move_jump(self):
        self.move(10, 0)