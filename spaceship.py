# spaceship.py
import pygame
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(BASE_DIR / "Assets/spaceship/spaceship.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.75)
        self.org_image = self.image.copy()
        self.rect = self.image.get_rect(center=(70, 600))
        self.angle = 0
        self.direction = pygame.Vector2(0, -1)
        self.pos = [self.screen.get_width() / 2, self.screen.get_height() / 2]
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 0.3
        self.max_speed = 10
        self.friction = 0.01

    def wrap_around(self):
        if self.pos.x < 0:
            self.pos.x = self.screen.get_width()
        elif self.pos.x > self.screen.get_width():
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = self.screen.get_height()
        elif self.pos.y > self.screen.get_height():
            self.pos.y = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.velocity += self.direction * self.acceleration
            if self.velocity.length() > self.max_speed:
                self.velocity = self.velocity.normalize() * self.max_speed
        elif keys[pygame.K_DOWN]:
            self.velocity -= self.direction * (self.acceleration / 2)
            if self.velocity.length() > self.max_speed:
                self.velocity = self.velocity.normalize() * self.max_speed
        else:
            if self.velocity.length() > 0:
                self.velocity *= (1 - self.friction)
        self.pos += self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def handle_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.angle += 4
        if pressed[pygame.K_RIGHT]:
            self.angle -= 4
        self.direction = pygame.Vector2(0, -1).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.move()
        self.wrap_around()
