import pygame

from classes.game import Game
import constants


def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    running = True
    game = Game(screen)

    while running:
        for event in pygame.event.get():
            game.logic(event)

            if event.type == pygame.QUIT:
                running = False

        game.draw()
        pygame.display.flip()

        clock.tick(60)


pygame.quit()

if __name__ == '__main__':
    main()
