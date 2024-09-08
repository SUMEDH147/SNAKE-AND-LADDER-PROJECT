import pygame
import random
pygame.init()
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 50
PLAYER_SIZE = 20
player_pos = [0, 0]
ladders = [(1, 38), (4, 14), (9, 31), (21, 42), (28, 84), (36, 44), (51, 67), (71, 91), (80, 100)]
snakes = [(17, 7), (54, 34), (62, 19), (64, 60), (87, 24), (93, 73), (95, 75), (98, 78)]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    dice_roll = random.randint(1, 6)
    player_pos[0] += dice_roll
    if player_pos[0] > 100:
        player_pos[0] = 100
    for ladder in ladders:
        if player_pos[0] == ladder[0]:
            player_pos[0] = ladder[1]
    for snake in snakes:
        if player_pos[0] == snake[0]:
            player_pos[0] = snake[1]
    screen.fill((255, 255, 255))
    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, (0, 0, 0), (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
    pygame.draw.rect(screen, (0, 0, 255), (player_pos[0] % 10 * SQUARE_SIZE, player_pos[1] * SQUARE_SIZE, PLAYER_SIZE, PLAYER_SIZE))
    pygame.display.flip()
    pygame.time.delay(1000)
