import pygame
pygame.init()
info = pygame.display.Info()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((1000,800))
screen_size_text = font.render(f"Screen size: {info.current_w}x{info.current_h}", True, (0, 0, 0))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.display.flip()
pygame.quit()
