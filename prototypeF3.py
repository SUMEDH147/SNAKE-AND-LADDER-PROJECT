import pygame
import sys
import random
import math


pygame.init()


screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake and Ladder Game")

cyan = (0, 255, 255)
white = (255, 255, 255)
black = (0, 0, 0)
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
running = True
dice_images = [
    pygame.image.load('/Users/sirishapulupula/Downloads/dice1.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice2.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice3.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice4.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice5.png'),
    pygame.image.load('/Users/sirishapulupula/Downloads/dice6.png')
]
player1_symbol=pygame.image.load('/Users/sirishapulupula/Downloads/pawn.png')
player2_symbol=pygame.image.load('/Users/sirishapulupula/Downloads/pawng.png')

dice_button_width = 100
dice_button_height = 100
dice_button_x = screen_width - dice_button_width - 20
dice_button_y = screen_height - dice_button_height - 20
dice_button_rect = pygame.Rect(dice_button_x, dice_button_y, dice_button_width, dice_button_height)

rolled_dice = None
player_turns = [1, 2]
current_turn = 0

player1_pos = 1
player2_pos = 1
player1_target_x=None
player1_target_y=None
player1_move_speed=10
player2_target_x=None
player2_target_y=None
player2_move_speed=10
player1_x=30
player1_y=screen_height-70
player2_x=30
player2_y=screen_height-70
player1_jump_speed=10
player2_jump_speed=10

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game_started = True
            elif quit_button_rect.collidepoint(event.pos):
                running = False
                player1_pos=1
                player2_pos=1
                current_turn=0
            elif quit_button_rect.collidepoint(event.pos):
                running=False
            elif game_started and dice_button_rect.collidepoint(event.pos):
                rolled_dice = random.randint(1, 6)
                if player_turns[current_turn] == 1:
                    if player1_pos+rolled_dice > 100:
                        print("ROLL NOT COUNTED-1")
                    else:
                        player1_pos += rolled_dice
                        player1_target_x = ((player1_pos - 1) % 10) * 80 + 10
                        player1_target_y = screen_height - (((player1_pos - 1) // 10) % 10 + 1) * 80 + 10
                        if (player1_pos - 1) // 10 % 2 == 1:
                            player1_target_x = (9 - ((player1_pos - 1) % 10)) * 80 + 10
                        for snake in snakes:
                            if player1_pos == snake["start"]:
                                player1_pos = snake["end"]
                                player1_target_x = ((player1_pos - 1) % 10) * 80 + 10
                                player1_target_y = screen_height - (((player1_pos - 1) // 10) % 10 + 1) * 80 + 10
                                if (player1_pos - 1) // 10 % 2 == 1:
                                    player1_target_x = (9 - ((player1_pos - 1) % 10)) * 80 + 10
                        for ladder in ladders:
                            if player1_pos == ladder["start"]:
                                player1_pos = ladder["end"]
                                player1_target_x = ((player1_pos - 1) % 10) * 80 + 10
                                player1_target_y = screen_height - (((player1_pos - 1) // 10) % 10 + 1) * 80 + 10
                                if (player1_pos - 1) // 10 % 2 == 1:
                                    player1_target_x = (9 - ((player1_pos - 1) % 10)) * 80 + 10
                else:
                    if player2_pos + rolled_dice > 100:
                        print("ROLL NOT COUNTED-2")
                    else:
                        player2_pos += rolled_dice
                        player2_target_x = ((player2_pos - 1) % 10) * 80 + 10
                        player2_target_y = screen_height - (((player2_pos - 1) // 10) % 10 + 1) * 80 + 10
                        if (player2_pos - 1) // 10 % 2 == 1:
                            player2_target_x = (9 - ((player2_pos - 1) % 10)) * 80 + 10
                        for snake in snakes:
                            if player2_pos == snake["start"]:
                                player2_pos = snake["end"]
                                player2_target_x = ((player2_pos - 1) % 10) * 80 + 10
                                player2_target_y = screen_height - (((player2_pos - 1) // 10) % 10 + 1) * 80 + 10
                                if (player2_pos - 1) // 10 % 2 == 1:
                                    player2_target_x = (9 - ((player2_pos - 1) % 10)) * 80 + 10
                        for ladder in ladders:
                            if player2_pos == ladder["start"]:
                                player2_pos = ladder["end"]
                                player2_target_x = ((player2_pos - 1) % 10) * 80 + 10
                                player2_target_y = screen_height - (((player2_pos - 1) // 10) % 10 + 1) * 80 + 10
                                if (player2_pos - 1) // 10 % 2 == 1:
                                    player2_target_x = (9 - ((player2_pos - 1) % 10)) * 80 + 10

                current_turn = (current_turn + 1) % 2

    if not game_started:
        screen.fill(cyan)
        screen.blit(welcome_message, (screen_width // 2 - welcome_message.get_width() // 2, 50))
        pygame.draw.ellipse(screen, black, play_button_rect, 2)
        play_button_text = font.render("Play", True, black)
        screen.blit(play_button_text, (play_button_x + button_width // 2 - play_button_text.get_width() // 2, play_button_y + button_height // 2 - play_button_text.get_height() // 2))
        pygame.draw.ellipse(screen, black, quit_button_rect, 2)
        quit_button_text = font.render("Quit", True, black)
        screen.blit(quit_button_text, (quit_button_x + button_width // 2 - quit_button_text.get_width() // 2, quit_button_y + button_height // 2 - quit_button_text.get_height() // 2))
    else:
        screen.fill(white)
        red = (255, 0, 0)
        dark_red = (139, 0, 0)
        black = (0, 0, 0)
        box_size = 80
        num = 1
        if rolled_dice is not None:
            dice_image_y = dice_button_y - dice_button_height - 10
            screen.blit(dice_images[rolled_dice - 1], (dice_button_x, dice_image_y))
        for i in range(10):
            if i % 2 == 0:
                for j in range(10):
                    box_x = j * box_size
                    box_y = screen_height - (i + 1) * box_size
                    box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                    pygame.draw.rect(screen, dark_red, box_rect, 1)
                    if num % 2 != 0:
                        pygame.draw.rect(screen, dark_red, box_rect)
                    font = pygame.font.Font(None, 36)
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
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(num), True, black)
                    text_rect = text.get_rect(center=box_rect.center)
                    screen.blit(text, text_rect)
                    num += 1

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
            start_x1 = ((ladder["start"] - 1) % 10) * box_size + 20
            start_x2 = ((ladder["start"] -1 ) % 10) * box_size + 60
            start_y = screen_height - (((ladder["start"] - 1) // 10) % 10 + 1) * box_size + 40
            if (ladder["start"] - 1) // 10 % 2 == 1:
                start_x1 = (9 - ((ladder["start"] - 1) % 10)) * box_size + 20
                start_x2 = (9 - ((ladder["start"] -1 ) % 10)) * box_size + 60
            end_x1 = ((ladder["end"] - 1) % 10) * box_size + 20
            end_x2 = ((ladder["end"] - 1) % 10) * box_size + 60
            end_y = screen_height - (((ladder["end"] - 1) // 10) % 10 + 1) * box_size + 40
            if (ladder["end"] - 1) // 10 % 2 == 1:
                end_x1 = (9 - ((ladder["end"] - 1) % 10)) * box_size + 20
                end_x2 = (9 - ((ladder["end"] - 1) % 10)) * box_size + 60
            spacing=(end_y-start_y)/6
            for i in range(1,6):
                t=(i*spacing)/(end_y-start_y)
                x=start_x1+(end_x1-start_x1)*t
                y=start_y+(i*spacing)
                pygame.draw.line(screen, (204,102,0), (x,y), (x + 40, y), 3)               
            pygame.draw.line(screen, (204,102,0), (start_x1, start_y), (end_x1, end_y), 7)
            pygame.draw.line(screen, (204,102,0), (start_x2, start_y), (end_x2, end_y), 7)
            
        screen.blit(player1_symbol, (player1_x, player1_y))
        screen.blit(player2_symbol, (player2_x, player2_y))

        if player1_target_x is not None and player1_target_y is not None:
            if abs(player1_x - player1_target_x) > player1_jump_speed:
                dx = player1_target_x - player1_x
                dy = player1_target_y - player1_y
                dist = math.sqrt(dx**2 + dy**2)
                player1_x += dx / dist * player1_jump_speed
                player1_y += dy / dist * player1_jump_speed
            else:
                player1_x = player1_target_x
                player1_y = player1_target_y
                player1_target_x = None
                player1_target_y = None
                player1_pos=ladder["end"]

        if player2_target_x is not None and player2_target_y is not None:
            if abs(player2_x - player2_target_x) > player2_jump_speed:
                dx = player2_target_x - player2_x
                dy = player2_target_y - player2_y
                dist = math.sqrt(dx**2 + dy**2)
                player2_x += dx / dist * player2_jump_speed
                player2_y += dy / dist * player2_jump_speed
            else:
                player2_x = player2_target_x
                player2_y = player2_target_y
                player2_target_x = None
                player2_target_y = None
                player2_pos=ladder["end"]
            
        for ladder in ladders:
            if player1_pos==ladder["start"]:
                player1_target_x = ((ladder["end"] - 1) % 10) * box_size + 30
                player1_target_y = screen_height - (((ladder["end"] - 1) // 10) % 10 + 1) * box_size + 30
                player1_move_speed = 5
                break
            if player2_pos==ladder["start"]:
                player2_target_x = ((ladder["end"] - 1) % 10) * box_size + 30
                player2_target_y = screen_height - (((ladder["end"] - 1) // 10) % 10 + 1) * box_size + 30
                player2_move_speed = 5
                break

                
        pygame.draw.rect(screen, red, dice_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Roll", True, black)
        text_rect = text.get_rect(center=dice_button_rect.center)
        screen.blit(text, text_rect)

        if player1_pos==100:
            print("PLAYER-1 WINS")
            running=False
        elif player2_pos==100:
            print("PLAYER-2 WINS")
            running=False

    pygame.display.flip()

pygame.quit()
sys.exit()
