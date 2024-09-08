import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up display
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dice Roller")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Dice face sizes
dice_size = 200
dot_radius = 15

# Function to draw a dice face
def draw_dice_face(screen, number):
    screen.fill(white)  # Fill the background with white
    font = pygame.font.SysFont(None, 120)
    
    if number == 1:
        pygame.draw.circle(screen, black, (width // 2, height // 2), dot_radius)
    elif number == 2:
        pygame.draw.circle(screen, black, (width // 4, height // 4), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, 3 * height // 4), dot_radius)
    elif number == 3:
        pygame.draw.circle(screen, black, (width // 4, height // 4), dot_radius)
        pygame.draw.circle(screen, black, (width // 2, height // 2), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, 3 * height // 4), dot_radius)
    elif number == 4:
        pygame.draw.circle(screen, black, (width // 4, height // 4), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, height // 4), dot_radius)
        pygame.draw.circle(screen, black, (width // 4, 3 * height // 4), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, 3 * height // 4), dot_radius)
    elif number == 5:
        pygame.draw.circle(screen, black, (width // 4, height // 4), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, height // 4), dot_radius)
        pygame.draw.circle(screen, black, (width // 2, height // 2), dot_radius)
        pygame.draw.circle(screen, black, (width // 4, 3 * height // 4), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, 3 * height // 4), dot_radius)
    elif number == 6:
        pygame.draw.circle(screen, black, (width // 4, height // 6), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, height // 6), dot_radius)
        pygame.draw.circle(screen, black, (width // 4, height // 2), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, height // 2), dot_radius)
        pygame.draw.circle(screen, black, (width // 4, 5 * height // 6), dot_radius)
        pygame.draw.circle(screen, black, (3 * width // 4, 5 * height // 6), dot_radius)
    pygame.display.update()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Roll the dice
    for _ in range(20):  # Number of roll frames
        draw_dice_face(screen, random.randint(1, 6))
        pygame.time.delay(50)  # Adjust to control the speed of the roll

    # Display final face
    draw_dice_face(screen, random.randint(1, 6))

    # Wait for a key press to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False

# Quit pygame
pygame.quit()

