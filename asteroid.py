# asteroid.py
import pygame
import random as r
import math
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen, game, size=None, spawned_by_other=False, x=0, y=0):
        super().__init__()

        self.size = 0
        if size is None:
            self.size = r.randint(40, 70)
        else:
            self.size = size
        
        self.asteroid_variation = [
            BASE_DIR / "Assets/asteroid/asteroid.png", 
            BASE_DIR / "Assets/asteroid/asteroid_purple.png",
            BASE_DIR / "Assets/asteroid/asteroid_green.png"
        ]
        
        self.asteroid_small_variation = [
            BASE_DIR / "Assets/asteroid/asteroid_small.png", 
            BASE_DIR / "Assets/asteroid/asteroid_small_purple.png",
            BASE_DIR / "Assets/asteroid/asteroid_small_green.png"
        ]

        self.screen = screen
        self.game = game
        self.rotation = 0
        
        if self.size > 40:
            self.image = pygame.image.load(self.asteroid_variation[r.randint(0,2)])
        else:
            self.image = pygame.image.load(self.asteroid_small_variation[r.randint(0,2)])



        if spawned_by_other:
            self.posx = x
            self.posy = y
            self.set_random_direction()
        else:
            self.spawn()

        self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.posx, self.posy))
        self.original_image = self.image
        self.speed = r.randint(3, 4+ game.level)


    def hit(self):
        if self.size > 40:
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
        self.rotation = self.rotation + 1
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        

    def update(self):
        self.move()
