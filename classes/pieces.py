import pygame

import constants


class Piece:
    def __init__(self, scene, row, col, color):
        self.scene = scene
        self.row = row
        self.col = col
        self.color = color
        self.surface = pygame.Surface((0, 0))
        self.rect = self.surface.get_rect().move(self.scene.tile_to_coords(row, col))

    def draw(self):
        self.scene.app.screen.blit(self.surface, self.rect)

    def move(self, row, col):
        if self.scene.board[row][col]:
            self.scene.inactive_player.pieces.remove(self.scene.board[row][col])
        self.scene.board[row][col] = self
        self.scene.board[self.row][self.col] = None
        self.row = row
        self.col = col
        self.rect.topleft = (self.scene.tile_to_coords(row, col))

    def basic_movement_check(self, row, col):
        if (not (self.row == row and self.col == col) and
                (0 <= row < constants.BOARD_SIZE and 0 <= col < constants.BOARD_SIZE)):
            return True


class Pawn(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.transform.scale(
            pygame.image.load('assets/pieces-basic-png/' + self.color + '-pawn.png').convert_alpha(),
            (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(self.scene.tile_to_coords(row, col))
        self.direction = -1 if color == 'white' else 1

    def can_see(self, row, col):
        if not self.basic_movement_check(row, col):
            return False
        if self.row + self.direction == row and abs(self.col - col) == 1:  # take opponent's piece
            if self.scene.board[row][col]:
                if self.scene.board[row][col].color != self.color:
                    return True
            if self.scene.last_moves:
                if (self.scene.last_moves[-1].piece == self.scene.board[row - self.direction][col] and  # en' passant
                        self.scene.last_moves[-1].row == (constants.BOARD_SIZE - 1 - self.direction) % (
                                constants.BOARD_SIZE - 1)):
                    return True
        if (self.row + self.direction == row and self.col == col and  # move forward once
                self.scene.board[row][col] is None):
            return True
        if (self.row == (constants.BOARD_SIZE - 1 + self.direction) % (constants.BOARD_SIZE - 1) and  # move frwrd twice
                self.row + self.direction * 2 == row and self.col == col and
                self.scene.board[self.row + self.direction][col] is None and
                self.scene.board[self.row + self.direction * 2][col] is None):
            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.transform.scale(
            pygame.image.load('assets/pieces-basic-png/' + self.color + '-bishop.png').convert_alpha(),
            (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(self.scene.tile_to_coords(row, col))

    def can_see(self, row, col):
        if not self.basic_movement_check(row, col):
            return False
        if self.row + self.col == row + col or self.row - self.col == row - col:  # check for diagonal movement
            for _row, _col in zip(  # check for pieces obstructing the path
                    range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1),
                    range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1)):
                if self.scene.board[_row][_col]:
                    return False
            return True
        else:
            return False


class Rook(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.transform.scale(
            pygame.image.load('assets/pieces-basic-png/' + self.color + '-rook.png').convert_alpha(),
            (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(self.scene.tile_to_coords(row, col))
        self.has_moved = False

    def can_see(self, row, col):
        if not self.basic_movement_check(row, col):
            return False
        if self.col == col:  # check for vertical movement
            for _row in range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1):
                if self.scene.board[_row][col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.row == row:  # check for horizontal movement
            for _col in range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1):
                if self.scene.board[row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.transform.scale(
            pygame.image.load('assets/pieces-basic-png/' + self.color + '-queen.png').convert_alpha(),
            (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(self.scene.tile_to_coords(row, col))

    def can_see(self, row, col):
        if not self.basic_movement_check(row, col):
            return False
        if self.row + self.col == row + col or self.row - self.col == row - col:  # check for diagonal movement
            for _row, _col in zip(
                    range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1),
                    range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1)):
                if self.scene.board[_row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.col == col:  # check for vertical movement
            for _row in range(self.row + 1 if row > self.row else self.row - 1, row, 1 if row > self.row else -1):
                if self.scene.board[_row][col]:  # check for pieces obstructing the path
                    return False
            return True
        if self.row == row:  # check for horizontal movement
            for _col in range(self.col + 1 if col > self.col else self.col - 1, col, 1 if col > self.col else -1):
                if self.scene.board[row][_col]:  # check for pieces obstructing the path
                    return False
            return True
        else:
            return False


class King(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.transform.scale(
            pygame.image.load('assets/pieces-basic-png/' + self.color + '-king.png').convert_alpha(),
            (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(self.scene.tile_to_coords(row, col))
        self.has_moved = False

    def can_see(self, row, col):
        if not self.basic_movement_check(row, col):
            return False
        if abs(self.col - col) <= 1 and abs(self.row - row) <= 1:  # check for king movement
            for piece in self.scene.inactive_player.pieces:
                if piece.can_see(row, col):
                    return False
            return True

        if not self.has_moved and not self.scene.active_player.in_check:  # check for castle
            if col - self.col == 2 and self.row == row:
                if type(self.scene.board[self.row][self.col + 3]) is Rook:
                    if not self.scene.board[self.row][self.col + 3].has_moved:
                        if (self.scene.board[self.row][self.col + 2] is None and
                                self.scene.board[self.row][self.col + 1] is None):
                            return True
            if col - self.col == -2 and self.row == row:
                if type(self.scene.board[self.row][self.col - 4]) is Rook:
                    if not self.scene.board[self.row][self.col - 4].has_moved:
                        if (self.scene.board[self.row][self.col - 3] is None and
                                self.scene.board[self.row][self.col - 2] is None and
                                self.scene.board[self.row][self.col - 1] is None):
                            return True

        else:
            return False


class Knight(Piece):
    def __init__(self, game, row, col, color):
        super().__init__(game, row, col, color)
        self.surface = pygame.transform.scale(
            pygame.image.load('assets/pieces-basic-png/' + self.color + '-knight.png').convert_alpha(),
            (constants.TILE_SIZE, constants.TILE_SIZE))
        self.rect = self.surface.get_rect().move(self.scene.tile_to_coords(row, col))

    def can_see(self, row, col):
        if not self.basic_movement_check(row, col):
            return False
        if (abs(self.col - col) == 2 and abs(self.row - row) == 1 or  # check for knight movement
                abs(self.row - row) == 2 and abs(self.col - col) == 1):
            return True
        else:
            return False
