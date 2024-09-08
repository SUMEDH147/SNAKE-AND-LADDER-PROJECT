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

sky_blue= (135, 206, 235)
white = (255, 255, 255)
black = (0, 0, 0)
brick_red = (178, 34, 34)
baby_blue = (161,201,242)
forest_green = (0, 128, 0)
amber=(204, 102, 0)
baby_red=(255,197,197)
maroon=(102,0,0)
bordeaux=(139,10,26)
baby_green=(198,244,214)

font = pygame.font.Font(None, 64)
fontt = pygame.font.Font(None, 32)
fonttt=pygame.font.Font(None,48)
roll_sound = pygame.mixer.Sound('/Users/sirishapulupula/Downloads/dice sound.mp3')
n1=' '
n2=' '
paused=False
message=font.render("YOU GOTTA FALL TO RISE !",True,bordeaux)
welcome_message = font.render("Welcome to Snake and Ladder Game !", True,black)
button_width = 200
button_height = 100
button_margin = 50
play_button_x = screen_width // 2 - button_width // 2
play_button_y = screen_height // 2 - button_height // 2
play_button_rect = pygame.Rect(play_button_x, play_button_y, button_width, button_height)
quit_button_x = screen_width // 2 - button_width // 2
quit_button_y = play_button_y + button_height + button_margin
quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)
SGBx=screen_width // 2 - button_width // 2
SGBy=play_button_y + button_height + button_margin
start_game_button_rect=pygame.Rect(SGBx-50,SGBy, button_width+100, button_height)
BBx=screen_width // 2 - button_width // 2
BBy=SGBy+ button_height + button_margin
back_button_rect=pygame.Rect(BBx,BBy, button_width, button_height)
player1=pygame.Rect(play_button_x-100, play_button_y-100, (button_width*2), (button_height/2))
player2=pygame.Rect(quit_button_x-100, quit_button_y-150, (button_width*2), (button_height/2))
pause_button_rect=pygame.Rect(940,10,50,50)

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
active=None

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

last_rolled_dice=1
def handle_dice_roll():
    global rolled_dice,last_rolled_dice
    rolled_dice = roll_dice_animation()
    last_rolled_dice=rolled_dice
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
        pygame.draw.line(screen, amber, (start_x1, start_y), (end_x1, end_y), 7)
        pygame.draw.line(screen, amber, (start_x2, start_y), (end_x2, end_y), 7)

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
        pygame.draw.line(screen, forest_green, (start_x, start_y), (end_x, end_y), 5)

def roll_dice():
    return random.randint(1, 6)

def handle_player_move(player_pos, rolled_dice, player_queue, player_x, player_y):
    new_pos = player_pos + rolled_dice
    if new_pos >100:
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
                pygame.draw.rect(screen,sky_blue, box_rect, 1)
                if num % 2 != 0:
                    pygame.draw.rect(screen,sky_blue, box_rect)
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=box_rect.center)
                screen.blit(text, text_rect)
                num += 1
        else:
            for j in range(9, -1, -1):
                box_x = j * box_size
                box_y = screen_height - (i + 1) * box_size
                box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                pygame.draw.rect(screen,sky_blue, box_rect, 1)
                if num % 2 != 0:
                    pygame.draw.rect(screen,sky_blue, box_rect)
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=box_rect.center)
                screen.blit(text, text_rect)
                num += 1
    pygame.draw.rect(screen,sky_blue,pygame.Rect(810,160,200,200))
    p1=fontt.render(n1,True,amber)
    screen.blit(p1,(810,240))
    p2=fontt.render(n2,True,amber)
    screen.blit(p2,(810,335))
    pause_button_rect=pygame.Rect(940,10,50,50)
    pygame.draw.rect(screen,sky_blue,pause_button_rect)
    pygame.draw.line(screen, forest_green,(955,20),(955,50),10)
    pygame.draw.line(screen, forest_green,(975,20),(975,50),10)
    screen.blit(player1_symbol,(play_button_x+420, play_button_y-180))
    screen.blit(player2_symbol,(play_button_x+420, play_button_y-80))

def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_button_rect.collidepoint(event.pos):
                    pause_game()

