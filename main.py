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
    menu = Menu()
    two_player = False

    while menu.run:
        menu.draw()
        two_player = menu.two_player

    game = Game(two_player)

        
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
