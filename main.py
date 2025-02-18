# main.py
import sys
import pygame
from game import Game

def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Spaceship Game')
    clock = pygame.time.Clock()
    game = Game()
    font = pygame.font.Font(None, 36)

    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
