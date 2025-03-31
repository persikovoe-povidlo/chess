import pygame

import constants
from functions import tile_to_coords


class Piece:
    def __init__(self, board, row, col, color):
        self.board = board
        self.row = row
        self.col = col
        self.color = color
        self.surface = pygame.transform.scale(pygame.Surface((0, 0)), (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(tile_to_coords(row, col))

    def draw(self, display):
        display.blit(self.surface, self.rect)


class Pawn(Piece):
    def __init__(self, board, row, col, color):
        super().__init__(board, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-pawn.png').convert_alpha()
        self.direction = -1 if color == 'white' else 1

    def can_move(self, row, col):
        if (self.row + self.direction == row and abs(self.col - col) == 1 and  # take opponent's piece
                self.board.tiles[row][col]):
            if self.board.tiles[row][col].color != self.color:
                return True
        if (self.row + self.direction == row and self.col == col and  # move forward once
                self.board.tiles[row][col] is None):
            return True
        if (self.row == (constants.BOARD_SIZE - 1 + self.direction) % (constants.BOARD_SIZE - 1) and  # move frwrd twice
                self.row + self.direction * 2 == row and self.col == col and
                self.board.tiles[self.row + self.direction][col] is None and
                self.board.tiles[self.row + self.direction * 2][col] is None):
            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, board, row, col, color):
        super().__init__(board, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-bishop.png').convert_alpha()

    def can_move(self, row, col):
        if self.row + self.col == row + col or self.row - self.col == row - col:  # check for diagonal movement
            for _row, _col in zip(  # check for pieces obstructing the path
                    range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1),
                    range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1)):
                if self.board.tiles[_row][_col]:
                    return False
            return True
        else:
            return False


class Rook(Piece):
    def __init__(self, board, row, col, color):
        super().__init__(board, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-rook.png').convert_alpha()

    def can_move(self, row, col):
        if self.col == col:  # check for vertical movement
            for _row in range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1):
                if self.board.tiles[_row][col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.row == row:  # check for horizontal movement
            for _col in range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1):
                if self.board.tiles[row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, board, row, col, color):
        super().__init__(board, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-queen.png').convert_alpha()

    def can_move(self, row, col):
        if self.row + self.col == row + col or self.row - self.col == row - col:  # check for diagonal movement
            for _row, _col in zip(
                    range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1),
                    range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1)):
                if self.board.tiles[_row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.col == col:  # check for vertical movement
            for _row in range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1):
                if self.board.tiles[_row][col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.row == row:  # check for horizontal movement
            for _col in range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1):
                if self.board.tiles[row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        else:
            return False


class King(Piece):
    def __init__(self, board, row, col, color):
        super().__init__(board, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-king.png').convert_alpha()

    def can_move(self, row, col):
        if abs(self.col - col) <= 1 and abs(self.row - row) <= 1:
            return True
        else:
            return False


class Knight(Piece):
    def __init__(self, board, row, col, color):
        super().__init__(board, row, col, color)
        self.surface = pygame.image.load('assets/pieces-basic-png/' + self.color + '-knight.png').convert_alpha()

    def can_move(self, row, col):
        if (abs(self.col - col) == 2 and abs(self.row - row) == 1 or
                abs(self.row - row) == 2 and abs(self.col - col) == 1):
            return True
        else:
            return False
