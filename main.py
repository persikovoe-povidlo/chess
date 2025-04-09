import pygame
import socket
from threading import Thread

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
        self.socket = socket.socket()
        self.socket.connect(('127.0.0.1', 25565))
        Thread(target=self.listen).start()

    def listen(self):
        while self.running:
            try:
                data = self.socket.recv(10).decode()
                if data == 'disconnect':
                    self.running = False
                self.scene.listen(data)
            except:
                self.running = False
                print('connection to server lost')

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
            self.socket.send('disconnect'.encode())
            self.socket.close()
            pygame.quit()

    def change_scene(self, scene, **kwargs):
        if scene == 'game':
            self.scene = GameScene(self, kwargs['color'])
        elif scene == 'main_menu':
            self.scene = MainMenuScene(self)


def main():
    application = Application()
    application.start()


if __name__ == '__main__':
    main()
