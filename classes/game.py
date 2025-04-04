import pygame

from classes.buttons import UndoButton
from classes.move import Move
from classes.pieces import Pawn, Bishop, Rook, Queen, Knight, King
from classes.player import Player
from classes.promotion_window import PromotionWindow
from functions import tile_to_coords, coords_to_tile
import constants


class Game:
    def __init__(self, display):
        self.game_over = False
        self.display = display
        self.highlighted_tiles_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
                                                        pygame.SRCALPHA)
        self.board = [[None for _ in range(constants.BOARD_SIZE)] for _ in range(constants.BOARD_SIZE)]
        self.promotion_window = PromotionWindow(self)
        self.dragged_piece = None
        self.selected_piece = None
        self.last_moves = []
        self.buttons = []
        self.available_moves = []

        self.active_player = Player(King(self, 7, 4, 'white'))
        self.inactive_player = Player(King(self, 0, 4, 'black'))

        self.place_default_pieces()
        self.place_buttons()

    def draw_promotion_window(self):
        self.promotion_window.draw()

    def get_available_moves_for_piece(self, piece):
        for row in range(constants.BOARD_SIZE):
            for col in range(constants.BOARD_SIZE):
                if (piece.can_see(row, col) and
                        (self.board[row][col].color != piece.color if self.board[row][col] else True)):

                    saved_row, saved_col = piece.row, piece.col
                    saved_piece = self.board[row][col]
                    piece.move(row, col)

                    defends_check = True
                    for opponents_piece in self.inactive_player.pieces:
                        if opponents_piece.can_see(self.active_player.king.row,
                                                   self.active_player.king.col):
                            defends_check = False

                    if defends_check:
                        self.available_moves.append((row, col))
                    if saved_piece:
                        self.inactive_player.pieces.append(saved_piece)
                    piece.move(saved_row, saved_col)
                    self.board[row][col] = saved_piece

    def release_piece(self, piece):
        col, row = coords_to_tile(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if (row, col) in self.available_moves:
            if (type(piece) is Pawn and  # check for en' passant
                    abs(piece.col - col) == 1 and self.board[row][col] is None):

                self.last_moves.append(Move(piece.row, piece.col, self.board[row - piece.direction][col], piece,
                                            self.active_player.in_check))
                self.inactive_player.pieces.remove(self.board[row - piece.direction][col])
                self.board[row - piece.direction][col] = None

            elif type(piece) is King and abs(piece.col - col) == 2:  # check for castle
                if piece.col - col == 2:
                    self.last_moves.append(Move(piece.row, piece.col, self.board[row][piece.col - 4], piece,
                                                self.active_player.in_check))
                    self.board[piece.row][piece.col - 4].move(row, col + 1)

                if piece.col - col == -2:
                    self.last_moves.append(Move(piece.row, piece.col, self.board[row][piece.col + 3], piece,
                                                self.active_player.in_check))
                    self.board[piece.row][piece.col + 3].move(row, col - 1)

            else:  # ordinary move
                if type(piece) is King or type(piece) is Rook:
                    self.last_moves.append(
                        Move(piece.row, piece.col, self.board[row][col], piece, self.active_player.in_check,
                             piece.has_moved))
                    piece.has_moved = True
                else:
                    self.last_moves.append(
                        Move(piece.row, piece.col, self.board[row][col], piece, self.active_player.in_check))

            piece.move(row, col)
            self.available_moves.clear()

            if type(piece) is Pawn and row % (constants.BOARD_SIZE - 1) == 0:  # check for promotion
                self.promotion_window.promotion = True
                self.active_player.pieces.remove(piece)
                self.board[row][col] = None
                self.promotion_window.place(row, col, piece.direction)

            self.inactive_player.in_check = False
            for piece in self.active_player.pieces:
                if piece.can_see(self.inactive_player.king.row, self.inactive_player.king.col):
                    self.inactive_player.in_check = True

            self.change_turn()
            if not self.check_if_player_has_moves():
                self.game_over = True
        else:  # place piece back if move is not available
            piece.rect.topleft = (tile_to_coords(piece.row, piece.col))

    def selected_piece_logic(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for piece in self.active_player.pieces:
                    if piece.rect.collidepoint(event.pos):
                        self.available_moves.clear()
                        if piece != self.selected_piece:
                            self.selected_piece = None
                        self.dragged_piece = piece
                        self.get_available_moves_for_piece(self.dragged_piece)
                if self.selected_piece and self.dragged_piece is None:
                    self.release_piece(self.selected_piece)
                    self.selected_piece = None
                    self.available_moves.clear()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.selected_piece is None and self.dragged_piece:
                    self.selected_piece = self.dragged_piece
                elif self.dragged_piece:
                    if coords_to_tile(event.pos[0], event.pos[1]) == (self.dragged_piece.col, self.dragged_piece.row):
                        self.available_moves.clear()
                    self.selected_piece = None
                else:
                    self.selected_piece = None
                    self.available_moves.clear()
                if self.dragged_piece:
                    if coords_to_tile(event.pos[0], event.pos[1]) != (self.dragged_piece.col, self.dragged_piece.row):
                        self.selected_piece = None
                    self.release_piece(self.dragged_piece)
                    self.dragged_piece = None

        if event.type == pygame.MOUSEMOTION:
            if self.dragged_piece:
                self.dragged_piece.rect.center = pygame.mouse.get_pos()

    def logic(self, event):
        if not self.game_over:
            if not self.promotion_window.promotion:
                self.selected_piece_logic(event)
            else:
                self.promotion_window.logic(event)
            for button in self.buttons:
                button.logic(event)
        else:
            pass

    def draw(self):
        self.display.fill((50, 50, 50))
        self.draw_board()
        self.draw_highlighted_tiles()
        self.draw_buttons()
        self.draw_pieces()
        self.draw_promotion_window()

    def place_default_pieces(self):
        self.new_piece(self.active_player.king)
        self.new_piece(self.inactive_player.king)

        for i in range(8):
            self.new_piece(Pawn(self, 1, i, 'black'))
            self.new_piece(Pawn(self, 6, i, 'white'))

        self.new_piece(Bishop(self, 7, 2, 'white'))
        self.new_piece(Bishop(self, 7, 5, 'white'))
        self.new_piece(Rook(self, 7, 0, 'white'))
        self.new_piece(Rook(self, 7, 7, 'white'))
        self.new_piece(Queen(self, 7, 3, 'white'))
        self.new_piece(Knight(self, 7, 1, 'white'))
        self.new_piece(Knight(self, 7, 6, 'white'))

        self.new_piece(Bishop(self, 0, 2, 'black'))
        self.new_piece(Bishop(self, 0, 5, 'black'))
        self.new_piece(Rook(self, 0, 0, 'black'))
        self.new_piece(Rook(self, 0, 7, 'black'))
        self.new_piece(Queen(self, 0, 3, 'black'))
        self.new_piece(Knight(self, 0, 1, 'black'))
        self.new_piece(Knight(self, 0, 6, 'black'))

    def place_buttons(self):
        self.buttons.append(UndoButton(self, constants.BOARD_POS_X - constants.TILE_SIZE * 2,
                                       constants.SCREEN_HEIGHT // 2 - constants.TILE_SIZE // 2, constants.TILE_SIZE,
                                       constants.TILE_SIZE, 'gray30', 'gray27'))

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()

    def check_if_player_has_moves(self):
        for piece in self.active_player.pieces:
            self.get_available_moves_for_piece(piece)
            if self.available_moves:
                self.available_moves.clear()
                return True
        return False

    def change_turn(self):
        self.active_player, self.inactive_player = self.inactive_player, self.active_player

    def draw_board(self):
        for col in range(constants.BOARD_SIZE):
            for row in range(constants.BOARD_SIZE):
                pygame.draw.rect(self.display, 'burlywood1' if (row % 2 == 0 and col % 2 == 0) or (
                        row % 2 != 0 and col % 2 != 0) else 'chocolate4',
                                 (tile_to_coords(row, col), (constants.TILE_SIZE, constants.TILE_SIZE)))

    def draw_highlighted_tiles(self):
        self.highlighted_tiles_surface.fill((0, 0, 0, 0))
        if self.last_moves:
            last_move = self.last_moves[-1]
            pygame.draw.rect(self.highlighted_tiles_surface, (0, 255, 0, 70), (tile_to_coords(
                last_move.row, last_move.col), (constants.TILE_SIZE, constants.TILE_SIZE)))
            pygame.draw.rect(self.highlighted_tiles_surface, (0, 255, 0, 70), (tile_to_coords(
                last_move.piece.row, last_move.piece.col), (constants.TILE_SIZE, constants.TILE_SIZE)))

        for tile in self.available_moves:
            row, col = tile[0], tile[1]
            x, y = tile_to_coords(row, col)
            if self.board[row][col] is None:
                pygame.draw.circle(self.highlighted_tiles_surface, (0, 0, 255, 100),
                                   (x + constants.TILE_SIZE // 2, y + constants.TILE_SIZE // 2),
                                   constants.TILE_SIZE // 8)
            else:
                pygame.draw.rect(self.highlighted_tiles_surface, (0, 0, 255, 100),
                                 (tile_to_coords(row, col), (constants.TILE_SIZE, constants.TILE_SIZE)))

        if self.dragged_piece:
            pygame.draw.rect(self.highlighted_tiles_surface, (0, 0, 255, 100), (tile_to_coords(
                self.dragged_piece.row, self.dragged_piece.col), (constants.TILE_SIZE, constants.TILE_SIZE)))

        elif self.selected_piece:
            pygame.draw.rect(self.highlighted_tiles_surface, (0, 0, 255, 100), (tile_to_coords(
                self.selected_piece.row, self.selected_piece.col), (constants.TILE_SIZE, constants.TILE_SIZE)))

        if self.active_player.in_check:
            x, y = tile_to_coords(self.active_player.king.row, self.active_player.king.col)
            x, y = x + constants.TILE_SIZE // 2, y + constants.TILE_SIZE // 2
            pygame.draw.circle(self.highlighted_tiles_surface, (255, 0, 0, 200), (x, y), constants.TILE_SIZE // 2.2)
        self.display.blit(self.highlighted_tiles_surface, (0, 0))

    def new_piece(self, piece):
        self.board[piece.row][piece.col] = piece
        if piece.color == self.active_player.king.color:
            self.active_player.pieces.append(piece)
        else:
            self.inactive_player.pieces.append(piece)
        return piece

    def draw_pieces(self):
        for row in self.board:
            for piece in row:
                if piece:
                    piece.draw()
        if self.dragged_piece:
            self.dragged_piece.draw()

    def undo(self):
        if self.last_moves:
            last_move = self.last_moves[-1]

            if last_move.in_check:
                self.inactive_player.in_check = True
            else:
                self.inactive_player.in_check = False

            if self.promotion_window.promotion:
                self.promotion_window.promotion = False

            if last_move.has_moved is not None:
                last_move.piece.has_moved = last_move.has_moved

            # check for promotion
            if type(last_move.piece) is Pawn and last_move.piece.row % (constants.BOARD_SIZE - 1) == 0:
                self.inactive_player.pieces.pop()
                self.new_piece(last_move.piece)

            # check for castle
            if type(last_move.piece) is King and last_move.col - last_move.piece.col == 2:
                last_move.captured_piece.move(last_move.piece.row, last_move.piece.col - 2)
                self.inactive_player.pieces.remove(last_move.captured_piece)

            elif type(last_move.piece) is King and last_move.col - last_move.piece.col == -2:
                last_move.captured_piece.move(last_move.piece.row, last_move.piece.col + 1)
                self.inactive_player.pieces.remove(last_move.captured_piece)

            # revert move
            self.board[last_move.piece.row][last_move.piece.col].move(last_move.row, last_move.col)
            if last_move.captured_piece:
                self.new_piece(last_move.captured_piece)

            self.change_turn()
            self.last_moves.pop()
