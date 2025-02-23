import pygame
from screeninfo import get_monitors
from pathlib import Path
import math

pygame.init()

display = get_monitors()
BASE_DIR = Path(__file__).parent

screen_width = display[0].width
screen_height = display[0].height
screen = pygame.display.set_mode((screen_width, screen_height))

class Deathscreen:
    def __init__(self):
        
        self.run = True
        self.start_game = False
        self.two_player = False

        self.image = pygame.image.load(BASE_DIR / "Assets/background/deathscreen.webp")
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.current_frame = 0


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False

#    def show_Text(self):
#        self.font = pygame.font.Font(BASE_DIR / 'Assets/PixelifySans-Regular.ttf', round(screen_width / 32) + round(math.sin(self.current_frame)*2))
#        Text = self.font.render("PRESS SPACE FOR SINGLEPLAYER",True, (0, 255, 0))
#        Text_2 = self.font.render("PRESS RIGHT SHIFT FOR MULTIPLAYER", True, (0,255,0))
 #       text_rect = Text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 100))
#        text_2_rect = Text_2.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 200))
#        screen.blit(Text, text_rect)
#        screen.blit(Text_2, text_2_rect)


    def draw(self):
        screen.blit(self.image, (0, 0))
        #self.show_Text()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        self.handle_events()
        self.current_frame = self.current_frame + 0.1
        
        
        

    

