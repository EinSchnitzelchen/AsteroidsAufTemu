# asteroid.py
import pygame
import random as r
import math
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen, game, size=None, spawned_by_other=False, x=0, y=0):
        super().__init__()
        self.size = size if size else r.randint(40, 70)
        self.screen = screen
        self.game = game

        if spawned_by_other:
            self.posx = x
            self.posy = y
            self.set_random_direction()
        else:
            self.spawn()

        self.image = pygame.image.load(BASE_DIR / "Sprites/asteroid/asteroid.png")
        self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
        self.rect = self.image.get_rect(center=(self.posx, self.posy))

        self.speed = r.randint(3, 5)

    def hit(self):
        if self.size > 30:
            new_size = self.size / 2
            self.game.new_asteroid(new_size, self.posx, self.posy)
            self.game.new_asteroid(new_size, self.posx, self.posy)
        self.kill()

    def spawn(self):
        random_side = r.randint(1, 4)
        if random_side in [1, 2]:
            self.posx = r.randint(0, self.screen.get_width())
            self.posy = 0 if random_side == 1 else self.screen.get_height()
        else:
            self.posx = 0 if random_side == 3 else self.screen.get_width()
            self.posy = r.randint(0, self.screen.get_height())

        midx = self.screen.get_width() // 2
        midy = self.screen.get_height() // 2
        dx = midx + r.randint(0, 20) - self.posx
        dy = midy + r.randint(0, 20) - self.posy
        dist = (dx**2 + dy**2) ** 0.5

        self.dirx = dx / dist
        self.diry = dy / dist

    def set_random_direction(self):
        angle = math.radians(r.uniform(0, 360))
        self.dirx = math.cos(angle)
        self.diry = math.sin(angle)

    def wrap_around(self):
        if self.posx < 0:
            self.posx = self.screen.get_width()
        elif self.posx > self.screen.get_width():
            self.posx = 0

        if self.posy < 0:
            self.posy = self.screen.get_height()
        elif self.posy > self.screen.get_height():
            self.posy = 0

    def move(self):
        self.posx += self.speed * self.dirx
        self.posy += self.speed * self.diry
        self.rect.center = (self.posx, self.posy)
        self.wrap_around()

    def update(self):
        self.move()
