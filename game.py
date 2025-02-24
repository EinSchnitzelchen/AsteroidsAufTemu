import pygame
from screeninfo import get_monitors
from asteroid import Asteroid
from spaceship import Spaceship
from bullet import Bullet
from pathlib import Path
import math

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
        self.level = 1

        #Initialisieren der Assets, die diese Datei braucht
        self.image = pygame.image.load(BASE_DIR / "Assets/background/background.png")
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.shoot_sound = pygame.mixer.Sound(BASE_DIR / "Assets/spaceship/shoot.wav")
        self.asteroid_hit_sound = pygame.mixer.Sound(BASE_DIR / "Assets/asteroid/hit.wav")
        self.spaceship_life_img = pygame.image.load(BASE_DIR / "Assets/spaceship/spaceship.png")
        self.spaceship_life_img = pygame.transform.scale(self.spaceship_life_img, (80, 80))

        self.spaceship_p2_life_img = pygame.image.load(BASE_DIR / "Assets/spaceship/spaceship_p2.png")
        self.spaceship_p2_life_img = pygame.transform.scale(self.spaceship_p2_life_img, (80, 80))
        self.screen = pygame.display.set_mode((screen_width, screen_height))


        self.lives = 4
        self.lifes_p2 = 4

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
                if pygame.sprite.collide_mask(asteroid, bullet):
                    asteroid.hit()
                    bullet.kill()
                    self.score_vel += 1  
                    pygame.mixer.Sound.play(self.asteroid_hit_sound)

        if self.two_player:
            for bullet in self.bullet_group_p2:
                for asteroid in self.asteroid_group:
                    if pygame.sprite.collide_mask(asteroid, bullet):
                        asteroid.hit()
                        bullet.kill()
                        self.score_vel += 1  
                        pygame.mixer.Sound.play(self.asteroid_hit_sound)

        for asteroid in self.asteroid_group:
            if pygame.sprite.collide_mask(self.spaceship, asteroid):
                asteroid.kill()
                self.lives -= 1

            if self.two_player:
                if pygame.sprite.collide_mask(self.spaceship_two , asteroid):
                    asteroid.kill()
                    self.lifes_p2 -= 1
        if self.lives <= 0 and (not self.two_player or self.lifes_p2 <= 0):
            self.show_deathscreen()

    def spawn_asteroids(self):
        for _ in range(5 + self.level - 1):
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

        if self.score_vel == 10:
            self.max_bullets = 5

        self.check_collisions()

        if not self.asteroid_group:
            self.spawn_asteroids()
            self.level += 1

    def draw_lives(self):
        for i in range(self.lives):
            screen.blit(self.spaceship_life_img, (10 + i * 60, screen_height - 90))

        if self.two_player:
            for i in range(self.lifes_p2):
                screen.blit(self.spaceship_p2_life_img, (screen_width - 10 - i * 60, screen_height - 90))

    def show_deathscreen(self):
        self.running = False  # Stoppt das Spiel
        self.screen.fill((0, 0, 0))  # Bildschirm leeren, um Überlagerungen zu verhindern
        self.show_Text()
        pygame.display.flip()
        pygame.time.delay(3000)  # 3 Sekunden warten
        self.reset_game()

    def reset_game(self):
        self.lives = 4
        self.lifes_p2 = 4
        self.score_vel = 0
        self.asteroid_group.empty()
        self.bullet_group.empty()
        self.bullet_group_p2.empty()
        self.spaceship.reset_position()
        if self.two_player:
            self.spaceship_two.reset_position()
        self.running = True
    
    def show_Text(self):
        self.current_frame = 0
        self.font = pygame.font.Font(BASE_DIR / 'Assets/PixelifySans-Regular.ttf', round(screen_width / 32) + round(math.sin(self.current_frame)*2))
        Text = self.font.render("YOU DIED",True, (0, 255, 0))
        text_rect = Text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 100))
        screen.blit(Text, text_rect)

    def draw(self):
        screen.blit(self.image, (0, 0))
        self.all_sprites.draw(screen)
        self.show_score(10, 10)
        self.draw_lives()
        pygame.display.update()
