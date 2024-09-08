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

# Set up the clock
clock = pygame.time.Clock()

# Set up the rectangle's initial position and speed
rect_x = 0
rect_y = 0
rect_speed = 10

# Set up the movement direction flags
move_right = True
move_up = False
move_left = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)

    # Move the rectangle based on the direction flags
    if move_right:
        rect_x += rect_speed
        if rect_x >= screen_width - 80:
            move_right = False
            move_up = True
    elif move_up:
        rect_y += rect_speed
        if rect_y >= screen_height - 80:
            move_up = False
            move_left = True
    elif move_left:
        rect_x -= rect_speed
        if rect_x <= 0:
            move_left = False
            move_up = True
    elif move_up:
        rect_y += rect_speed
        if rect_y >= screen_height - 80:
            move_up = False
            move_right = True

    # Draw the rectangle at its new position
    pygame.draw.rect(screen, brown, (rect_x, rect_y, 80, 80))

    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
