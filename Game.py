# game.py
import pygame
from screeninfo import get_monitors
from asteroid import Asteroid
from spaceship import Spaceship
from bullet import Bullet
from pathlib import Path

display = get_monitors()
BASE_DIR = Path(__file__).parent
screen_width = display[0].width
screen_height = display[0].height
screen = pygame.display.set_mode((screen_width, screen_height))

class Game:
    def __init__(self):
        self.run = True
        self.image = pygame.image.load(BASE_DIR / "Assets/background/background.png")
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.spaceship = Spaceship(screen)  # Pass the screen here
        self.all_sprites.add(self.spaceship)
        for _ in range(5):
            asteroid = Asteroid(screen, self)
            self.asteroid_group.add(asteroid)
            self.all_sprites.add(asteroid)

    def check_collisions(self):
        for bullet in self.bullet_group:
            for asteroid in self.asteroid_group:
                if bullet.rect.colliderect(asteroid.rect):
                    asteroid.hit()
                    bullet.kill()

    def new_asteroid(self, size, x, y):
        asteroid = Asteroid(screen, self, size, True, x, y)
        self.asteroid_group.add(asteroid)
        self.all_sprites.add(asteroid)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.spaceship.handle_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.spaceship)
                    self.bullet_group.add(bullet)
                    self.all_sprites.add(bullet)

    def update(self):
        self.all_sprites.update()
        for asteroid in self.asteroid_group:
            asteroid.move()
        self.check_collisions()

    def draw(self):
        screen.blit(self.image, (0, 0))
        self.all_sprites.draw(screen)
        pygame.display.update()
