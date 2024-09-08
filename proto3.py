import pygame
import sys
pygame.init()
game_width = 1000
game_height = 800
screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Snake and LAdders Game-Play")
red = (255, 0, 0)
dark_red=(139,0,0)
white = (255, 255, 255)
black = (0, 0, 0)
box_size = 80
font = pygame.font.Font(None, 36)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)
    num = 1
    for i in range(10):
        if i % 2 == 0:
            for j in range(10):
                box_x = j*box_size
                box_y = game_height - (i + 1) * box_size
                box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                pygame.draw.rect(screen, dark_red, box_rect, 1)
                pygame.draw.rect(screen, red, box_rect)
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=box_rect.center)
                screen.blit(text, text_rect)
                num += 1
        else:
            for j in range(9, -1, -1):
                box_x = j * box_size
                box_y = game_height - (i + 1) * box_size
                box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                pygame.draw.rect(screen, dark_red, box_rect, 1)
                pygame.draw.rect(screen, red, box_rect)
                text = font.render(str(num), True, black)
                text_rect = text.get_rect(center=box_rect.center)
                screen.blit(text, text_rect)
                num += 1
    pygame.display.flip()
pygame.quit()
sys.exit()
