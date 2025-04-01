class Player:
    def __init__(self, king):
        self.king = king
        self.in_check = False
        self.pieces = []