def pause_game():
    global paused
    resume_button_rect = pygame.Rect(450,320, 100,100)
    new_game_button_rect = pygame.Rect(screen_width // 2 - button_width // 2-35, screen_height // 2 + 60, button_width+70, button_height)
    quit_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 200, button_width, button_height)
    while True:
        screen.fill(baby_green)
        new_game_text = font.render("NEW GAME ", True,white)
        quit_text = font.render("QUIT", True,white)
        
        triangle=(480,330),(480,410),(540,370)
        pygame.draw.rect(screen, forest_green, resume_button_rect)
        pygame.draw.rect(screen, forest_green, new_game_button_rect)
        pygame.draw.rect(screen, forest_green, quit_button_rect)
        pygame.draw.line(screen,sky_blue,(465,330),(465,410),10)
        pygame.draw.polygon(screen,sky_blue,triangle)
 
        screen.blit(new_game_text, (370,490))
        screen.blit(quit_text, (440,630))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button_rect.collidepoint(event.pos):
                    print("gg")
                    paused=False
                    return
                elif new_game_button_rect.collidepoint(event.pos):
                    welcome_screen() 
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

def main_game():
    global player1_pos, player2_pos, current_turn, rolled_dice,paused
    global player1_x, player1_y, player2_x, player2_y
    global player1_queue, player2_queue
    global player_turns

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
        player_turns=[1,2]

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
                    if pause_button_rect.collidepoint(event.pos):
                        paused=True
                        pause_game()

            screen.fill(white)
            draw_board()
            draw_ladders(screen, ladders)
            draw_snakes(screen, snakes)

            dice_image = dice_images[last_rolled_dice - 1]
            screen.blit(dice_image, (dice_button_x, dice_button_y))

            if rolled_dice is not None:
                rolled_dice_value = rolled_dice
            else:
                rolled_dice_value = last_rolled_dice
                if player_turns[current_turn]==1:
                    rolled_dice_text = font.render(str(rolled_dice_value), True, amber)
                    screen.blit(rolled_dice_text, (930, 280))
                else:
                    rolled_dice_text = font.render(str(rolled_dice_value), True, amber)
                    screen.blit(rolled_dice_text, (930, 180))

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

            pygame.display.flip()
            clock.tick(60)
            if player1_pos == 100 or player2_pos == 100:
                game_over=True
                
            

        time.sleep(2)

        welcome_screen()

def welcome_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    player_game()
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(sky_blue)
        screen.blit(welcome_message, (screen_width // 2 - welcome_message.get_width() // 2, screen_height // 8))
        pygame.draw.rect(screen,black, play_button_rect)
        pygame.draw.rect(screen,black, quit_button_rect)

        play_text = font.render("PLAY", True, white)
        screen.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))

        quit_text = font.render("QUIT", True, white)
        screen.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))

        pygame.display.flip()

def draw_player_name_input_boxes():
    
    pygame.draw.rect(screen,white,player1)
    pygame.draw.rect(screen,white,player2)
    
    player1_text = fontt.render("PLAYER 1-NAME",True,bordeaux)
    screen.blit(player1_text, (play_button_x - 90, play_button_y - 130))
    screen.blit(player1_symbol,(play_button_x+310, play_button_y-107))
    
    player2_text = fontt.render("PLAYER 2-NAME",True,bordeaux)
    screen.blit(player2_text, (play_button_x-90, play_button_y-30))
    screen.blit(player2_symbol,(play_button_x+310, play_button_y-7))
    
    pygame.draw.rect(screen,bordeaux, start_game_button_rect)
    start_text = font.render("START GAME", True,white)
    screen.blit(start_text, (SGBx-45, SGBy+30))
       
    pygame.draw.rect(screen,bordeaux, back_button_rect)
    back_text=font.render("BACK", True,white)
    screen.blit(back_text,(BBx+40,BBy+25))

    screen.blit(message,(200,100))

def player_game():
    global n1,n2
    screen.fill(baby_red)
    while True:
        draw_player_name_input_boxes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_game_button_rect.collidepoint(event.pos):
                    main_game()
                elif back_button_rect.collidepoint(event.pos):
                    welcome_screen()
                elif player1.collidepoint(event.pos):
                    active='player1'
                elif player2.collidepoint(event.pos):
                    active='player2'
            elif event.type == pygame.KEYDOWN:
                if active == 'player1':
                    if event.key == pygame.K_BACKSPACE:
                        n1 = n1[:-1]
                    elif event.unicode.isalnum():
                        n1 += event.unicode
                elif active == 'player2':
                    if event.key == pygame.K_BACKSPACE:
                        n2 = n2[:-1]
                    elif event.unicode.isalnum():
                        n2 += event.unicode

        player1_text = font.render(n1, True,bordeaux)
        screen.blit(player1_text, (play_button_x -90, play_button_y - 100))
        player2_text = font.render(n2, True,bordeaux)
        screen.blit(player2_text, (play_button_x -90, play_button_y ))
        pygame.display.flip()

welcome_screen()

