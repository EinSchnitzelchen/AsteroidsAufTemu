import pygame
from screeninfo import get_monitors
from pathlib import Path

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

        self.image = pygame.image.load(BASE_DIR / "Assets/background/background.png")
        self.logo = pygame.image.load(BASE_DIR / "Assets/logo.png")
        self.logo = pygame.transform.scale(self.logo, (screen_width/3 * 1.5, screen_height/7 * 1.5))
        self.logo_rect = self.logo.get_rect()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))

        self.sound = pygame.mixer.Sound(BASE_DIR / "Assets/soundtrack.wav")
        self.channel = self.sound.play(loops = -1)
        self.logo_rect.center = (screen_width // 2, screen_height // 4)


    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                self.start_game = True
                self.run = False

    def draw(self):
        screen.blit(self.logo, self.logo_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        self.handle_events()

    

