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

sky_blue = (135, 206, 235)
white = (255, 255, 255)
black = (0, 0, 0)
brick_red = (178, 34, 34)
baby_blue = (161, 201, 242)
forest_green = (0, 128, 0)
amber = (204, 102, 0)
baby_red = (255, 197, 197)

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
        draw_ladders(screen, ladders)
        draw_snakes(screen, snakes)
        draw_dice(screen, dice_images[random.randint(0, 5)], angle, dice_x, dice_y)
        pygame.display.flip()
        pygame.time.delay(20)
    rolled_dice = random.randint(1, 6)

    start_time = pygame.time.get_ticks()
    roll_duration = 500

    while pygame.time.get_ticks() - start_time < roll_duration:
        angle = ((pygame.time.get_ticks() - start_time) / roll_duration * spin_speed) % 360
        draw_board()
        screen.blit(player1_symbol, (player1_x, player1_y))
        screen.blit(player2_symbol, (player2_x, player2_y))
        draw_ladders(screen, ladders)
        draw_snakes(screen, snakes)
        draw_dice(screen, dice_images[random.randint(0, 5)], angle, dice_x, dice_y)
        pygame.display.flip()
        pygame.time.delay(20)

    draw_board()
    screen.blit(player1_symbol, (player1_x, player1_y))
    screen.blit(player2_symbol, (player2_x, player2_y))
    draw_ladders(screen, ladders)
    draw_snakes(screen, snakes)
    draw_dice(screen, dice_images[rolled_dice - 1], 0, dice_x, dice_y)
    pygame.display.flip()

    return rolled_dice

def draw_dice_roll_text(screen, dice_value):
    dice_text = fontt.render(f"Dice Rolled: {dice_value}", True, black)
    screen.blit(dice_text, (800, 40))

def draw_board():
    screen.fill(sky_blue)
    for i in range(10):
        for j in range(10):
            rect = pygame.Rect(j * 80 + 10, screen_height - (i + 1) * 80 + 10, 80, 80)
            pygame.draw.rect(screen, white, rect)
            pygame.draw.rect(screen, black, rect, 2)
            text = fontt.render(str(i * 10 + j + 1), True, black)
            screen.blit(text, (j * 80 + 30, screen_height - (i + 1) * 80 + 30))

def draw_ladders(screen, ladders):
    for ladder in ladders:
        start_pos = ladder["start"]
        end_pos = ladder["end"]
        start_x, start_y = calculate_position(start_pos)
        end_x, end_y = calculate_position(end_pos)
        pygame.draw.line(screen, forest_green, (start_x + 30, start_y + 30), (end_x + 30, end_y + 30), 10)

def draw_snakes(screen, snakes):
    for snake in snakes:
        start_pos = snake["start"]
        end_pos = snake["end"]
        start_x, start_y = calculate_position(start_pos)
        end_x, end_y = calculate_position(end_pos)
        pygame.draw.line(screen, amber, (start_x + 30, start_y + 30), (end_x + 30, end_y + 30), 10)

def handle_player_move(player, roll_result):
    global player1_pos, player2_pos
    if player == 1:
        start_pos = player1_pos
        end_pos = min(start_pos + roll_result, 100)
        if end_pos in [ladder["start"] for ladder in ladders]:
            ladder = next(ladder for ladder in ladders if ladder["start"] == end_pos)
            update_queue(start_pos, end_pos, player1_queue, ladder=ladder)
            player1_pos = ladder["end"]
        elif end_pos in [snake["start"] for snake in snakes]:
            snake = next(snake for snake in snakes if snake["start"] == end_pos)
            update_queue(start_pos, end_pos, player1_queue, snake=snake)
            player1_pos = snake["end"]
        else:
            update_queue(start_pos, end_pos, player1_queue)
            player1_pos = end_pos
    else:
        start_pos = player2_pos
        end_pos = min(start_pos + roll_result, 100)
        if end_pos in [ladder["start"] for ladder in ladders]:
            ladder = next(ladder for ladder in ladders if ladder["start"] == end_pos)
            update_queue(start_pos, end_pos, player2_queue, ladder=ladder)
            player2_pos = ladder["end"]
        elif end_pos in [snake["start"] for snake in snakes]:
            snake = next(snake for snake in snakes if snake["start"] == end_pos)
            update_queue(start_pos, end_pos, player2_queue, snake=snake)
            player2_pos = snake["end"]
        else:
            update_queue(start_pos, end_pos, player2_queue)
            player2_pos = end_pos

