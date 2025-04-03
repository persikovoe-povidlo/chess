import pygame


class Button:
    def __init__(self, game, x, y, w, h, color, color_pressed):
        self.game = game
        self.color = color
        self.color_pressed = color_pressed
        self.surface = pygame.Surface((w, h))
        self.surface.fill(color)
        self.rect = pygame.Rect((x, y), (w, h))
        self.pressed = False

    def draw(self):
        self.game.display.blit(self.surface, self.rect)

    def press(self):
        self.pressed = True
        self.surface.fill(self.color_pressed)
        self.action()

    def release(self):
        self.pressed = False
        self.surface.fill(self.color)

    def action(self):
        pass


class UndoButton(Button):
    def __init__(self, board, x, y, w, h, color, color_pressed):
        super().__init__(board, x, y, w, h, color, color_pressed)

    def action(self):
        self.game.undo()
