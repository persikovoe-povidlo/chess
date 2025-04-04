import pygame


class Button:
    def __init__(self, game, x, y, w, h, color, color_pressed):
        self.game = game
        self.rect = pygame.Rect((x, y), (w, h))
        self.color = color
        self.color_pressed = color_pressed
        self.image = None
        self.pressed = False
        self.surface = pygame.Surface((w, h))
        self.surface.fill(color)

    def draw(self):
        self.game.app.screen.blit(self.surface, self.rect)

    def press(self):
        self.pressed = True
        self.surface.fill(self.color_pressed)
        if self.image:
            self.surface.blit(self.image, (0, 0))

    def release(self):
        self.pressed = False
        self.surface.fill(self.color)
        if self.image:
            self.surface.blit(self.image, (0, 0))

    def action(self):
        pass

    def logic(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos) and not self.pressed:
                    self.press()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.rect.collidepoint(event.pos) and self.pressed:
                    self.action()
                self.release()

        if event.type == pygame.MOUSEMOTION:
            pass


class UndoButton(Button):
    def __init__(self, board, x, y, w, h, color, color_pressed):
        super().__init__(board, x, y, w, h, color, color_pressed)
        self.image = pygame.transform.scale(pygame.image.load('assets/undo.png').convert_alpha(), (w, h))
        self.surface.blit(self.image, (0, 0))

    def action(self):
        self.game.undo()
