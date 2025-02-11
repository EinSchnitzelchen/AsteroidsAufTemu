import pygame
import asteroiden
from screeninfo import get_monitors

display  = get_monitors()
display_width = display[0].width
display_height = display[0].height
random = 0
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    asteroiden.spawn(screen)
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000


