import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# Screen settings
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake and Ladder Game")

# Colors
cyan = (135, 206, 235)
white = (255, 255, 255)
black = (0, 0, 0)
red = (178, 34, 34)
dark_red = (135, 206, 235)
green = (0, 128, 0)

# Font and sound
font = pygame.font.Font(None, 64)
roll_sound = pygame.mixer.Sound('/Users/sirishapulupula/Downloads/dice sound.mp3')

# Welcome screen setup
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

# Dice images
dice_images = [
    pygame.image.load('/Users/sirishapulupula/Downloads/dice1.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice2.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice3.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice4.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice5.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice6.png')
]
dice_button_width = dice_images[0].get_width()
dice_button_height = dice_images[0].get_height()
dice_button_x = screen_width - dice_button_width - 20
dice_button_y = screen_height - dice_button_height - 20
dice_button_rect = pygame.Rect(dice_button_x, dice_button_y, dice_button_width, dice_button_height)

# Player symbols
player1_symbol = pygame.image.load('/Users/sirishapulupula/Downloads/pawn.png')
player2_symbol = pygame.image.load('/Users/sirishapulupula/Downloads/pawng.png')

# Player initial positions
player1_pos = 1
player2_pos = 1
player1_x, player1_y = 30, screen_height - 70
player2_x, player2_y = 30, screen_height - 70
player1_queue = []
player2_queue = []

# Turn handling
player_turns = [1, 2]
current_turn = 0
rolled_dice = None

# Snakes and Ladders
snakes = [
    {"start": 22, "end": 1},
    {"start": 55, "end": 16},
    {"start": 62, "end": 41},
    {"start": 93, "end": 49},
    {"start": 95, "end": 74},
    {"start": 71, "end": 9},
    {"start": 99, "end": 56}
]

ladders = [
    {"start": 65, "end": 86},
    {"start": 6, "end": 14},
    {"start": 28, "end": 48},
    {"start": 54, "end": 73},
    {"start": 17, "end": 38},
    {"start": 44, "end": 58},
    {"start": 77, "end": 98}
]

