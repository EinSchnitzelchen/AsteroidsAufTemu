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

class Menu:
    def __init__(self):
        
        self.run = True
        self.start_game = False
        self.logo_pos_x = screen.get_width() / 2
        self.logo_pos_y = 100

        self.two_player = False

        self.image = pygame.image.load(BASE_DIR / "Assets/background/background.png")
        self.logo = pygame.image.load(BASE_DIR / "Assets/logo.png")
        self.logo = pygame.transform.scale(self.logo, (screen_width/3 * 1.5, screen_height/7 * 1.5))
        self.logo_rect = self.logo.get_rect()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))

        self.logo_rect.center = (screen_width // 2, screen_height // 4)

        self.current_frame = 0

    def logo_float(self):
        self.logo_rect.centery = math.sin(self.current_frame) * 30 + screen_height/7 * 1.5


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                elif event.key == pygame.K_RSHIFT:
                    self.two_player = True
                    self.start_game = True
                    self.run = False
                elif event.key == pygame.K_SPACE:
                    self.two_player = False
                    self.start_game = True
                    self.run = False

    def show_Text(self):
        self.font = pygame.font.Font(BASE_DIR / 'Assets/PixelifySans-Regular.ttf', round(screen_width / 32) + round(math.sin(self.current_frame)*2))
        Text = self.font.render("PRESS SPACE FOR SINGLEPLAYER",True, (0, 255, 0))
        Text_2 = self.font.render("PRESS RIGHT SHIFT FOR MULTIPLAYER", True, (0,255,0))
        text_rect = Text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 100))
        text_2_rect = Text_2.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 200))
        screen.blit(Text, text_rect)
        screen.blit(Text_2, text_2_rect)


    def draw(self):
        screen.blit(self.image, (0, 0))
        screen.blit(self.logo, self.logo_rect)
        self.show_Text()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        self.handle_events()
        self.current_frame = self.current_frame + 0.1
        self.logo_float()
        
        
        

    

