import json

import pygame
import socket
from threading import Thread
from random import randint


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption('test')
        self.clock = pygame.time.Clock()
        self.running = True
        self.socket = socket.socket()
        self.socket.connect(('127.0.0.1', 25565))
        Thread(target=self.listen).start()

    def listen(self):
        while True:
            data = self.socket.recv(1024).decode()
            if data:
                self.new_rect()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.socket.send('move'.encode())
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()

            self.clock.tick(60)
        else:
            self.socket.close()
            pygame.quit()

    def new_rect(self):
        x = randint(100, 1820)
        y = randint(100, 980)
        h = randint(10, 40)
        w = randint(10, 40)
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        pygame.draw.rect(self.screen, color, (x, y, h, w))


def main():
    s = 'm1234aa'
    print(s[1:5])
    row1, col1, row2, col2 = map(int, s[1:5])
    print(row1, col1, row2, col2)
    # application = Application()
    # application.start()


if __name__ == '__main__':
    main()
