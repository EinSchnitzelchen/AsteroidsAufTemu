# bullet.py
import pygame
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(BASE_DIR / "Sprites/bullet/bullet.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.centerx = spaceship.rect.centerx
        self.rect.centery = spaceship.rect.centery
        self.direction = pygame.Vector2(0, -1).rotate(-spaceship.angle)
        self.pos = pygame.Vector2(self.rect.center)

    def update(self):
        self.pos += self.direction * 75
        self.rect.center = round(self.pos.x), round(self.pos.y)