def calculate_position(position):
    """Calculate the (x, y) screen coordinates based on the board position."""
    row = (position - 1) // 10
    col = (position - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * 80 + 10
    y = screen_height - (row + 1) * 80 + 10
    return x, y

def interpolate_movement(start_x, start_y, end_x, end_y, steps):
    """Interpolate positions for smooth movement."""
    movement = []
    for i in range(steps):
        x = start_x + (end_x - start_x) * i / steps
        y = start_y + (end_y - start_y) * i / steps
        movement.append((x, y))
    movement.append((end_x, end_y))
    return movement

def update_queue(start_pos, end_pos, queue, ladder=None, snake=None, steps=20):
    """Update the movement queue for players."""
    queue.clear()
    if ladder:
        ladder_start_x, ladder_start_y = calculate_position(ladder["start"])
        ladder_end_x, ladder_end_y = calculate_position(ladder["end"])
        queue.extend(interpolate_movement(ladder_start_x, ladder_start_y, ladder_end_x, ladder_end_y, steps))
    elif snake:
        snake_start_x, snake_start_y = calculate_position(snake["start"])
        snake_end_x, snake_end_y = calculate_position(snake["end"])
        queue.extend(interpolate_movement(snake_start_x, snake_start_y, snake_end_x, snake_end_y, steps))
    else:
        for pos in range(start_pos + 1, end_pos + 1):
            x, y = calculate_position(pos)
            queue.append((x, y))

def draw_ladders(screen, ladders):
    """Draw ladders on the board."""
    for ladder in ladders:
        start_x1 = ((ladder["start"] - 1) % 10) * 80 + 20
        start_x2 = ((ladder["start"] - 1) % 10) * 80 + 60
        start_y = screen_height - (((ladder["start"] - 1) // 10) % 10 + 1) * 80 + 40
        if (ladder["start"] - 1) // 10 % 2 == 1:
            start_x1 = (9 - ((ladder["start"] - 1) % 10)) * 80 + 20
            start_x2 = (9 - ((ladder["start"] - 1) % 10)) * 80 + 60
        end_x1 = ((ladder["end"] - 1) % 10) * 80 + 20
        end_x2 = ((ladder["end"] - 1) % 10) * 80 + 60
        end_y = screen_height - (((ladder["end"] - 1) // 10) % 10 + 1) * 80 + 40
        if (ladder["end"] - 1) // 10 % 2 == 1:
            end_x1 = (9 - ((ladder["end"] - 1) % 10)) * 80 + 20
            end_x2 = (9 - ((ladder["end"] - 1) % 10)) * 80 + 60
        spacing = (end_y - start_y) / 6
        for i in range(1, 6):
            t = (i * spacing) / (end_y - start_y)
            x = start_x1 + (end_x1 - start_x1) * t
            y = start_y + i * spacing
            pygame.draw.line(screen, (204, 102, 0), (x, y), (x + 40, y), 3)
        pygame.draw.line(screen, (204, 102, 0), (start_x1, start_y), (end_x1, end_y), 7)
        pygame.draw.line(screen, (204, 102, 0), (start_x2, start_y), (end_x2, end_y), 7)

def draw_snakes(screen, snakes):
    """Draw snakes on the board."""
    for snake in snakes:
        start_x = ((snake["start"] - 1) % 10) * 80 + 30
        start_y = screen_height - (((snake["start"] - 1) // 10) % 10 + 1) * 80 + 30
        if (snake["start"] - 1) // 10 % 2 == 1:
            start_x = (9 - ((snake["start"] - 1) % 10)) * 80 + 30
        end_x = ((snake["end"] - 1) % 10) * 80 + 30
        end_y = screen_height - (((snake["end"] - 1) // 10) % 10 + 1) * 80 + 30
        if (snake["end"] - 1) // 10 % 2 == 1:
            end_x = (9 - ((snake["end"] - 1) % 10)) * 80 + 30
        pygame.draw.line(screen, dark_red, (start_x, start_y), (end_x, end_y), 5)
        pygame.draw.circle(screen, red, (start_x, start_y), 20)
        pygame.draw.circle(screen, green, (end_x, end_y), 20)

def roll_dice():
    """Simulate dice roll."""
    return random.randint(1, 6)

def handle_player_move(player_pos, rolled_dice, player_queue, player_x, player_y):
    """Handle the player movement based on dice roll and handle snakes and ladders."""
    new_pos = player_pos + rolled_dice
    if new_pos > 100:
        return player_pos, player_queue, player_x, player_y

    for ladder in ladders:
        if new_pos == ladder["start"]:
            update_queue(player_pos, ladder["start"], player_queue)
            player_pos = ladder["end"]
            update_queue(ladder["start"], player_pos, player_queue, ladder=ladder)
            return player_pos, player_queue, player_x, player_y

    for snake in snakes:
        if new_pos == snake["start"]:
            update_queue(player_pos, snake["start"], player_queue)
            player_pos = snake["end"]
            update_queue(snake["start"], player_pos, player_queue, snake=snake)
            return player_pos, player_queue, player_x, player_y

    update_queue(player_pos, new_pos, player_queue)
    player_pos = new_pos

    return player_pos, player_queue, player_x, player_y

def main_game():
    global player1_pos, player2_pos, current_turn, rolled_dice
    global player1_x, player1_y, player2_x, player2_y
    global player1_queue, player2_queue  # Ensure queues are global

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if dice_button_rect.collidepoint(event.pos):
                    roll_sound.play()
                    rolled_dice = roll_dice()

        screen.fill(cyan)

        # Draw board
        for row in range(10):
            for col in range(10):
                x = col * 80
                y = screen_height - (row + 1) * 80
                pygame.draw.rect(screen, white, (x, y, 80, 80))
                position = row * 10 + (col + 1) if row % 2 == 0 else row * 10 + (10 - col)
                text = font.render(str(position), True, black)
                screen.blit(text, (x + 30, y + 20))

        # Draw snakes and ladders
        draw_ladders(screen, ladders)
        draw_snakes(screen, snakes)

        # Draw dice
        if rolled_dice:
            dice_image = dice_images[rolled_dice - 1]
            screen.blit(dice_image, (dice_button_x, dice_button_y))
        else:
            screen.blit(dice_images[0], (dice_button_x, dice_button_y))

        # Update player positions based on queue
        if player1_queue:
            player1_x, player1_y = player1_queue.pop(0)
        if player2_queue:
            player2_x, player2_y = player2_queue.pop(0)

        # Draw players
        screen.blit(player1_symbol, (player1_x, player1_y))
        screen.blit(player2_symbol, (player2_x, player2_y))

        # Handle player turn and move
        if rolled_dice:
            if player_turns[current_turn] == 1:
                player1_pos, player1_queue, player1_x, player1_y = handle_player_move(player1_pos, rolled_dice, player1_queue, player1_x, player1_y)
            else:
                player2_pos, player2_queue, player2_x, player2_y = handle_player_move(player2_pos, rolled_dice, player2_queue, player2_x, player2_y)
            rolled_dice = None
            current_turn = (current_turn + 1) % len(player_turns)

        # Check for winner
        if player1_pos == 100:
            winner_message = font.render("Player 1 Wins!", True, black)
            screen.blit(winner_message, (screen_width // 2 - 200, screen_height // 2 - 32))
            pygame.display.flip()
            pygame.time.delay(2000)
            game_over = True
        elif player2_pos == 100:
            winner_message = font.render("Player 2 Wins!", True, black)
            screen.blit(winner_message, (screen_width // 2 - 200, screen_height // 2 - 32))
            pygame.display.flip()
            pygame.time.delay(2000)
            game_over = True

        pygame.display.flip()
        clock.tick(30)  # Control frame rate for smoother animations

def welcome_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    main_game()
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(cyan)
        screen.blit(welcome_message, (screen_width // 2 - welcome_message.get_width() // 2, screen_height // 4))

        # Draw buttons
        pygame.draw.rect(screen, black, play_button_rect)
        pygame.draw.rect(screen, black, quit_button_rect)

        play_text = font.render("Play", True, white)
        screen.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))

        quit_text = font.render("Quit", True, white)
        screen.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))

        pygame.display.flip()

welcome_screen()
