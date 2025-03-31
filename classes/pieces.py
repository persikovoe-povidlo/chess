import pygame

import constants
from functions import tile_to_coords


class Piece:
    def __init__(self, game, row, col, color):
        self.game = game
        self.row = row
        self.col = col
        self.color = color
        self.surface = pygame.transform.scale(pygame.Surface((0, 0)), (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(tile_to_coords(row, col))

    def draw(self, display):
        display.blit(self.surface, self.rect)

    def move(self, row, col):
        self.game.board[row][col] = self
        self.game.board[self.row][self.col] = None
        self.row = row
        self.col = col
        self.rect.topleft = (
            tile_to_coords(row, col))


class Pawn(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-pawn.png').convert_alpha()
        self.direction = -1 if color == 'white' else 1

    def can_move(self, row, col):
        if (self.row + self.direction == row and abs(self.col - col) == 1 and  # take opponent's piece
                self.game.board[row][col]):
            if self.game.board[row][col].color != self.color:
                return True
            if (self.game.last_moves[-1].piece == self.game.board[row - self.direction][col] and  # en' passant
                    self.game.last_moves[-1].row1 == (constants.BOARD_SIZE - 1 - self.direction) % (
                            constants.BOARD_SIZE - 1)):
                self.game.board[row - self.direction][col] = None
                return True
        if (self.row + self.direction == row and self.col == col and  # move forward once
                self.game.board[row][col] is None):
            return True
        if (self.row == (constants.BOARD_SIZE - 1 + self.direction) % (constants.BOARD_SIZE - 1) and  # move frwrd twice
                self.row + self.direction * 2 == row and self.col == col and
                self.game.board[self.row + self.direction][col] is None and
                self.game.board[self.row + self.direction * 2][col] is None):
            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-bishop.png').convert_alpha()

    def can_move(self, row, col):
        if self.row + self.col == row + col or self.row - self.col == row - col:  # check for diagonal movement
            for _row, _col in zip(  # check for pieces obstructing the path
                    range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1),
                    range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1)):
                if self.game.board[_row][_col]:
                    return False
            return True
        else:
            return False


class Rook(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-rook.png').convert_alpha()
        self.has_moved = False

    def can_move(self, row, col):
        if self.col == col:  # check for vertical movement
            for _row in range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1):
                if self.game.board[_row][col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.row == row:  # check for horizontal movement
            for _col in range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1):
                if self.game.board[row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-queen.png').convert_alpha()

    def can_move(self, row, col):
        if self.row + self.col == row + col or self.row - self.col == row - col:  # check for diagonal movement
            for _row, _col in zip(
                    range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1),
                    range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1)):
                if self.game.board[_row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.col == col:  # check for vertical movement
            for _row in range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1):
                if self.game.board[_row][col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.row == row:  # check for horizontal movement
            for _col in range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1):
                if self.game.board[row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        else:
            return False


class King(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-king.png').convert_alpha()
        self.has_moved = False
        self.castled = False

    def can_move(self, row, col):
        if abs(self.col - col) <= 1 and abs(self.row - row) <= 1:  # check for king movement
            return True
        if not self.castled:
            if col - self.col == 2:
                if type(self.game.board[self.row][self.col + 3]) is Rook:
                    if not self.game.board[self.row][self.col + 3].has_moved:
                        if (self.game.board[self.row][self.col + 2] is None and
                                self.game.board[self.row][self.col + 1] is None):
                            self.has_moved = True
                            return True
            if col - self.col == -2:
                if type(self.game.board[self.row][self.col - 4]) is Rook:
                    if not self.game.board[self.row][self.col - 4].has_moved:
                        if (self.game.board[self.row][self.col - 3] is None and
                                self.game.board[self.row][self.col - 2] is None and
                                self.game.board[self.row][self.col - 1] is None):
                            self.has_moved = True
                            return True
        else:
            return False


class Knight(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-knight.png').convert_alpha()

    def can_move(self, row, col):
        if (abs(self.col - col) == 2 and abs(self.row - row) == 1 or  # check for knight movement
                abs(self.row - row) == 2 and abs(self.col - col) == 1):
            return True
        else:
            return False
