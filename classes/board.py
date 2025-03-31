import pygame

from functions import tile_to_coords
import constants


class Board:
    def __init__(self, display):
        self.display = display
        self.tiles = [[None for _ in range(constants.BOARD_SIZE)] for _ in range(constants.BOARD_SIZE)]
        self.dragged_piece = None
        self.last_move = None
        self.turn = 'white'

    def draw(self):
        for col in range(constants.BOARD_SIZE):
            for row in range(constants.BOARD_SIZE):
                pygame.draw.rect(self.display, 'burlywood1' if (row % 2 == 0 and col % 2 == 0) or (
                        row % 2 != 0 and col % 2 != 0) else 'chocolate4',
                                 (tile_to_coords(row, col), (constants.TILE_SIZE, constants.TILE_SIZE)))

    def place_piece(self, piece):
        self.tiles[piece.row][piece.col] = piece

    def draw_pieces(self):
        for row in self.tiles:
            for piece in row:
                if piece:
                    piece.draw(self.display)
        if self.dragged_piece:
            self.dragged_piece.draw(self.display)

    def undo(self):
        if self.last_move:
            self.tiles[self.last_move.row1][self.last_move.col1] = self.tiles[self.last_move.row2][self.last_move.col2]
            self.tiles[self.last_move.row1][self.last_move.col1].row = self.last_move.row1
            self.tiles[self.last_move.row1][self.last_move.col1].col = self.last_move.col1
            self.tiles[self.last_move.row1][self.last_move.col1].rect.topleft = (
                tile_to_coords(self.last_move.row1, self.last_move.col1))
            self.tiles[self.last_move.row2][self.last_move.col2] = self.last_move.piece
            if self.turn == 'white':
                self.turn = 'black'
            else:
                self.turn = 'white'
            self.last_move = None
