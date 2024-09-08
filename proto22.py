import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake and Ladder Game")

cyan = (0, 255, 255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
dark_red = (139, 0, 0)

font = pygame.font.Font(None, 64)
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

rolled_dice = None
player_turns = [1, 2]
current_turn = 0
player1_pos = 1
player2_pos = 1
player1_queue = []
player2_queue = []
player1_x = 30
player1_y = screen_height - 70
player2_x = 30
player2_y = screen_height - 70

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

def calculate_position(position):
    row = (position - 1) // 10
    col = (position - 1) % 10
    if row % 2 == 1:
        col = 9 - col  
    x = col * 80 + 10
    y = screen_height - (row + 1) * 80 + 10
    return x, y

def update_queue(start_pos, end_pos, queue, ladder=None, snake=None):
    queue.clear()
    if ladder:
        ladder_start_x, ladder_start_y = calculate_position(ladder["start"])
        ladder_end_x, ladder_end_y = calculate_position(ladder["end"])
        steps = 20
        for i in range(steps):
            x = ladder_start_x + (ladder_end_x - ladder_start_x) * i / steps
            y = ladder_start_y + (ladder_end_y - ladder_start_y) * i / steps
            queue.append((x, y))
        queue.append((ladder_end_x, ladder_end_y))
    elif snake:
        snake_start_x, snake_start_y = calculate_position(snake["start"])
        snake_end_x, snake_end_y = calculate_position(snake["end"])
        steps = 20
        for i in range(steps):
            x = snake_start_x + (snake_end_x - snake_start_x) * i / steps
            y = snake_start_y + (snake_end_y - snake_start_y) * i / steps
            queue.append((x, y))
        queue.append((snake_end_x, snake_end_y))
    else:
        for pos in range(start_pos + 1, end_pos + 1):
            x, y = calculate_position(pos)
            queue.append((x, y))

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
        pygame.draw.line(screen, (0, 0, 255), (start_x, start_y), (end_x, end_y), 5)

game_started = False
rolling = False
dice_animation_time = 0
clock = pygame.time.Clock()

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
            elif game_started and dice_button_rect.collidepoint(event.pos):
                rolling = True
                dice_animation_time = pygame.time.get_ticks()
                rolled_dice = None
                roll_sound.play()

    if rolling:
        elapsed_time = pygame.time.get_ticks() - dice_animation_time
        num_frames = 30
        frame_index = (elapsed_time // (1000 // num_frames)) % 6
        screen.fill(white)
        screen.blit(dice_images[frame_index], (dice_button_x, dice_button_y))
        if elapsed_time > 1000:
            rolled_dice = random.randint(1, 6)
            rolling = False
            if player_turns[current_turn] == 1:
                if player1_pos + rolled_dice > 100:
                    print("ROLL NOT COUNTED-1")
                else:
                    new_pos = player1_pos + rolled_dice
                    for ladder in ladders:
                        if new_pos == ladder["start"]:
                            update_queue(player1_pos, ladder["start"], player1_queue, ladder=ladder)
                            player1_pos = ladder["end"]
                            update_queue(ladder["end"] - 1, player1_pos, player1_queue)
                            break
                    else:
                        for snake in snakes:
                            if new_pos == snake["start"]:
                                update_queue(player1_pos, snake["start"], player1_queue, snake=snake)
                                player1_pos = snake["end"]
                                update_queue(snake["end"] - 1, player1_pos, player1_queue)
                                break
                        else:
                            update_queue(player1_pos, new_pos, player1_queue)
                            player1_pos = new_pos
                    for snake in snakes:
                        if player1_pos == snake["start"]:
                            player1_pos = snake["end"]
                            update_queue(player1_pos, player1_pos, player1_queue)

            else:
                if player2_pos + rolled_dice > 100:
                    print("ROLL NOT COUNTED-2")
                else:
                    new_pos = player2_pos + rolled_dice
                    for ladder in ladders:
                        if new_pos == ladder["start"]:
                            update_queue(player2_pos, ladder["start"], player2_queue, ladder=ladder)
                            player2_pos = ladder["end"]
                            update_queue(ladder["end"] - 1, player2_pos, player2_queue)
                            break
                    else:
                        for snake in snakes:
                            if new_pos == snake["start"]:
                                update_queue(player2_pos, snake["start"], player2_queue, snake=snake)
                                player2_pos = snake["end"]
                                update_queue(snake["end"] - 1, player2_pos, player2_queue)
                                break
                        else:
                            update_queue(player2_pos, new_pos, player2_queue)
                            player2_pos = new_pos

                    for snake in snakes:
                        if player2_pos == snake["start"]:
                            player2_pos = snake["end"]
                            update_queue(player2_pos, player2_pos, player2_queue)

            current_turn = (current_turn + 1) % 2

    if not game_started:
        screen.fill(cyan)
        screen.blit(welcome_message, (screen_width // 2 - welcome_message.get_width() // 2, 50))
        pygame.draw.rect(screen, dark_red, play_button_rect)
        pygame.draw.rect(screen, red, play_button_rect.inflate(-10, -10))
        play_text = font.render("Play", True, white)
        screen.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))
        pygame.draw.rect(screen, dark_red, quit_button_rect)
        pygame.draw.rect(screen, red, quit_button_rect.inflate(-10, -10))
        quit_text = font.render("Quit", True, white)
        screen.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))
    
    else:
        screen.fill(white)
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
        draw_ladders(screen,ladders)
        draw_snakes(screen,snakes)
        

        if player1_queue:
            player1_x, player1_y = player1_queue.pop(0)
            pygame.time.delay(400)
        if player2_queue:
            player2_x, player2_y = player2_queue.pop(0)
            pygame.time.delay(400)

        screen.blit(player1_symbol, (player1_x, player1_y))
        screen.blit(player2_symbol, (player2_x, player2_y))

        if rolling:
            elapsed_time = pygame.time.get_ticks() - dice_animation_time
            num_frames = 30
            frame_index = (elapsed_time // (1000 // num_frames)) % 6
            screen.blit(dice_images[frame_index], (dice_button_x, dice_button_y))
        else:
            screen.blit(dice_images[rolled_dice - 1] if rolled_dice else dice_images[0], (dice_button_x, dice_button_y))

        if player1_pos == 100:
            print("PLAYER-1 WINS")
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        elif player2_pos == 100:
            print("PLAYER-2 WINS")
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(30)
