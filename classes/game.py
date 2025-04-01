import pygame

from classes.buttons import UndoButton
from classes.move import Move
from classes.pieces import Pawn, Bishop, Rook, Queen, Knight, King
from classes.player import Player
from functions import tile_to_coords, coords_to_tile
import constants


class Game:
    def __init__(self, display):
        self.display = display
        self.possible_moves_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)

        self.board = [[None for _ in range(constants.BOARD_SIZE)] for _ in range(constants.BOARD_SIZE)]
        self.dragged_piece = None
        self.last_moves = []
        self.buttons = []
        self.possible_moves = []

        self.active_player = Player(King(self, 7, 4, 'white'))
        self.inactive_player = Player(King(self, 0, 4, 'black'))

        self.place_default_pieces()
        self.place_buttons()

    def logic(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for row in self.board:
                    for tile in row:
                        if tile:
                            if tile.rect.collidepoint(event.pos) and tile.color == self.active_player.king.color:
                                self.dragged_piece = tile
                                for row in range(constants.BOARD_SIZE):
                                    for col in range(constants.BOARD_SIZE):
                                        if self.dragged_piece.can_move(row, col):
                                            self.possible_moves.append((row, col))
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos) and not button.pressed:
                        button.press()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragged_piece:
                    col, row = coords_to_tile(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if (row, col) in self.possible_moves:

                        if (type(self.dragged_piece) is Pawn and  # check for en' passant
                                abs(self.dragged_piece.col - col) == 1 and self.board[row][col] is None):
                            self.last_moves.append(Move(self.dragged_piece.row, self.dragged_piece.col, row, col,
                                                        self.board[row - self.dragged_piece.direction][col],
                                                        self.dragged_piece))
                            self.board[row - self.dragged_piece.direction][col] = None

                        elif type(self.dragged_piece) is King and self.dragged_piece.col - col == 2:  # check for castle
                            self.last_moves.append(Move(self.dragged_piece.row, self.dragged_piece.col, row, col,
                                                        self.board[row][self.dragged_piece.col - 4],
                                                        self.dragged_piece))
                            self.board[self.dragged_piece.row][self.dragged_piece.col - 4].move(row, col + 1)

                        elif type(self.dragged_piece) is King and self.dragged_piece.col - col == -2:  # chck for castle
                            self.last_moves.append(Move(self.dragged_piece.row, self.dragged_piece.col, row, col,
                                                        self.board[row][self.dragged_piece.col + 3],
                                                        self.dragged_piece))
                            self.board[self.dragged_piece.row][self.dragged_piece.col + 3].move(row, col - 1)

                        else:  # default move
                            if type(self.dragged_piece) is King or type(self.dragged_piece) is Rook:
                                self.last_moves.append(Move(self.dragged_piece.row, self.dragged_piece.col, row, col,
                                                            self.board[row][col], self.dragged_piece,
                                                            self.dragged_piece.has_moved))
                                self.dragged_piece.has_moved = True
                            else:
                                self.last_moves.append(Move(self.dragged_piece.row, self.dragged_piece.col, row, col,
                                                            self.board[row][col], self.dragged_piece))
                        self.dragged_piece.move(row, col)
                        for piece in self.active_player.pieces:
                            if piece.can_move(self.inactive_player.king.row, self.inactive_player.king.col):
                                self.inactive_player.in_check = True
                        self.change_turn()
                    else:  # place piece back
                        self.dragged_piece.rect.topleft = (
                            tile_to_coords(self.dragged_piece.row, self.dragged_piece.col))
                    self.dragged_piece = None
                    self.possible_moves.clear()
                    self.possible_moves_surface.fill((0, 0, 0, 0))
                for button in self.buttons:
                    button.release()

        if event.type == pygame.MOUSEMOTION:
            if self.dragged_piece:
                self.dragged_piece.rect.center = pygame.mouse.get_pos()

    def draw(self):
        self.display.fill((50, 50, 50))
        self.draw_board()
        self.draw_possible_moves()
        self.draw_buttons()
        self.draw_pieces()

    def place_default_pieces(self):
        self.place_piece(self.active_player.king)
        self.place_piece(self.inactive_player.king)

        for i in range(8):
            self.place_piece(Pawn(self, 1, i, 'black'))
            self.place_piece(Pawn(self, 6, i, 'white'))

        self.place_piece(Bishop(self, 7, 2, 'white'))
        self.place_piece(Bishop(self, 7, 5, 'white'))
        self.place_piece(Rook(self, 7, 0, 'white'))
        self.place_piece(Rook(self, 7, 7, 'white'))
        self.place_piece(Queen(self, 7, 3, 'white'))
        self.place_piece(Knight(self, 7, 1, 'white'))
        self.place_piece(Knight(self, 7, 6, 'white'))

        self.place_piece(Bishop(self, 0, 2, 'black'))
        self.place_piece(Bishop(self, 0, 5, 'black'))
        self.place_piece(Rook(self, 0, 0, 'black'))
        self.place_piece(Rook(self, 0, 7, 'black'))
        self.place_piece(Queen(self, 0, 3, 'black'))
        self.place_piece(Knight(self, 0, 1, 'black'))
        self.place_piece(Knight(self, 0, 6, 'black'))

    def place_buttons(self):
        self.buttons.append(UndoButton(self, constants.BOARD_POS_X - constants.TILE_SIZE,
                                       constants.BOARD_POS_Y + constants.TILE_SIZE * 4, constants.TILE_SIZE,
                                       constants.TILE_SIZE // 2, 'gray10', 'gray6'))

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.display)

    def change_turn(self):
        self.active_player, self.inactive_player = self.inactive_player, self.active_player

    def draw_board(self):
        for col in range(constants.BOARD_SIZE):
            for row in range(constants.BOARD_SIZE):
                pygame.draw.rect(self.display, 'burlywood1' if (row % 2 == 0 and col % 2 == 0) or (
                        row % 2 != 0 and col % 2 != 0) else 'chocolate4',
                                 (tile_to_coords(row, col), (constants.TILE_SIZE, constants.TILE_SIZE)))

    def draw_possible_moves(self):
        for tile in self.possible_moves:
            row, col = tile[0], tile[1]
            x, y = tile_to_coords(row, col)
            if self.board[row][col] is None:
                pygame.draw.circle(self.possible_moves_surface, (0, 0, 255, 100),
                                   (x + constants.TILE_SIZE // 2, y + constants.TILE_SIZE // 2),
                                   constants.TILE_SIZE // 8)
            else:
                pygame.draw.rect(self.possible_moves_surface, (0, 0, 255, 100),
                                 (tile_to_coords(row, col), (constants.TILE_SIZE, constants.TILE_SIZE)))
        if self.dragged_piece:
            pygame.draw.rect(self.possible_moves_surface, (0, 0, 255, 100), (tile_to_coords(
                self.dragged_piece.row, self.dragged_piece.col), (constants.TILE_SIZE, constants.TILE_SIZE)))
        self.display.blit(self.possible_moves_surface, (0, 0))

    def place_piece(self, piece):
        self.board[piece.row][piece.col] = piece
        if piece.color == self.active_player.king.color:
            self.active_player.pieces.append(piece)
        else:
            self.inactive_player.pieces.append(piece)

    def draw_pieces(self):
        for row in self.board:
            for piece in row:
                if piece:
                    piece.draw(self.display)
        if self.dragged_piece:
            self.dragged_piece.draw(self.display)

    def undo(self):
        if self.last_moves:
            if self.last_moves[-1].has_moved is not None:
                self.last_moves[-1].piece.has_moved = self.last_moves[-1].has_moved
            # check for en' passant
            if self.last_moves[-1].piece.row != self.last_moves[-1].row2:
                self.place_piece(self.last_moves[-1].captured_piece)
                self.board[self.last_moves[-1].row2 - self.last_moves[-1].piece.direction][
                    self.last_moves[-1].col2] = None

            # check for castle
            if type(self.last_moves[-1].piece) is King and self.last_moves[-1].col1 - self.last_moves[-1].col2 == 2:
                self.last_moves[-1].captured_piece.move(self.last_moves[-1].row2, self.last_moves[-1].col2 - 2)

            if type(self.last_moves[-1].piece) is King and self.last_moves[-1].col1 - self.last_moves[-1].col2 == -2:
                self.last_moves[-1].captured_piece.move(self.last_moves[-1].row2, self.last_moves[-1].col2 + 1)

            # revert move
            self.board[self.last_moves[-1].row2][self.last_moves[-1].col2].move(self.last_moves[-1].row1,
                                                                                self.last_moves[-1].col1)
            if self.last_moves[-1].captured_piece:
                self.place_piece(self.last_moves[-1].captured_piece)
            self.change_turn()
            self.last_moves.pop()
