import sys
import pygame


class Game:

    def __init__(self):
        self.run = True
        self.screen_width = 1060
        self.screen_height = 798
        WHITE = (255, 255, 255)
        self.image = pygame.Surface((50, 50)) 
        self.image.fill(WHITE)
        self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.all_sprites = pygame.sprite.Group()

        self.bullet_group = pygame.sprite.Group()

        self.tank = Tank()
        self.all_sprites.add(self.tank)

        bullet = Bullet(self.tank)
        self.bullet_group.add(bullet)
        self.all_sprites.add(bullet)


    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.tank.handle_events()


        if keys[pygame.K_UP]:
            self.tank.rect.centery -= 5
        if keys[pygame.K_DOWN]:
            self.tank.rect.centery += 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.tank)
                    self.bullet_group.add(bullet)
                    self.all_sprites.add(bullet)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.update()


class Tank(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Schreibtisch/PYgame/Sprites/tank/tank.png")
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

    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Schreibtisch/PYgame/Sprites/bullet/bullet.png")
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx + 3 # How much pixels from tank turret on x axis
        self.rect.centery = tank.rect.centery - 25 # How much pixels from tank turret on y axis

    def update(self):
        self.rect.y -= 10  # Move up 10 pixels per frame.


def main():
    pygame.init()
    pygame.display.set_caption('Tank Game')
    clock = pygame.time.Clock()
    game = Game()

    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()

    #https://stackoverflow.com/questions/61106297/moving-forward-after-angle-change-pygame/61106823#61106823