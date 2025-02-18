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

    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        game.show_score(0,0)
        clock.tick(60)

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
