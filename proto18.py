import pygame
import sys
import random

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

player1_symbol = pygame.Surface((20, 20))
player1_symbol.fill((0, 0, 0))
pygame.draw.circle(player1_symbol, (0, 0, 0), (10, 10), 10)

player2_symbol = pygame.Surface((20, 20))
player2_symbol.fill((255, 255, 255))
pygame.draw.polygon(player2_symbol, (0, 0, 0), ((10, 0), (20, 10), (10, 20), (0, 10)))

player1_target_x = None
player1_target_y = None
player1_move_speed = 10

player1_x = 30
player1_y = screen_height - 30

player2_x = 60
player2_y = screen_height - 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game_started = True
            elif quit_button_rect.collidepoint(event.pos):
                running = False
            elif game_started and dice_button_rect.collidepoint(event.pos):
                rolled_dice = random.randint(1, 6)
                if player_turns[current_turn] == 1:
                    if player1_pos+rolled_dice > 100:
                        print("ROLL NOT COUNTED")
                    else:
                        player1_pos += rolled_dice
                        player1_target_x = ((player1_pos - 1) % 10) * 80 + 30
                        player1_target_y = screen_height - (((player1_pos - 1) // 10) % 10 + 1) * 80 + 30
                        if (player1_pos - 1) // 10 % 2 == 1:
                            player1_target_x = (9 - ((player1_pos - 1) % 10)) * 80 + 30
                else:
                    if player2_pos+rolled_dice > 100:
                        print("roll not counted")
                    else:
                        player2_pos += rolled_dice
                current_turn = (current_turn + 1) % 2

    if not game_started:
        screen.fill(cyan)
        screen.blit(welcome_message, (screen_width // 2 - welcome_message.get_width() // 2, 50))
        pygame.draw.ellipse(screen, black, play_button_rect, 2)
        play_button_text = font.render("Play", True, black)
        screen.blit(play_button_text, (play_button_x + button_width // 2  - play_button_text.get_width() // 2, play_button_y + button_height // 2 - play_button_text.get_height() // 2))
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
        for i in range(10):
            if i % 2 == 0:
                for j in range(10):
                    box_x = j * box_size
                    box_y = screen_height - (i + 1) * box_size
                    box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                    pygame.draw.rect(screen, red, box_rect, 1)
                    if num % 2 != 0:
                        pygame.draw.rect(screen, red, box_rect)
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
                    pygame.draw.rect(screen, red, box_rect, 1)
                    if num % 2 != 0:
                        pygame.draw.rect(screen, red, box_rect)
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(num), True, black)
                    text_rect = text.get_rect(center=box_rect.center)
                    screen.blit(text, text_rect)
                    num += 1

        if player1_target_x is not None:
            player1_x += (player1_target_x - player1_x) / player1_move_speed
            player1_y += (player1_target_y - player1_y) / player1_move_speed
            if abs(player1_x - player1_target_x) < 1 and abs(player1_y - player1_target_y) < 1:
                player1_x = player1_target_x
                player1_y = player1_target_y
                player1_target_x = None
                player1_target_y = None

        screen.blit(player1_symbol, (int(player1_x), int(player1_y)))
        screen.blit(player2_symbol, (player2_x, player2_y))

        if rolled_dice is not None:
            dice_image_y = dice_button_y - dice_button_height - 10
            screen.blit(dice_images[rolled_dice - 1], (dice_button_x, dice_image_y))

        pygame.draw.rect(screen, dark_red, dice_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Roll", True, black)
        text_rect = text.get_rect(center=dice_button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
