import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
screen_width = 1000
screen_height = 800
box_size = 80
red = (255, 0, 0)
dark_red = (139, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the player symbols
player1_symbol = pygame.image.load('/Users/sirishapulupula/Downloads/pawn.png')
player2_symbol = pygame.image.load('/Users/sirishapulupula/Downloads/pawng.png')

# Set up the dice images
dice_images = [
    pygame.image.load('/Users/sirishapulupula/Downloads/dice1.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice2.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice3.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice4.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice5.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice6.png')
]

# Set up the game state
player_turns = [1, 2]
current_turn = 0
player1_pos = 1
player2_pos = 1
player1_destination = 1
player2_destination = 1
player_moving = False
rolled_dice = None

# Set up the snakes and ladders
snakes = [
    {"start": 17, "end": 1},
    {"start": 52, "end": 29},
    {"start": 62, "end": 19},
    {"start": 88, "end": 36},
    {"start": 95, "end": 42},
    {"start": 97, "end": 79},
    {"start": 99, "end": 46}
]

ladders = [
    {"start": 3, "end": 20},
    {"start": 6, "end": 14},
    {"start": 11, "end": 28},
    {"start": 15, "end": 34},
    {"start": 22, "end": 38},
    {"start": 44, "end": 59},
    {"start": 77, "end": 98}
]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_moving:
                continue
            rolled_dice = random.randint(1, 6)
            if player_turns[current_turn] == 1:
                player1_destination = player1_pos + rolled_dice
                player_moving = True
            else:
                player2_destination = player2_pos + rolled_dice
                player_moving = True

    # Move player
    if player_moving:
        if player_turns[current_turn] == 1:
            if player1_pos < player1_destination:
                player1_pos += 1
                for ladder in ladders:
                    if player1_pos == ladder["start"]:
                        player1_pos = ladder["end"]
                        print("Player 1 climbed a ladder!")
                for snake in snakes:
                    if player1_pos == snake["start"]:
                        player1_pos = snake["end"]
                        print("Player 1 fell down a snake!")
            else:
                player_moving = False
                current_turn = (current_turn + 1) % 2
        else:
            if player2_pos < player2_destination:
                player2_pos += 1
                for ladder in ladders:
                    if player2_pos == ladder["start"]:
                        player2_pos = ladder["end"]
                        print("Player 2 climbed a ladder!")
                for snake in snakes:
                    if player2_pos == snake["start"]:
                        player2_pos = snake["end"]
                        print("Player 2 fell down a snake!")
            else:
                player_moving = False
                current_turn = (current_turn + 1) % 2

    # Draw everything
    screen.fill(white)
    for i in range(10):
        for j in range(10):
            box_x = j * box_size
            box_y = screen_height - (i + 1) * box_size
            box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
            pygame.draw.rect(screen, red, box_rect, 1)
            text = font.render(str(i * 10 + j + 1), True, black)
            text_rect = text.get_rect(center=box_rect.center)
            screen.blit(text, text_rect)

    for snake in snakes:
        start_x = ((snake["start"] - 1) % 10) * box_size + 30
        start_y = screen_height - (((snake["start"] - 1) // 10) % 10 + 1) * box_size + 30
        if (snake["start"] - 1) // 10 % 2 == 1:
            start_x = (9 - ((snake["start"] - 1) % 10)) * box_size + 30
        end_x = ((snake["end"] - 1) % 10) * box_size + 30
        end_y = screen_height - (((snake["end"] - 1) // 10) % 10 + 1) * box_size + 30
        if (snake["end"] - 1) // 10 % 2 == 1:
            end_x = (9 - ((snake["end"] - 1) % 10)) * box_size + 30
        pygame.draw.line(screen, (0, 0, 255), (start_x, start_y), (end_x, end_y), 5)

    for ladder in ladders:
        start_x = ((ladder["start"] - 1) % 10) * box_size + 30
        start_y = screen_height - (((ladder["start"] - 1) // 10) % 10 + 1) * box_size + 30
        if (ladder["start"] - 1) // 10 % 2 == 1:
            start_x = (9 - ((ladder["start"] - 1) % 10)) * box_size + 30
        end_x = ((ladder["end"] - 1) % 10) * box_size + 30
        end_y = screen_height - (((ladder["end"] - 1) // 10) % 10 + 1) * box_size + 30
        if (ladder["end"] - 1) // 10 % 2 == 1:
            end_x = (9 - ((ladder["end"] - 1) % 10)) * box_size + 30
        pygame.draw.line(screen, (0, 255, 255), (start_x, start_y), (end_x, end_y), 5)

    player1_x = ((player1_pos - 1) % 10) * box_size + 30
    player1_y = screen_height - (((player1_pos - 1) // 10) % 10 + 1) * box_size + 10
    if (player1_pos - 1) // 10 % 2 == 1:
        player1_x = (9 - ((player1_pos - 1) % 10)) * box_size + 10
    screen.blit(player1_symbol, (player1_x, player1_y))

    player2_x = ((player2_pos - 1) % 10) * box_size + 30
    player2_y = screen_height - (((player2_pos - 1) // 10) % 10 + 1) * box_size + 10
    if (player2_pos - 1) // 10 % 2 == 1:
        player2_x = (9 - ((player2_pos - 1) % 10)) * box_size + 10
    screen.blit(player2_symbol, (player2_x, player2_y))

    if rolled_dice is not None:
        dice_image_y = screen_height - dice_images[0].get_height() - 20
        screen.blit(dice_images[rolled_dice - 1], (screen_width - dice_images[0].get_width() - 20, dice_image_y))

    pygame.display.flip()

    # Check for win
    if player1_pos == 100:
        print("Player 1 wins!")
        break
    elif player2_pos == 100:
        print("Player 2 wins!")
        break
pygame.quit()
pygame.exit()
