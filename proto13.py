import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
screen_width = 1000
screen_height = 800
white = (255, 255, 255)
brown = (139, 69, 19)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(white)
    pygame.draw.line(screen,brown,(100,100),(400,400),7)
    pygame.draw.line(screen,brown,(50,100),(350,400),7)
    pygame.draw.line(screen,brown,(325,375),(375,375),3)
    pygame.draw.line(screen,brown,(300,350),(350,350),3)
    pygame.draw.line(screen,brown,(275,325),(325,325),3)
    pygame.draw.line(screen,brown,(250,300),(300,300),3)
    pygame.draw.line(screen,brown,(225,275),(275,275),3)
    pygame.draw.line(screen,brown,(200,250),(250,250),3)
    pygame.draw.line(screen,brown,(175,225),(225,225),3)
    pygame.draw.line(screen,brown,(150,200),(200,200),3)
    pygame.draw.line(screen,brown,(125,175),(175,175),3)
    pygame.draw.line(screen,brown,(100,150),(150,150),3)
    pygame.draw.line(screen,brown,(75,125),(125,125),3)
    pygame.display.flip()
   

   
