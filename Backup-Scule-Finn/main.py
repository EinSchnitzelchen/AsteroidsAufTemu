# main.py
import sys
import pygame
from game import Game
from menu import Menu

def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Spaceship Game')
    clock = pygame.time.Clock()
    game = Game()
    menu = Menu()

    while menu.run:
        menu.draw()
        
    if menu.start_game:
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
