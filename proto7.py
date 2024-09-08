import pygame
import sys
import random

pygame.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake and Ladder Game")
cyan = (0, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


font = pygame.font.Font(None, 64)
welcome_message = font.render("Welcome to Snake and Ladder Game", True, black)


button_width = 200
button_height = 100
button_margin = 50
play_button_x = screen_width // 2 - button_width // 2
play_button_y = screen_height // 2 - button_height // 2
play_button_rect = pygame.Rect(play_button_x, play_button_y, button_width, button_height)
quit_button_x = screen_width // 2 - button_width // 2
quit_button_y = play_button_y + button_height + button_margin
quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)


game_started = False
num = 1
current_dice_image = 0


dice_images = [
    pygame.image.load('dice1.png'),
    pygame.image.load('dice2.png'),
    pygame.image.load('dice3.png'),
    pygame.image.load('dice4.png'),
    pygame.image.load('dice5.png'),
    pygame.image.load('dice6.png')
]
dice_rect = dice_images[0].get_rect()
dice_rect.bottomright = (screen_width, screen_height)


def roll_dice():
    global current_dice_image
    current_dice_image = random.randint(1, 6) - 1


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game_started = True
            elif quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif game_started and dice_rect.collidepoint(event.pos):
                roll_dice()

    screen.fill(cyan)

    if not game_started:
        screen.blit(welcome_message, (screen_width // 2 - welcome_message.get_width() // 2, 50))
        pygame.draw.ellipse(screen, black, play_button_rect, 2)
        play_button_text = font.render("Play", True, black)
        screen.blit(play_button_text, (play_button_x + button_width // 2 - play_button_text.get_width() // 2, play_button_y + button_height // 2 - play_button_text.get_height() // 2))
        pygame.draw.ellipse(screen, black, quit_button_rect, 2)
        quit_button_text = font.render("Quit", True, black)
        screen.blit(quit_button_text, (quit_button_x + button_width // 2 - quit_button_text.get_width() // 2, quit_button_y + button_height // 2 - quit_button_text.get_height() // 2))
    else:
        box_size = 80
        for i in range(10):
            for j in range(10):
                box_x = j * box_size
                box_y = screen_height - (i + 1) * box_size
                box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                if num % 2 == 0:
                    pygame.draw.rect(screen, red, box_rect, 1)
                else:
                    pygame.draw.rect(screen, red, box_rect)
                font = pygame.font.Font(None, 36)
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=box_rect.center)
                screen.blit(text, text_rect)
                num += 1
        screen.blit(dice_images[current_dice_image], dice_rect)

    pygame.display.flip()
