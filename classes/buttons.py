import pygame


class Button:
    def __init__(self, board, x, y, w, h, color):
        self.color = color
        self.board = board
        self.surface = pygame.Surface((w, h))
        self.surface.fill(color)
        self.rect = pygame.Rect((x, y), (w, h))
        self.pressed = False

    def draw(self, display):
        display.blit(self.surface, self.rect)

    def press(self):
        self.pressed = True
        self.surface.fill('gray1')
        self.action()

    def release(self):
        self.pressed = False
        self.surface.fill('gray')

    def action(self):
        pass


class UndoButton(Button):
    def __init__(self, board, x, y, w, h, color):
        super().__init__(board, x, y, w, h, color)

    def action(self):
        self.board.undo()
