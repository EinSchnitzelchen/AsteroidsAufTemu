import pygame
from screeninfo import get_monitors
from asteroid import Asteroid
from spaceship import Spaceship
from bullet import Bullet
from pathlib import Path

pygame.init()

## GENERAL VARS
display = get_monitors()
BASE_DIR = Path(__file__).parent

## SCREEN SET VARS
screen_width = display[0].width
screen_height = display[0].height
screen = pygame.display.set_mode((screen_width, screen_height))

# FONT
font = pygame.font.Font(BASE_DIR / 'Assets/PixelifySans-Regular.ttf', round(screen_width / 32))

class Game:
    def __init__(self):
        self.run = True
        self.image = pygame.image.load(BASE_DIR / "Assets/background/background.png")
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.spaceship = Spaceship(screen)
        self.all_sprites.add(self.spaceship)
        self.score_vel = 0  # Score als Instanzvariable
        self.shoot_sound = pygame.mixer.Sound(BASE_DIR / "Assets/spaceship/shoot.wav")
        self.asteroid_hit_sound = pygame.mixer.Sound(BASE_DIR / "Assets/asteroid/hit.wav")

        self.spawn_asteroids()

        self.sound = pygame.mixer.Sound(BASE_DIR / "Assets/soundtrack.wav")
        self.channel = self.sound.play(loops = -1)


    def check_collisions(self):
        for bullet in self.bullet_group:
            for asteroid in self.asteroid_group:
                if bullet.rect.colliderect(asteroid.rect):
                    asteroid.hit()
                    bullet.kill()
                    self.score_vel += 1  # Richtig auf Instanzvariable zugreifen
                    pygame.mixer.Sound.play(self.asteroid_hit_sound)
        for asteroid in self.asteroid_group:
            if asteroid.rect.colliderect(self.spaceship.rect):
                asteroid.kill()
                self.score_vel -= 1

    def spawn_asteroids(self):
        for _ in range(5):
            asteroid = Asteroid(screen, self)
            self.asteroid_group.add(asteroid)
            self.all_sprites.add(asteroid)


    def show_score(self, x, y):
        score = font.render("Score: " + str(self.score_vel), True, (0, 255, 0))
        screen.blit(score, (x, y))  # Richtiges Blit-Ziel

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
                    pygame.mixer.Sound.play(self.shoot_sound)

    def update(self):
        self.all_sprites.update()
        for asteroid in self.asteroid_group:
            asteroid.move()
        self.check_collisions()
        if not self.asteroid_group:
            self.spawn_asteroids()


    def draw(self):
        screen.blit(self.image, (0, 0))
        self.all_sprites.draw(screen)
        self.show_score(10, 10)  # Score wird jetzt gezeichnet
        pygame.display.update()
