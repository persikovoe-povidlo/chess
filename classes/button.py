import pygame


class Button:
    def __init__(self, scene, x, y, w, h, color, color_pressed, image=None, action=lambda: None):
        self.scene = scene
        self.rect = pygame.Rect((x, y), (w, h))
        self.color = color
        self.color_pressed = color_pressed
        self.pressed = False
        self.surface = pygame.Surface((w, h))
        self.surface.fill(color)
        self.image = image
        self.action = action
        if self.image:
            self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (w, h))
            self.surface.blit(self.image, (0, 0))

    def draw(self):
        self.scene.app.screen.blit(self.surface, self.rect)

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

    def move(self, x, y):
        self.rect.topleft = (x, y)
