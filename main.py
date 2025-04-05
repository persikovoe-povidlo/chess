import pygame

from scenes.game_scene import GameScene
import constants
from scenes.main_menu_scene import MainMenuScene


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = MainMenuScene(self)

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

    def change_scene(self, scene, **kwargs):
        match scene:
            case 'game':
                self.scene = GameScene(self)
            case 'main_menu':
                self.scene = MainMenuScene(self)

    '''def force_redraw(self):
        self.scene.draw()
        pygame.display.flip()'''


def main():
    application = Application()
    application.start()


if __name__ == '__main__':
    main()
