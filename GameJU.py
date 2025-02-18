import sys
import pygame
from pathlib import Path
from screeninfo import get_monitors
import random as r

BASE_DIR = Path(__file__).parent
display = get_monitors()
level = 1

score = 0
score_increment = 10

screen_width = display[0].width
screen_height = display[0].height
screen = pygame.display.set_mode((screen_width, screen_height))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen, level):
        self.screen = screen
        self.spawn()
        if level < 13:
            self.speed = r.randint(4 + level, (level + 7))
        else:
            self.speed = r.randint(4 + 13, (level + 20))
    
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
        dy = midy + r.randint(0, 20) - self.posy
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



class Spaceship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(BASE_DIR / "Sprites/spaceship/spaceship.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.75)
        self.org_image = self.image.copy()
        self.rect = self.image.get_rect(center=(70, 600))
        self.angle = 0
        self.direction = pygame.Vector2(0, -1)
        self.pos = pygame.Vector2(self.rect.center)

        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 0.3
        self.max_speed = 10
        self.friction = 0.02

    def wrap_around(self):
        if self.pos.x < 0:
            self.pos.x = screen.get_width()
        elif self.pos.x > screen.get_width():
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = screen.get_height()
        elif self.pos.y > screen.get_height():
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
            self.angle += 3
        if pressed[pygame.K_RIGHT]:
            self.angle -= 3
        self.direction = pygame.Vector2(0, -1).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.move()
        self.wrap_around()

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

class Score():
    def __init__(self):
     pass
class Game:
    def __init__(self):
        self.run = True
        self.image = pygame.image.load(BASE_DIR / "Sprites/background/background.png") 
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.spaceship = Spaceship()
        self.all_sprites.add(self.spaceship)
        self.asteroids = [Asteroid(screen, level) for _ in range(5)]

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
                    #score += score_increment
                    

    def update(self):
        self.all_sprites.update()
        for asteroid in self.asteroids:
            asteroid.move()

    def draw(self):
        screen.blit(self.image, (0, 0))
        self.all_sprites.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw()
        pygame.display.update()

def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Spaceship Game')
    clock = pygame.time.Clock()
    game = Game()
    font = pygame.font.Font(None, 36)
    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (100, 100))
        clock.tick(60)

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
