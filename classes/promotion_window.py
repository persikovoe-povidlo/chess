import pygame

from classes.pieces import Queen, Rook, Bishop, Knight
from functions import tile_to_coords
import constants


class PromotionWindow:
    class Promotion:
        def __init__(self, piece, color):
            self.piece = piece
            self.color = color
            self.image = pygame.transform.scale(
                pygame.image.load('assets/pieces-basic-png/' + color + '-' + piece + '.png').convert_alpha(),
                (constants.TILE_SIZE, constants.TILE_SIZE))
            self.rect = self.image.get_rect()

    def __init__(self, game):
        self.game = game
        self.promotion = False
        self.active_promotions = None
        self.row = 0
        self.col = 0

        self.white_promotions = [self.Promotion('queen', 'white'), self.Promotion('knight', 'white'),
                                 self.Promotion('bishop', 'white'), self.Promotion('rook', 'white')]
        self.black_promotions = [self.Promotion('queen', 'black'), self.Promotion('knight', 'black'),
                                 self.Promotion('bishop', 'black'), self.Promotion('rook', 'black')]

    def draw(self):
        if self.promotion:
            for promotion in self.active_promotions:
                self.game.display.blit(promotion.image, promotion.rect)

    def logic(self, event):
        if self.promotion:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for promotion in self.active_promotions:
                        if promotion.rect.collidepoint(event.pos):
                            match promotion.piece:
                                case 'queen':
                                    self.game.new_piece(Queen(self.game, self.row, self.col, promotion.color))
                                case 'knight':
                                    self.game.new_piece(Knight(self.game, self.row, self.col, promotion.color))
                                case 'bishop':
                                    self.game.new_piece(Bishop(self.game, self.row, self.col, promotion.color))
                                case 'rook':
                                    self.game.new_piece(Rook(self.game, self.row, self.col, promotion.color))
                            self.promotion = False
                            self.game.change_turn()
        '''if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragged_piece:
                    self.release_piece(self.dragged_piece)
                    self.dragged_piece = None
                    self.available_moves.clear()
                    self.available_moves_surface.fill((0, 0, 0, 0))

        if event.type == pygame.MOUSEMOTION:
            if self.dragged_piece:
                self.dragged_piece.rect.center = pygame.mouse.get_pos()'''

    def place(self, row, col, direction):
        self.row = row
        self.col = col
        if self.game.active_player.king.color == 'white':
            self.active_promotions = self.white_promotions
        else:
            self.active_promotions = self.black_promotions
        shift = 0
        for promotion in self.active_promotions:
            promotion.rect.topleft = tile_to_coords(row + shift * direction*-1, col)
            shift += 1
