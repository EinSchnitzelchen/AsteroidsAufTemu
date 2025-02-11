import random as r
import pygame

class astroids:
    def spawn(screen):
        random = r.randint(1,4)
        if random == 1:
            r2 = r.randint(0, screen.get_width())
            pygame.draw.circle(screen, "red", (r2,0),40)
        elif random == 2:
            r2 = r.randint(0, screen.get_width())
            pygame.draw.circle(screen, "red", (r2,screen.get_height()),40)
        elif random == 3:
            r2 = r.randint(0, screen.get_height())
            pygame.draw.circle(screen, "red", (0,r2),40)
        elif random == 4:
            r2 = r.randint(0, screen.get_height())
            pygame.draw.circle(screen, "red", (screen.get_width(),r2),40)