def main_menu():
    while True:
        screen.fill(sky_blue)
        screen.blit(welcome_message, (screen_width // 2 - welcome_message.get_width() // 2, 100))
        pygame.draw.rect(screen, white, play_button_rect)
        pygame.draw.rect(screen, black, play_button_rect, 2)
        pygame.draw.rect(screen, white, quit_button_rect)
        pygame.draw.rect(screen, black, quit_button_rect, 2)
        play_text = font.render("Play", True, black)
        quit_text = font.render("Quit", True, black)
        screen.blit(play_text, (play_button_x + 30, play_button_y + 30))
        screen.blit(quit_text, (quit_button_x + 30, quit_button_y + 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(pos):
                    player_name_entry()
                if quit_button_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

def player_name_entry():
    input_box1 = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 60, 140, 40)
    input_box2 = pygame.Rect(screen_width // 2 + 30, screen_height // 2 - 60, 140, 40)
    start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    text2 = ''
    done = False

    screen.fill(baby_red)
    pygame.draw.rect(screen, white, input_box1)
    pygame.draw.rect(screen, white, input_box2)
    pygame.draw.rect(screen, black, input_box1, 2)
    pygame.draw.rect(screen, black, input_box2, 2)
    pygame.draw.rect(screen, black, start_button_rect)
    screen.blit(font.render("Player 1:", True, black), (input_box1.x - 100, input_box1.y))
    screen.blit(font.render("Player 2:", True, black), (input_box2.x - 100, input_box2.y))
    screen.blit(font.render("Start Game", True, black), (start_button_rect.x + 30, start_button_rect.y + 10))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active = True
                    color = color_active
                elif input_box2.collidepoint(event.pos):
                    active = True
                    color = color_active
                elif start_button_rect.collidepoint(event.pos):
                    # Start the game with the entered names
                    start_game()
                    done = True
                else:
                    active = False
                    color = color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False
                        color = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        if input_box1.collidepoint(event.pos):
                            text = text[:-1]
                        elif input_box2.collidepoint(event.pos):
                            text2 = text2[:-1]
                    else:
                        if input_box1.collidepoint(event.pos):
                            text += event.unicode
                        elif input_box2.collidepoint(event.pos):
                            text2 += event.unicode

        screen.fill(baby_red)
        pygame.draw.rect(screen, color, input_box1, 2)
        pygame.draw.rect(screen, color, input_box2, 2)
        screen.blit(font.render(text, True, color), (input_box1.x + 5, input_box1.y + 5))
        screen.blit(font.render(text2, True, color), (input_box2.x + 5, input_box2.y + 5))
        pygame.draw.rect(screen, black, start_button_rect)
        screen.blit(font.render("Start Game", True, black), (start_button_rect.x + 30, start_button_rect.y + 10))
        pygame.display.flip()

def start_game():
    global player1_name, player2_name
    player1_name = text
    player2_name = text2
    game_loop()

def game_loop():
    global current_turn, rolled_dice

    while True:
        draw_board()
        screen.blit(player1_symbol, (player1_x, player1_y))
        screen.blit(player2_symbol, (player2_x, player2_y))
        draw_ladders(screen, ladders)
        draw_snakes(screen, snakes)

        dice_value = roll_dice_animation()
        draw_dice_roll_text(screen, dice_value)
        pygame.display.flip()

        handle_player_move(player_turns[current_turn], dice_value)
        current_turn = (current_turn + 1) % 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dice_button_rect.collidepoint(event.pos):
                    roll_dice_animation()

main_menu()
