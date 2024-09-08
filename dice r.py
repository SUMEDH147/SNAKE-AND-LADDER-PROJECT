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

# Dice images
dice_images = [
    pygame.image.load('/Users/sirishapulupula/Downloads/dice1.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice2.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice3.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice4.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice5.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice6.png')
]

# Assume all dice images are the same size
dice_size = dice_images[0].get_width()

# Function to check if the mouse is over the dice
def is_mouse_over_dice(mouse_pos):
    dice_rect = pygame.Rect(width // 2 - dice_size // 2, height // 2 - dice_size // 2, dice_size, dice_size)
    return dice_rect.collidepoint(mouse_pos)

# Function to draw the dice image with rotation
def draw_dice(screen, image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=(width // 2, height // 2))
    screen.blit(rotated_image, rect.topleft)

# Main loop
rolling = False
final_number = 1
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_mouse_over_dice(event.pos):
                rolling = True
                final_number = random.randint(1, 6)  # Final result after rolling
                
                # Spinning effect
                start_time = pygame.time.get_ticks()
                spin_duration = 500  # Duration of spinning in milliseconds
                spin_speed = 360 / 0.5  # Spinning speed (angle per frame)

                while pygame.time.get_ticks() - start_time < spin_duration:
                    angle = ((pygame.time.get_ticks() - start_time) / spin_duration * spin_speed) % 360
                    draw_dice(screen, dice_images[random.randint(0, 5)], angle)
                    pygame.display.flip()
                    clock.tick(60)  # Limit to 60 frames per second

                # Rolling effect
                start_time = pygame.time.get_ticks()
                roll_duration =500 # Duration of rolling in milliseconds

                while pygame.time.get_ticks() - start_time < roll_duration:
                    angle = ((pygame.time.get_ticks() - start_time) / roll_duration * spin_speed) % 360
                    draw_dice(screen, dice_images[random.randint(0, 5)], angle)
                    pygame.display.flip()
                    clock.tick(60)  # Limit to 60 frames per second

                # Final result
                draw_dice(screen, dice_images[final_number - 1], angle)
                pygame.display.flip()
                rolling = False

    if not rolling:
        draw_dice(screen, dice_images[final_number - 1], 0)  # Show the current dice face
        pygame.display.flip()

    clock.tick(30)  # Limit to 30 frames per second overall

