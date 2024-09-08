import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
screen_width = 800
screen_height = 600
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the clock
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)

    # Draw the rectangle with curved edges
    rect_x = 100
    rect_y = 100
    rect_width = 200
    rect_height = 200
    corner_radius = 20

    pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height), 2)

    # Draw the curved edges
    pygame.draw.arc(screen, black, (rect_x, rect_y, corner_radius*2, corner_radius*2), 0, 3.14/2)
    pygame.draw.arc(screen, black, (rect_x+rect_width-corner_radius*2, rect_y, corner_radius*2, corner_radius*2), 3.14/2, 3.14)
    pygame.draw.arc(screen, black, (rect_x, rect_y+rect_height-corner_radius*2, corner_radius*2, corner_radius*2), 3.14, 3.14*3/2)
    pygame.draw.arc(screen, black, (rect_x+rect_width-corner_radius*2, rect_y+rect_height-corner_radius*2, corner_radius*2, corner_radius*2), 3.14*3/2, 0)

    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
