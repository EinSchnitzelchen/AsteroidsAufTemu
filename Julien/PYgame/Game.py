import sys
import pygame
from pathlib import Path
from screeninfo import get_monitors
import random as r

BASE_DIR = Path(__file__).parent
display  = get_monitors()
random = 0
level = 1

screen_width = display[0].width
screen_height = display[0].height
screen = pygame.display.set_mode((screen_width, screen_height))

class Game:

    def __init__(self):
        self.run = True
        self.image = pygame.image.load(BASE_DIR / "Sprites/background/background.png") 
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))

        self.all_sprites = pygame.sprite.Group()

        self.bullet_group = pygame.sprite.Group()

        self.spaceship = Spaceship()
        self.all_sprites.add(self.spaceship)

        bullet = Bullet(self.spaceship)
        self.bullet_group.add(bullet)
        self.all_sprites.add(bullet)
        


    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.spaceship.handle_events()


        if keys[pygame.K_UP]:
            self.spaceship.move(-5)
        if keys[pygame.K_DOWN]:
            self.spaceship.move(5)

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

    def draw(self):
        screen.blit(self.image, (0, 0))
        self.all_sprites.draw(screen)
        pygame.display.update()

    


class Asteroid:
    def __init__(self, screen, level):
        screen = screen
        self.spawn()
        if level < 13:
            self.speed = r.randint(4 + level, (level + 7) )
        else:
            self.speed = r.randint(4 + 13, (level + 20) )
    


    def spawn(self):
        random_side = r.randint(1, 4)
        if random_side in [1, 2]:  # Oben oder unten
            self.posx = r.randint(0, screen.get_width())
            self.posy = 0 if random_side == 1 else screen.get_height()
        else:  # Links oder rechts
            self.posx = 0 if random_side == 3 else screen.get_width()
            self.posy = r.randint(0, screen.get_height())

        midx = screen.get_width() // 2
        midy = screen.get_height() // 2
        dx = midx + r.randint(0, 20) - self.posx
        dy = midy + r.randint(0, 20) -self.posy
        dist = (dx**2 + dy**2) ** 0.5

        self.dirx = dx / dist
        self.diry = dy / dist

    def wrap_around(self):
        if self.posx < 0:
            self.posx = screen.get_width()
        elif self.posx > screen.get_width():
             self.posx = 0

        if self.posy < 0:
            self.posy = screen.get_height()
        elif self.posy > screen.get_height():
            self.posy = 0
    
    def move(self):
        self.posx += self.speed * self.dirx
        self.posy += self.speed * self.diry
        self.wrap_around()



    def draw(self):
        pygame.draw.circle(screen, "white", (int(self.posx), int(self.posy)), 40)


class Spaceship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(BASE_DIR / "Sprites/spaceship/spaceship.png")
        self.org_image = self.image.copy()

    
        self.rect = self.image.get_rect(center=(70, 600))
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)

    def move(self, velocity):
        direction = pygame.Vector2(0, velocity).rotate(-self.angle)
        self.pos += direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])

    def handle_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.angle += 3
        if pressed[pygame.K_RIGHT]:
            self.angle -= 3

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)





class Bullet(pygame.sprite.Sprite):

    def __init__(self, spaceship):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(BASE_DIR / "Sprites/bullet/bullet.png")
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()

        # offset für den Bulletspawn (später ändern)
        self.rect.centerx = spaceship.rect.centerx 
        self.rect.centery = spaceship.rect.centery 

        self.direction = pygame.Vector2(0, -1).rotate(-spaceship.angle)
        self.pos = pygame.Vector2(self.rect.center)

    def update(self):
        self.pos += self.direction * 10
        self.rect.center = round(self.pos.x), round(self.pos.y)

def main():
    pygame.init()
    pygame.display.set_caption('Spaceship Game')
    clock = pygame.time.Clock()
    game = Game()
    asteroids = [Asteroid(screen, level) for _ in range(5)]

    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)
        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw()

        
if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()