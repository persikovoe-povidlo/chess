import pygame

from classes.pieces import Queen, Rook, Bishop, Knight
from functions import tile_to_coords
import constants


class PromotionWindow:
    class Promotion:
        def __init__(self, class_name, piece_name, color):
            self.class_name = class_name
            self.piece = piece_name
            self.color = color
            self.image = pygame.transform.scale(
                pygame.image.load('assets/pieces-basic-png/' + color + '-' + piece_name + '.png').convert_alpha(),
                (constants.TILE_SIZE, constants.TILE_SIZE))
            self.rect = self.image.get_rect()

    def __init__(self, game):
        self.game = game
        self.promotion = False
        self.active_promotions = None
        self.row = 0
        self.col = 0
        self.highlighted_piece_rect = None
        self.surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)

        self.white_promotions = [self.Promotion(Queen, 'queen', 'white'), self.Promotion(Knight, 'knight', 'white'),
                                 self.Promotion(Bishop, 'bishop', 'white'), self.Promotion(Rook, 'rook', 'white')]
        self.black_promotions = [self.Promotion(Queen, 'queen', 'black'), self.Promotion(Knight, 'knight', 'black'),
                                 self.Promotion(Bishop, 'bishop', 'black'), self.Promotion(Rook, 'rook', 'black')]

    def draw(self):
        pygame.draw.rect(self.surface, (0, 0, 0, 150),
                         (constants.BOARD_POS_X, constants.BOARD_POS_Y, constants.BOARD_WIDTH, constants.BOARD_WIDTH))
        if self.promotion:
            for promotion in self.active_promotions:
                pygame.draw.circle(self.surface, (200, 200, 200, 255), promotion.rect.center, constants.TILE_SIZE // 2)
            if self.highlighted_piece_rect:
                pygame.draw.circle(self.surface, (255, 102, 0, 255), self.highlighted_piece_rect.center,
                                   constants.TILE_SIZE // 2)
            for promotion in self.active_promotions:
                self.surface.blit(promotion.image, promotion.rect)
            self.game.display.blit(self.surface, (0, 0))

    def logic(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for piece in self.active_promotions:
                    if piece.rect.collidepoint(event.pos):
                        self.game.new_piece(piece.class_name(self.game, self.row, self.col, piece.color))
                        self.promotion = False

        if event.type == pygame.MOUSEMOTION:
            self.highlighted_piece_rect = None
            for piece in self.active_promotions:
                if piece.rect.collidepoint(event.pos):
                    self.highlighted_piece_rect = piece.rect

    def place(self, row, col, direction):
        self.row = row
        self.col = col
        self.highlighted_piece_rect = pygame.Rect(tile_to_coords(self.row, self.col), (constants.TILE_SIZE,
                                                                                       constants.TILE_SIZE))
        if self.game.active_player.king.color == 'white':
            self.active_promotions = self.white_promotions
        else:
            self.active_promotions = self.black_promotions
        shift = 0
        for promotion in self.active_promotions:
            promotion.rect.topleft = tile_to_coords(row + shift * direction * -1, col)
            shift += 1
