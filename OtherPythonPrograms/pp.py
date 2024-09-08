import pygame
import sys
import random
import time 

pygame.init()
pygame.mixer.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake and Ladder Game")

cyan = (135, 206, 235)
white = (255, 255, 255)
black = (0, 0, 0)
red = (178, 34, 34)
dark_red = (135, 206, 235)
green = (0, 128, 0)

font = pygame.font.Font(None, 64)
fontt = pygame.font.Font(None, 32)
roll_sound = pygame.mixer.Sound('/Users/sirishapulupula/Downloads/dice sound.mp3')

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

player1_symbol = pygame.image.load('/Users/sirishapulupula/Downloads/pawn.png')
player2_symbol = pygame.image.load('/Users/sirishapulupula/Downloads/pawng.png')

player1_pos = 1
player2_pos = 1
player1_x, player1_y = 30, screen_height - 70
player2_x, player2_y = 30, screen_height - 70
player1_queue = []
player2_queue = []

player_turns = [1, 2]
current_turn = 0
rolled_dice = None

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
    row = (position - 1) // 10
    col = (position - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * 80 + 10
    y = screen_height - (row + 1) * 80 + 10
    return x, y

def draw_dice_roll_text(screen, dice_value):
    dice_text = fontt.render(f"Dice Rolled: {dice_value}", True, black)
    screen.blit(dice_text, (800,40))

def interpolate_movement(start_x, start_y, end_x, end_y, steps=5):
    movement = []
    for i in range(steps):
        x = start_x + (end_x - start_x) * i / steps
        y = start_y + (end_y - start_y) * i / steps
        movement.append((x, y))
    movement.append((end_x, end_y))
    return movement
def slide_down_snake(start_x, start_y, end_x, end_y, steps=100):
    movement = []
    for i in range(steps):
        x = start_x + (end_x - start_x) * i / steps
        y = start_y + (end_y - start_y) * i / steps
        movement.append((x, y))
    movement.append((end_x, end_y))
    return movement

def update_queue(start_pos, end_pos, queue, ladder=None, snake=None, steps=5):
    queue.clear()

    if ladder:
        for pos in range(start_pos + 1, ladder["start"]):
            x, y = calculate_position(pos)
            queue.append((x, y))
        queue.append(calculate_position(ladder["start"]))
        ladder_start_x, ladder_start_y = calculate_position(ladder["start"])
        ladder_end_x, ladder_end_y = calculate_position(ladder["end"])
        queue.extend(interpolate_movement(ladder_start_x, ladder_start_y, ladder_end_x, ladder_end_y, steps))
    elif snake:
        for pos in range(start_pos + 1, snake["start"]):
            x, y = calculate_position(pos)
            queue.append((x, y))
        queue.append(calculate_position(snake["start"]))
        snake_start_x, snake_start_y = calculate_position(snake["start"])
        snake_end_x, snake_end_y = calculate_position(snake["end"])
        queue.extend(slide_down_snake(snake_start_x, snake_start_y, snake_end_x, snake_end_y, steps))
    else:
        for pos in range(start_pos + 1, end_pos + 1):
            x, y = calculate_position(pos)
            queue.append((x, y))

def draw_dice(screen, image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=(x, y))
    screen.blit(rotated_image, rect.topleft)

def roll_dice_animation():
    global rolled_dice
    rolled_dice = random.randint(1, 6)
    start_time = pygame.time.get_ticks()
    spin_duration = 500 
    spin_speed = 360 / 0.5  
    dice_x = 930
    dice_y = 730


    while pygame.time.get_ticks() - start_time < spin_duration:
        angle = ((pygame.time.get_ticks() - start_time) / spin_duration * spin_speed) % 360
        draw_board()
        screen.blit(player1_symbol, (player1_x, player1_y))
        screen.blit(player2_symbol, (player2_x, player2_y))
        draw_ladders(screen,ladders)
        draw_snakes(screen,snakes)
        draw_dice(screen, dice_images[random.randint(0, 5)], angle, dice_x, dice_y)
        pygame.display.flip()
        pygame.time.delay(20) 
    rolled_dice=random.randint(1,6)


    start_time = pygame.time.get_ticks()
    roll_duration = 500 

    while pygame.time.get_ticks() - start_time < roll_duration:
        angle = ((pygame.time.get_ticks() - start_time) / roll_duration * spin_speed) % 360
        draw_board()
        screen.blit(player1_symbol, (player1_x, player1_y))
        screen.blit(player2_symbol, (player2_x, player2_y))
        draw_ladders(screen,ladders)
        draw_snakes(screen,snakes)
        draw_dice(screen, dice_images[random.randint(0, 5)], angle, dice_x, dice_y)
        pygame.display.flip()
        pygame.time.delay(20)

    draw_board()
    screen.blit(player1_symbol, (player1_x, player1_y))
    screen.blit(player2_symbol, (player2_x, player2_y))
    draw_ladders(screen,ladders)
    draw_snakes(screen,snakes)
    draw_dice(screen, dice_images[rolled_dice - 1], 0, dice_x, dice_y)
    pygame.display.flip()

    return rolled_dice

def handle_dice_roll():
    global rolled_dice
    rolled_dice = roll_dice_animation()
    print("Dice Rolled:", rolled_dice)


def draw_ladders(screen, ladders):
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
    for snake in snakes:
        start_x = ((snake["start"] - 1) % 10) * 80 + 30
        start_y = screen_height - (((snake["start"] - 1) // 10) % 10 + 1) * 80 + 30
        if (snake["start"] - 1) // 10 % 2 == 1:
            start_x = (9 - ((snake["start"] - 1) % 10)) * 80 + 30
        end_x = ((snake["end"] - 1) % 10) * 80 + 30
        end_y = screen_height - (((snake["end"] - 1) // 10) % 10 + 1) * 80 + 30
        if (snake["end"] - 1) // 10 % 2 == 1:
            end_x = (9 - ((snake["end"] - 1) % 10)) * 80 + 30
        pygame.draw.line(screen, green, (start_x, start_y), (end_x, end_y), 5)

def roll_dice():
    return random.randint(1, 6)

def handle_player_move(player_pos, rolled_dice, player_queue, player_x, player_y):
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

def draw_board():
    box_size = 80
    num = 1
    for i in range(10):
        if i % 2 == 0:
             for j in range(10):
                box_x = j * box_size
                box_y = screen_height - (i + 1) * box_size
                box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                pygame.draw.rect(screen, dark_red, box_rect, 1)
                if num % 2 != 0:
                    pygame.draw.rect(screen, dark_red, box_rect)
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=box_rect.center)
                screen.blit(text, text_rect)
                num += 1
        else:
            for j in range(9, -1, -1):
                box_x = j * box_size
                box_y = screen_height - (i + 1) * box_size
                box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                pygame.draw.rect(screen, dark_red, box_rect, 1)
                if num % 2 != 0:
                    pygame.draw.rect(screen, dark_red, box_rect)
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=box_rect.center)
                screen.blit(text, text_rect)
                num += 1

def main_game():
    global player1_pos, player2_pos, current_turn, rolled_dice
    global player1_x, player1_y, player2_x, player2_y
    global player1_queue, player2_queue 

    clock = pygame.time.Clock()
    delay = 400

    while True:  
        player1_pos = 1
        player2_pos = 1
        player1_x, player1_y = 30, screen_height - 70
        player2_x, player2_y = 30, screen_height - 70
        player1_queue = []
        player2_queue = []
        current_turn = 0
        rolled_dice = None

        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if dice_button_rect.collidepoint(event.pos):
                        roll_sound.play()
                        handle_dice_roll()

            screen.fill(white)
            draw_board()
            draw_ladders(screen, ladders)
            draw_snakes(screen, snakes)
            draw_dice_roll_text(screen,rolled_dice)
            
            if rolled_dice is not None:
                dice_image = dice_images[rolled_dice - 1]
                screen.blit(dice_image, (dice_button_x, dice_button_y))
            else:
                screen.blit(dice_images[0], (dice_button_x, dice_button_y))

            if player1_queue:
                player1_x, player1_y = player1_queue.pop(0)
                pygame.time.delay(delay)
            if player2_queue:
                player2_x, player2_y = player2_queue.pop(0)
                pygame.time.delay(delay)
            screen.blit(player1_symbol, (player1_x, player1_y))
            screen.blit(player2_symbol, (player2_x, player2_y))

            if rolled_dice is not None:
                if player_turns[current_turn] == 1:
                    player1_pos, player1_queue, player1_x, player1_y = handle_player_move(player1_pos, rolled_dice, player1_queue, player1_x, player1_y)
                else:
                    player2_pos, player2_queue, player2_x, player2_y = handle_player_move(player2_pos, rolled_dice, player2_queue, player2_x, player2_y)
                rolled_dice = None
                current_turn = (current_turn + 1) % len(player_turns)

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
            clock.tick(30)

        welcome_screen()

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
        pygame.draw.rect(screen, black, play_button_rect)
        pygame.draw.rect(screen, black, quit_button_rect)

        play_text = font.render("Play", True, white)
        screen.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))

        quit_text = font.render("Quit", True, white)
        screen.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))

        pygame.display.flip()

welcome_screen()
