import pygame
from screeninfo import get_monitors
import random as r

level = 1

display  = get_monitors()
display_width = display[0].width
display_height = display[0].height
random = 0
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
running = True

class Asteroid:
    def __init__(self, screen, level):
        self.screen = screen
        self.spawn()
        if level < 13:
            self.speed = r.randint(4 + level, (level + 7) )
        else:
            self.speed = r.randint(4 + 13, (level + 20) )
    


    def spawn(self):
        random_side = r.randint(1, 4)
        if random_side in [1, 2]:  # Oben oder unten
            self.posx = r.randint(0, self.screen.get_width())
            self.posy = 0 if random_side == 1 else self.screen.get_height()
        else:  # Links oder rechts
            self.posx = 0 if random_side == 3 else self.screen.get_width()
            self.posy = r.randint(0, self.screen.get_height())

        midx = self.screen.get_width() // 2
        midy = self.screen.get_height() // 2
        dx = midx + r.randint(0, 20) - self.posx
        dy = midy + r.randint(0, 20) -self.posy
        dist = (dx**2 + dy**2) ** 0.5

        self.dirx = dx / dist
        self.diry = dy / dist

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
        self.wrap_around()



    def draw(self):
        pygame.draw.circle(self.screen, "white", (int(self.posx), int(self.posy)), 40)

        
asteroids = [Asteroid(screen, level) for _ in range(5)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw()

    
    pygame.display.flip()
    dt = clock.tick(60) / 1000


