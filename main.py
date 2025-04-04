import pygame

from scenes.game_scene import GameScene
import constants


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = GameScene(self)

    def start(self):
        while self.running:
            for event in pygame.event.get():
                self.scene.logic(event)

                if event.type == pygame.QUIT:
                    self.running = False

            self.scene.draw()
            pygame.display.flip()

            self.clock.tick(60)
        else:
            pygame.quit()

    def switch_scene(self, scene):
        self.scene = scene(self)


def main():
    application = Application()
    application.start()


if __name__ == '__main__':
    main()
