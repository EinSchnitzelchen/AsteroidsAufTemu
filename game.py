import pygame
from screeninfo import get_monitors
from asteroid import Asteroid
from spaceship import Spaceship
from bullet import Bullet
from pathlib import Path

pygame.init()

#Generelle Variablen
display = get_monitors()
BASE_DIR = Path(__file__).parent        #Gibt den Pfad zu dem Projetz an, egal in welchem Ordner er ist

#Variablen für die Größe des Bildschirms
screen_width = display[0].width
screen_height = display[0].height
screen = pygame.display.set_mode((screen_width, screen_height))

# Hier wird das Text Objekt erstellt mit der lokalen Schriftart
font = pygame.font.Font(BASE_DIR / 'Assets/PixelifySans-Regular.ttf', round(screen_width / 32))

class Game:
    def __init__(self, two_player = False):
        self.run = True
        self.two_player = two_player

        #Initialisieren der Assets, die diese Datei braucht
        self.image = pygame.image.load(BASE_DIR / "Assets/background/background.png")
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.shoot_sound = pygame.mixer.Sound(BASE_DIR / "Assets/spaceship/shoot.wav")
        self.asteroid_hit_sound = pygame.mixer.Sound(BASE_DIR / "Assets/asteroid/hit.wav")
        self.sound = pygame.mixer.Sound(BASE_DIR / "Assets/soundtrack.wav")

        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.bullet_group_p2 = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.max_bullets = 2

        self.spaceship = Spaceship(screen, False)

        if two_player:
            self.spaceship_two = Spaceship(screen, True)
            self.all_sprites.add(self.spaceship_two)

        self.all_sprites.add(self.spaceship)
        self.score_vel = 0 

        self.spawn_asteroids()
        self.channel = self.sound.play(loops = -1)


    def check_collisions(self):
        for bullet in self.bullet_group:
            for asteroid in self.asteroid_group:
                if bullet.rect.colliderect(asteroid.rect):
                    asteroid.hit()
                    bullet.kill()
                    self.score_vel += 1  
                    pygame.mixer.Sound.play(self.asteroid_hit_sound)

        if self.two_player:
            for bullet in self.bullet_group_p2:
                for asteroid in self.asteroid_group:
                    if bullet.rect.colliderect(asteroid.rect):
                        asteroid.hit()
                        bullet.kill()
                        self.score_vel += 1  
                        pygame.mixer.Sound.play(self.asteroid_hit_sound)

        for asteroid in self.asteroid_group:
            if asteroid.rect.colliderect(self.spaceship.rect):
                asteroid.kill()
                self.score_vel -= 1

            if self.two_player:
                if asteroid.rect.colliderect(self.spaceship_two.rect) & self.two_player:
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

        if self.two_player:
            self.spaceship_two.handle_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False

                if event.key == pygame.K_SPACE:
                    if not self.two_player:
                        if self.bullet_group.__len__() < self.max_bullets:
                            bullet = Bullet(self.spaceship, screen)
                            self.bullet_group.add(bullet)
                            self.all_sprites.add(bullet)
                            pygame.mixer.Sound.play(self.shoot_sound)

                    else:
                        if self.bullet_group_p2.__len__() < self.max_bullets:
                            bullet = Bullet(self.spaceship_two,screen)
                            self.bullet_group_p2.add(bullet)
                            self.all_sprites.add(bullet)
                            pygame.mixer.Sound.play(self.shoot_sound)

                if event.key == pygame.K_RSHIFT:
                    if self.two_player:
                        if self.bullet_group.__len__() < self.max_bullets:
                            bullet = Bullet(self.spaceship, screen)
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
